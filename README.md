# Analyzer_RNA-Seq
# Author: Li Guochao
# e-mail: stevelee0201@163.com
# Version of README: 0.8



1. Introduction

    Analyzer_RNA-Seq is designed for reducing person's repeated work during analysis of RNA-Seq data. It is an integration of some popular exsiting softwares. Meanwhile, some scripts written in Python and R are contained as well. Given raw data of RNA-Seq in fastq format, it analyzes automatically by tophat, cufflinks, Python, R, etc. The output contains the regular readable results of RNA-Seq analysis (eg. summary, density plot, scatter plot, volcano plot, results of GO and KEGG enrichment, etc.) and some necessary results for use in downstream personanlized analysis (eg. the list of genes with different expressions filtered by p or q value).



2. Preparation

    (1) System: So far, Analyzer_RNA-Seq has only been tested to run sucessfully on Linux (RedHat, other Linux has not been tested). It might be available on Windows and Mac, or not.

    (2) Requirements: Analyzer_RNA-Seq needs many softwares and R packages to be installed. After once test, with the softwares with specific version and R packages which are shown below, Analyzer_RNA-Seq runs normally. Given the other versions, Analyzer_RNA-Seq might run normally as well. However, I can not give a promise. Thus various systems and more versions of softwares will be tested in the future.

        Python          v2.7.8
        Tophat          v2.0.9 (note: Tophat only works normally with lower version of samtools, such as v0.1.19. Higher version of samtools make Tophat CANNOT work, such as v1.2)
        Cufflinks       v2.0.2
        R               v3.1.1
        R packages      ggplot2, pheatmap, org.Hs.eg.db, GSEABase, GOstats, Category, pathview, cummeRbund and the packages they rely on. 
        piplineforQC or another software for QC.

    (3) You can use these three cmmands in R to install all of required R packages:

        > install.packages("ggplot2")
        > source("http://bioconductor.org/biocLite.R")
        > biocLite(c("org.Hs.eg.db", "pheatmap", "GSEABase", "GOstats", "Category", "pathview", "cummeRbund"))



3. Run Analyzer_RNA-Seq

    (1) Download Analyzer_RNA-Seq on your computer.

    (2) In shell, run this commands:

        $ chmod +x /path_to_Analyzer_RNA-Seq/Analyzer_RNA-Seq

    (3) Analyzer_RNA-Seq need the ABSOLUTE PATH of raw RNA-Seq data in fastq format and ABSOLUTE PATH of output directory. Therefore, there is no need to put Analyzer_RNA-Seq and your RNA-Seq data in the same directory. A better way is put it in environment PATH.

    (4) In shell, run this command to see help document of Analyzer_RNA-Seq : 
     
        $ /path_to_Analyzer_RNA/Analyzer_RNA-Seq --help 
        
        Usage: Analyzer_RNA-Seq [-o] output_path [-g] Reference.gtf [-a] Reference.fa [-i] control,fastq1,fastq2:treat,fastq1,fastq2 [-t] num_of_threads [-e] run enrichment analysis on the Internet or not (default is not)

        Options:
            --version             show program's version number and exit
            -h, --help            show this help message and exit
            -o OUTPUT_PATH, --output_path=OUTPUT_PATH
                                    The path of output. (eg:
                                    /leofs/sunyl_group/ligch/YuHui/analysis/RNA-Seq or ./)
            -g REFERENCE_GTF, --gtf=REFERENCE_GTF
                                    The annotation GTF file of reference. (eg:
                                    /leofs/sunyl_group/yaolsh/ref/hg19/hg.gtf or ./hg.gtf)
            -a REFERENCE_FA, --fa=REFERENCE_FA
                                    The reference name in .fa format. (eg:
                                    /leofs/sunyl_group/yaolsh/ref/hg19/hg.fa or ./hg.fa)
            -i INPUT_GROUPS_AND_FILENAMES, --input=INPUT_GROUPS_AND_FILENAMES, --fq=INPUT_GROUPS_AND_FILENAMES
                                    The names of fastq files for analysis. (eg:
                                    231-2,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-
                                    2/231-2_1.fastq,/leofs/sunyl_group/ligch/YuHui/data
                                    /RNA-Seq/231-2/231-2_2.fastq:231-1,/leofs/sunyl_group/
                                    ligch/YuHui/data/RNA-Seq/231-1/231-1_1.fastq,/leofs/su
                                    nyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_2.fastq
                                    or NCSC,./231-2/231-2_1.fastq,./231-2/231-2_1.fastq:CS
                                    C,./231-1/231-1_1.fastq,./231-1/231-1_2.fastq)
            -t THREAD, --thread=THREAD
                                    The number of threads, default is 8.
            -e, --enrichment      Tell Analyzer_RNA-Seq to run GO and KEGG enrichment
                                    analysis on the Internet or not. Default is False. If
                                    '-e' is given, this step will run.

    (5) An example of running Analyzer_RNA-Seq in shell is shown below:

        $ /path_to_Analyzer_RNA-Seq/Analyzer_RNA-Seq \
            -p /leofs/sunyl_group/ligch/Test/tophat+cufflinks \
            -g /leofs/sunyl_group/yaolsh/ref/hg19/hg.gtf \
            -a /leofs/sunyl_group/yaolsh/ref/hg19/hg.fa \
            -i 231-2,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_2.fastq:231-1,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_2.fastq



4. Analyzer_RNA-Seq's functions:

    (1) Analyzer_RNA-Seq runs tophat and cufflinks automatically with two RNA-Seq samples, which are sequnced by pair-end and no replicate is given. 
    
    (2) A summary of result of cuffdiff, raw information of genes with different expression levels (generated from /cufflinks/cuffdiff/gene_exp.diff) by p or q value are outputed in text format.
    
    (3) Visulization: A density plot, a scatter plot and a volcano plot are outputed in tif format. Then various heatmaps are drawn by different methods of clustering and measurements of distance. You can choose one according to your own biological problem. 
    
    (4) GO and KEGG enrichment analysis are done by R, whose results are outputed in text format (for GO) and png format (for KEGG), respectively. 
    
    (5) More functions (eg. saturation analysis) are comming soon.
