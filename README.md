# PMDfinder

#### A pipeline to identify partially methylation domains from whole-genome bisulfite sequencing data

By Yihui Zhu

## Running PMDfinder:
First prepare WGBS data in DSS file format.

## DSS file format:
Input files should be split by each sample and each chromosome. The format should be in DSS which is a tab-delimited text file with 4 columns: chromosome (chr), position (pos), total reads (N), and methylated reads (X) (see below).

        chr	        pos	N	X
        chr21	5013971	168	70
        chr21	5014046	10	5
        chr21	5014056	60	5
        chr21	5014082	190	10
        chr21	5014097	50	6

### PMDfinder workflow plot:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_workflow.png" alt="PMDfinder workflow plot" width="400" height="525"></div>

### Example output:
<div align="center"><img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_output.png" alt="PMDfinder output plot" width="600" height="400"></div>

Each dot represents the percent methylation level of an individual CpG site. The red line represent the identification of PMD. 
