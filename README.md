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
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_workflow.png" alt="PMDfinder workflow plot" width="400" height="600"></div>

### Example output:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_output.png" alt="PMDfinder output plot" width="1500" height="500"></div>

Each dot represents the percent methylation level of an individual CpG site. The red line on the top represent the identification of PMD. The red line on the bottom represent the identification of Non-PMD.

### Example output_meth BED:
        chr	        pos	        N	X	PMD_predict
        chr22	21971583	39	26	Non-PMD
        chr22	21971603	34	31	Non-PMD
        chr22	21971653	26	25	Non-PMD
        chr22	21971662	24	24	Non-PMD
        chr22	21971701	41	40	Non-PMD

### Example GRanges BED:
        chr	        start	        end	        status
        chr22	36146264	36188467	Non-PMD
        chr22	36188555	36701973	PMD
        chr22	36701993	36709838	Non-PMD
        chr22	36709840	36729403	PMD
        chr22	36729422	36729422	Non-PMD
        chr22	36729431	36751503	PMD

## Version
v0.2.0  
