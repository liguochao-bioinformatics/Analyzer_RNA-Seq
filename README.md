# Analyzer_RNA-Seq
# Author: Li Guochao
# e-mail: stevelee0201@163.com
# Version of README: 0.1



1. Introduction
    Analyzer_RNA-Seq is designed for reducing person's repeated work during analysis of RNA-Seq data. It is an integration of some popular exsiting softwares. Meanwhile, some scripts written in Python and R are contained as well. Given raw data of RNA-Seq in fastq format, it analyzes automatically by tophat, cufflinks, Python, R, etc. The output contains the regular readable results of RNA-Seq analysis (eg. summary, density plot, scatter plot, volcano plot, results of GO and KEGG enrichment, etc.) and some necessary results for use in downstream personanlized analysis (eg. the list of genes with different expressions filtered by p or q value).



2. Preparation

    (1) System
        So far, Analyzer_RNA-Seq has only been tested to run sucessfully on Linux (RedHat, other Linux has not been tested). It might be available on Windows and Mac, or not.

    (2) Requirement
        Analyzer_RNA-Seq need many softwares and R packages installed. After once test, with these softwares with specific version and R packages, Analyzer_RNA-Seq works normally:

        Python      v2.7.8
        Tophat      v2.0.9 (note: Tophat only works normally with lower version of samtools, such as v0.1.19. Higher version of samtools make Tophat CANNOT work, such as v1.2)
        Cufflinks   v2.0.2
        R           v3.1.1
        R packages: org.Hs.eg.db, GSEABase, GOstats, Category, pathview, cummeRbund and the packages it relies. 
                    PS: You can use these two cmmands to install all of them:
                    source("http://bioconductor.org/biocLite.R")
                    biocLite(c("org.Hs.eg.db", "GSEABase", "GOstats", "Category", "pathview", "cummeRbund"))

        Given the softwares noted above with other versions, Analyzer_RNA-Seq might work normally as well. However, I can not promise. Thus more tests should be done in the future.



3. Run Analyzer_RNA-Seq

    (1) Download Analyzer_RNA-Seq on your computer.

    (2) In shell, run these commands:
        cd /path_to_Analyzer_RNA-Seq 
        chmod +x Analyzer_RNA-Seq

    (3) Analyzer_RNA-Seq need the ABSOLUTE PATH of raw RNA-Seq data in fastq format and ABSOLUTE PATH of output directory. Therefore, there is no need to put Analyzer_RNA-Seq and your RNA-Seq data in the same directory. A better way is put it in environment PATH.

    (4) In shell, run this command to see help of Analyzer_RNA-Seq : 
        /path_to_Analyzer_RNA/Analyzer_RNA-Seq --help 
        You will see the help information like this:
        
        Usage: Analyzer_RNA-Seq.py [-p] path_name [-g] Reference.gtf [-a] Reference.fa [-i] input_fastq_files [-t] num_of_threads

        Options:
        --version             show program's version number and exit
        -h, --help            show this help message and exit
        -p PATH, --path=PATH  The path of project. Absolute path is needed. (eg:
                                /leofs/sunyl_group/ligch/YuHui/analysis/RNA-
                                Seq/mapping)
        -g REFERENCE_GTF, --gtf=REFERENCE_GTF
                                The annotation GTF file of reference. Absolute path is
                                needed. (eg:
                                /leofs/sunyl_group/yaolsh/ref/hg19/hg.gtf)
        -a REFERENCE_FA, --fa=REFERENCE_FA
                                The reference name in .fa format. Absolute path is
                                needed. (eg: /leofs/sunyl_group/yaolsh/ref/hg19/hg.fa)
        -i INPUT_GROUPS_AND_FILENAMES, --input=INPUT_GROUPS_AND_FILENAMES, --fq=INPUT_GROUPS_AND_FILENAMES
                                The names of fastq for analysis. The format is
                                "control,fastq1,fastq2:treat,fastq1,fastq2". Absolute
                                path is needed. (eg:
                                231-2,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-
                                2/231-2_1.fastq,/leofs/sunyl_group/ligch/YuHui/data
                                /RNA-Seq/231-2/231-2_2.fastq:231-1,/leofs/sunyl_group/
                                ligch/YuHui/data/RNA-Seq/231-1/231-1_1.fastq,/leofs/su
                                nyl_group/ligch/YuHui/data/RNA-
                                Seq/231-1/231-1_2.fastq)
        -t THREAD, --thread=THREAD
                                The number of threads, default 8.

    (5) An example of running Analyzer_RNA-Seq is shown below:
        /Analyzer_RNA-Seq \
            -p /leofs/sunyl_group/ligch/Test/tophat+cufflinks \
            -g /leofs/sunyl_group/yaolsh/ref/hg19/hg.gtf \
            -a /leofs/sunyl_group/yaolsh/ref/hg19/hg.fa \
            -i 231-2,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_2.fastq:231-1,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_2.fastq

    (6) So far, it will only run tophat and cufflinks automatically with two RNA-Seq samples, which are sequnced by pair-end and no replicate is given. More functions (eg. various plots, GO and KEGG enrichment, etc.) are comming soon.
