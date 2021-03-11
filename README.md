# PMDfinder

#### A pipeline to identify partially methylation domains from whole-genome bisulfite sequencing data

By Yihui Zhu

## Running PMDfinder:
First prepare WGBS data in DSS file format.

## DSS file format:
Input files should be split by each sample and each chromosome. The format should be in DSS which is a tab-delimited text file with 4 columns: chromosome (chr), position (pos), total reads (N), and methylated reads (X) (see below).
        
        chr	        pos	N	X
        chr21	5013971	1	1
        chr21	5014046	1	1
        chr21	5014056	1	1
        chr21	5014082	1	1
        chr21	5014097	1	0

### PMDfinder workflow plot
<img src="https://github.com/Yihui-Zhu/PMDfinder/blob/main/Figures/PMDfinder_workflow.png" alt="PMDfinder workflow plot" width="400" height="500">
