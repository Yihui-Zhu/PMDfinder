# PMDfinder

### A Python Package to identify partially methylation domains (PMDs) from whole-genome bisulfite sequencing (WGBS) data

By Yihui Zhu

## Language
Python 3

## Running PMDfinder:
First prepare WGBS data in BED file format.

## Installation
Make local copy of the package from Github and change directory in Terminal to the local package folder
```
$ git clone https://github.com/Yihui-Zhu/PMDfinder.git
$ cd PMDfinder
$ pip install .
```

## Generic Usage Example
```
$ python
>>> from PMDfinder import findPMD
>>> findPMD("tests/DSS_chr22_files", "tests/cpgIslandExt.hg38.bed", "tests/output_meth.bed", "tests/output_GRanges.bed", 0.9, 20, "tests/meth_plot.png")
```

## Function
`findPMD` is the main function of the PMDfinder package with methylome as input with output as PMD location.
```
findPMD(directory, CpG_Island_path, outputpath1, outputpath2, percentile=0.9, cutoff=20, plotpath='tests/meth_plot.png')
```
- `directory`: input BED files directory path.
- `CpG_Island_path`: input CpG Island BED files path.
- `outputpath1`: the output bed file path.
- `outputpath2`: the output grange file path.
- `percentile`: Percent of samples per CpG coverage, values range from 0 to 1.
- `cutoff`: minimum number of reads per CpG site
- `plotpath`: the output figure path. 

`generateFigure` is the plotting function of PMDfinder package that enable plot results from the output methylation file
```
generateFigure(output_methylation, path)
```
- `output_methylation`: BED file.
- `path`: the output figure path.

## Input BED file format:
Input files should be split by each chromosome. The format should be in BED which is a tab-delimited text file with 4 columns: chromosome (chr), position (pos), total reads (N), and methylated reads (X) (see below).

        chr	        pos	        N	X
        chr22	21971583	39	26
        chr22	21971603	34	31
        chr22	21971653	26	25
        chr22	21971662	24	24
        chr22	21971701	41	40

## Input Directory:
Store all samples BED files inside one directory. For example: `tests/DSS_chr22_files`

## Input CpG island:
For `hg38`, `cpgIslandExt` table was extracted from UCSC and used [BEDOPS](http://bedops.readthedocs.io/en/latest/content/reference/file-management/sorting/sort-bed.html) `sort-bed` for BED file.
Command line adapted from [biostars page](https://www.biostars.org/p/236141/). 
```
wget -qO- http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cpgIslandExt.txt.gz \
   | gunzip -c \
   | awk 'BEGIN{ OFS="\t"; }{ print $2, $3, $4, $5$6, substr($0, index($0, $7)); }' \
   | sort-bed - \
   > cpgIslandExt.hg38.bed
```
### Example cpgIslandExt.hg38.bed:
```
chr22	48500563	48500779	CpG:17	216	17	134	15.7	62	0.82
chr22	48560078	48560294	CpG:15	216	15	139	13.9	64.4	0.68
chr22	48575045	48577135	CpG:290	2090	290	1549	27.8	74.1	1.01
chr22	48581364	48581571	CpG:16	207	16	128	15.5	61.8	0.84
chr22	48623105	48623505	CpG:47	400	47	280	23.5	70	1
```

### PMDfinder workflow plot:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_workflow.png" alt="PMDfinder workflow plot" width="640" height="1300"></div>

### Example output:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_output.png" alt="PMDfinder output plot" width="2200" height="500"></div>

Each dot represents the percent methylation level of an individual CpG site. The red line on the top represent the identification of PMD. The red line on the bottom represent the identification of Non-PMD.

### Example output_meth BED:
        chr	        pos	        meth_ratio	PMD_predict
        chr22	49175149	0.5735586481113321	PMD
        chr22	49175157	0.3700707785642063	PMD
        chr22	49175225	0.7020905923344948	PMD
        chr22	49175246	0.6876404494382022	PMD
        chr22	49175265	0.4755784061696658	PMD

### Example GRanges BED:
        chr	        start	        end	        status
        chr22	50169395	50171197	CpG_Island
        chr22	50171248	50173818	PMD
        chr22	50173823	50176803	Non-PMD
        chr22	50176850	50179470	CpG_Island
        chr22	50179513	50184700	Non-PMD

## UC Davis Tristan Server Example
Install TensorFlow and activate it.
```
conda create -n tf-gpu tensorflow-gpu
conda activate tf-gpu
```

## Version
v0.3.0  

## Dataset
- Zhu, Yihui, J. Antonio Gomez, Benjamin I. Laufer, Charles E. Mordaunt, Julia S. Mouat, Daniela C. Soto, Megan Y. Dennis et al. "Placental methylome reveals a 22q13. 33 brain regulatory gene locus associated with autism." Genome biology 23, no. 1 (2022): 1-32. **doi:** https://doi.org/10.1186/s13059-022-02613-1
- Datasets supporting the conclusions are available in the Gene Expression Omnibus repository (GEO): https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178206
