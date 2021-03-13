# Load Packages
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
from sklearn.model_selection import LeaveOneOut
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import tensorflow as tf
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

def findPMD(filepath, outputpath):
    """
        findPMD(filepath, outputpath)
    The main function in PMDfinder.
    
    * filepath: input BED file path.
    * outputpath: the output file path.
    """
    # load DSS methylation data
    methylation = pd.read_csv(filepath, sep='\t', comment='t', header = 0, low_memory=False)

    # store the location and the percent methylation
    a = list(map(float, methylation['X']))
    b = list(map(float, methylation['N']))
    meth_ratio = [i / j for i, j in zip(a, b)]
    # geno_pos = list(map(float, methylation['pos']))

    ### Data Conversion
    # convert methylation ratio to PMD/non-PMD level (y=4x(1-x))
    def methRatio2PMDLevel(meth_ratio):
        n = len(meth_ratio)
        PMD_level = [0]*n
        for i in range(n):
            PMD_level[i] = 4 * meth_ratio[i] * (1 - meth_ratio[i])
        return PMD_level

    PMD_level = methRatio2PMDLevel(meth_ratio)

    ### Sequential Data Matrix
    # Extract sequenctial feature by sliding window
    N = len(PMD_level)
    X = np.zeros((N-1023, 1024))
    for i in range(N-1023):
        X[i, :] = PMD_level[i:i+1024]

    ### Autoencoder
    # latent is the last variable
    latent_dim = 8

    m = Autoencoder(latent_dim)
    m.compile(optimizer='adam', loss=losses.MeanSquaredError())

    # fit the model
    m.fit(X, X, epochs=5, shuffle=True)

    # get the encoded PMD
    encoded_slicing_PMD = m.encoder(X).numpy()

    ### k-means
    kmeans = KMeans(n_clusters=2, random_state=22).fit(encoded_slicing_PMD)
    final_result = kmeans.labels_

    ### Post-processing steps
    ## Remove PMD that is less than 51 bp length
    assign1 = [] # index for the location equal to 1
    for i in range(len(final_result)):
        if final_result[i] == 1:
            assign1.append(i)

    break_pts1 = [] # index for the break point, the next equal to 1 is more than 1bp
    for i in range(1, len(assign1)):
        if assign1[i] - assign1[i-1] > 1:
            break_pts1.append(i)    

    # small_PMD_intervals: identify region that is close with each other 
    small_PMD_intervals = []
    for i in range(1, len(break_pts1)):
        if assign1[break_pts1[i]-1] - assign1[break_pts1[i-1]] + 1 < 101:
            small_PMD_intervals.append(i)

    # change the PMD interval with less than 51 to Non-PMD
    for interval in small_PMD_intervals:
        final_result[assign1[break_pts1[interval-1] : break_pts1[interval]-1]] == 0

    ## Merge PMD that is less than 101 bp from the next one
    # This need to check the non-PMD region length
    assign2 = []
    for i in range(len(final_result)):
        if final_result[i] == 0:
            assign2.append(i)

    break_pts2 = []
    for i in range(1, len(assign2)):
        if assign2[i] - assign2[i-1] > 1:
            break_pts2.append(i)

    # small non_PMD intervals
    small_non_PMD_intervals = []
    for i in range(1, len(break_pts2)):
        if assign2[break_pts2[i]-1] - assign2[break_pts2[i-1]] + 1 < 101:
            small_non_PMD_intervals.append(i)

    # change the PMD interval with less than 51 to Non-PMD
    for interval in small_non_PMD_intervals:
        final_result[assign2[break_pts2[interval-1] : break_pts2[interval]-1]] == 0
    
    # file output
    output_methylation = methylation[:len(methylation)-1023].copy()
    output_methylation.loc[:, 'PMD_predict'] = pd.DataFrame(final_result)[0].map({1: 'Non-PMD', 0: 'PMD'})
    output_methylation.to_csv(outputpath, sep='\t', index = False, header=True)

    # np.savetxt(outputpath, final_result, delimiter=',')
