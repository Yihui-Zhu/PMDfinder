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
>>> findPMD("tests/DSS_chr22_files", "tests/output_meth.bed", "tests/output_GRanges.bed", 0.9, 20)
```

## Function
`findPMD` is the main function of the PMDfinder package with methylome as input with output as PMD location.
```
findPMD(filepath, outputpath1, outputpath2, percentile, cutoff)
```
- `directory`: input BED files directory path.
- `outputpath1`: the output bed file path.
- `outputpath2`: the output grange file path.
- `percentile`: Percent of samples per CpG coverage, values range from 0 to 1.
- `cutoff`: minimum number of reads per CpG site

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

### PMDfinder workflow plot:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_workflow.png" alt="PMDfinder workflow plot" width="640" height="1200"></div>

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
        chr22	47151743	49735986	PMD
        chr22	49736040	49971468	Non-PMD
        chr22	49971477	50167316	PMD
        chr22	50167380	50290338	Non-PMD
        chr22	50290345	50296272	PMD


## Version
v0.2.0  
