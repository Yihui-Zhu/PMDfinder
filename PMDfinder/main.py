# Load Packages
import pandas as pd
import numpy as np
import random
import os
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
from sklearn.model_selection import LeaveOneOut
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import tensorflow as tf
tf.enable_eager_execution()
tf.executing_eagerly()
from tensorflow.keras import layers, losses
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Model           
configuration = tf.compat.v1.ConfigProto(device_count={"GPU": 0})
session = tf.compat.v1.Session(config=configuration)
random.seed(12)

class Autoencoder(Model):
    def __init__(self, latent_dim):
        super(Autoencoder, self).__init__()
        self.latent_dim = latent_dim   
        self.encoder = tf.keras.Sequential([
        layers.Dense(latent_dim, activation=layers.LeakyReLU(alpha=0.3)),
        ])
        self.decoder = tf.keras.Sequential([
        layers.Dense(1024, activation=layers.LeakyReLU(alpha=0.3))
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded  

def findPMD(directory, outputpath1, outputpath2, percentile, cutoff):
    """
        findPMD(filepath, outputpath1, outputpath2, percentile, cutoff)
    The main function in PMDfinder.
    
    * directory: input BED files directory path.
    * outputpath1: the output bed file path.
    * outputpath2: the output grange file path.
    * percentile: Percent of samples per CpG coverage, values range from 0 to 1.
    * cutoff: minimum number of reads per CpG site
    """

    # load DSS methylation data
    meth_ratios = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        methylation = pd.read_csv(filepath, sep='\t', comment='t', header = 0, low_memory=False)
        # store the location and the percent methylation
        a = list(map(float, methylation['X']))
        b = list(map(float, methylation['N']))
        # ratio = [i / j for i, j in zip(a, b)]
        twonum = [(i, j) for i, j in zip(a, b)]
        geno_pos = list(map(int, methylation['pos']))
        meth_ratio_dict = dict(zip(geno_pos, twonum))
        meth_ratios.append(meth_ratio_dict)

    ### Data pre-processing
    def methRatioPreprocessing(meth_ratios, percentile, cutoff):
        union_pos = set()
        for d in meth_ratios:
            union_pos |= set(d.keys())
        
        union_pos = sorted(list(union_pos))
        meth_ratio = {}
        for pos in union_pos:
            temp = []
            for i, ratio in enumerate(meth_ratios):
                if pos in ratio:
                    temp.append(i)
            if len(temp) > percentile * len(meth_ratios):
                count = sum([meth_ratios[j][pos][1] for j in temp])
                if count > cutoff:
                    is_meth = sum([meth_ratios[j][pos][0] for j in temp])
                    meth_ratio[pos] =  is_meth / count

        return meth_ratio

    ### Data Conversion
    # convert methylation ratio to PMD/non-PMD level (y=4x(1-x))
    def methRatio2PMDLevel(meth_ratio):
        n = len(meth_ratio)
        PMD_level = [0]*n
        for i in range(n):
            PMD_level[i] = 4 * meth_ratio[i] * (1 - meth_ratio[i])
        return PMD_level

    position2ratio = methRatioPreprocessing(meth_ratios, percentile, cutoff)
    position = list(position2ratio.keys())
    meth_ratio = list(position2ratio.values())
    PMD_level = methRatio2PMDLevel(meth_ratio)

    ### Sequential Data Matrix
    # Extract sequenctial feature by sliding window
    N = len(PMD_level)
    X = np.zeros((N-1023, 1024))
    for i in range(N-1023):
        X[i, :] = PMD_level[i:i+1024]
    
    X = X.astype(np.float32)

    ### Autoencoder
    # latent is the last variable
    latent_dim = 8

    m = Autoencoder(latent_dim)
    m.compile(optimizer='adam', loss=losses.MeanSquaredError())

    # fit the model
    m.fit(X, X, epochs=3, shuffle=True)

    # get the encoded PMD
    encoded_slicing_PMD = m.encoder(X).numpy()

    ### k-means
    kmeans = KMeans(n_clusters=2, random_state=22).fit(encoded_slicing_PMD)
    final_result = kmeans.labels_

    ### Post-processing steps
    ## Remove PMD that is less than 6 bp length
    assign1 = [] # index for the location equal to 1
    for i in range(len(final_result)):
        if final_result[i] == 1:
            assign1.append(i)

    break_pts1 = [0] # index for the break point, the next equal to 1 is more than 1bp
    for i in range(1, len(assign1)):
        if assign1[i] - assign1[i-1] > 1:
            break_pts1.append(i)    
    
    # small_PMD_intervals: identify region that is close with each other 
    small_PMD_intervals = []
    for i in range(1, len(break_pts1)):
        if assign1[break_pts1[i]-1] - assign1[break_pts1[i-1]] + 1 < 6:
            small_PMD_intervals.append(i)

    # change the PMD interval with less than 6 to Non-PMD
    for interval in small_PMD_intervals:
        final_result[assign1[break_pts1[interval-1] : break_pts1[interval]]] = 0

    ## Merge PMD that is less than 6 bp from the next one
    # This need to check the non-PMD region length
    assign2 = []
    for i in range(len(final_result)):
        if final_result[i] == 0:
            assign2.append(i)

    break_pts2 = [0]
    for i in range(1, len(assign2)):
        if assign2[i] - assign2[i-1] > 1:
            break_pts2.append(i)

    # small non_PMD intervals
    small_non_PMD_intervals = []
    for i in range(1, len(break_pts2)):
        if assign2[break_pts2[i]-1] - assign2[break_pts2[i-1]] + 1 < 6:
            small_non_PMD_intervals.append(i)

    # change the PMD interval with less than 6 to Non-PMD
    for interval in small_non_PMD_intervals:
        final_result[assign2[break_pts2[interval-1] : break_pts2[interval]]] = 1
    
    # file output
    output_methylation = pd.DataFrame(['chr22'] * (len(meth_ratio)-1023), columns=['chr'])
    output_methylation.loc[:, 'pos'] = position[:len(meth_ratio)-1023]
    output_methylation.loc[:, 'meth_ratio'] = meth_ratio[:len(meth_ratio)-1023]

    one_avg = np.mean([PMD_level[x] for x in range(len(final_result)) if final_result[x] == 1])
    zero_avg = np.mean([PMD_level[x] for x in range(len(final_result)) if final_result[x] == 0])

    output_methylation.loc[:, 'PMD_predict'] = pd.DataFrame(final_result)[0].map({1: 'PMD', 0: 'Non-PMD'}) if one_avg > zero_avg else pd.DataFrame(final_result)[0].map({1: 'Non-PMD', 0: 'PMD'})
    output_methylation.to_csv(outputpath1, sep='\t', index = False, header=True)

    # output grange file
    df = pd.DataFrame(columns = ['chr', 'start', 'end', 'status'])

    ncols = len(output_methylation)
    i, j = 0, 0

    while i < ncols:
        if j == ncols:
            df = df.append({'chr': output_methylation.iloc[i, 0], 'start': output_methylation.iloc[i, 1], 'end': output_methylation.iloc[j-1, 1], 'status': ti}, ignore_index = True)
            break

        ti = output_methylation.iloc[i, 3]
        tj = output_methylation.iloc[j, 3]
        if tj == ti:
            j += 1
        else:
            df = df.append({'chr': output_methylation.iloc[i, 0], 'start': output_methylation.iloc[i, 1], 'end': output_methylation.iloc[j-1, 1], 'status': ti}, ignore_index = True)
            i = j

    df.to_csv(outputpath2, sep='\t', index = False, header=True)
    # print(df)
    generateFigure(output_methylation, 'tests/meth_plot.png')

    print("Finished PMDfinder!")

    # np.savetxt(outputpath1, outputpath2, final_result, delimiter=',')

def generateFigure(output_methylation, path):
    """
        generateFigure(output_methylation, path)
    The plotting function in PMDfinder.
    
    * output_methylation: BED file.
    * path: the output figure path.
    """

    fig = plt.figure(figsize=(40, 15), dpi=100)

    plt.plot(output_methylation['pos'], output_methylation['meth_ratio'], 'o', color='black', label='meth ratio', ms = 1)
    plt.plot(output_methylation['pos'], output_methylation['PMD_predict'] == 'PMD', 'o', color='red')

    current_values = plt.gca().get_xticks()
    plt.gca().set_xticklabels(['{:.0f}'.format(x) for x in current_values])

    fig.savefig(path)
