#!/usr/bin/env python
# -*- coding: utf-8 -*-
__metaclass__ = type
# Author: Li Guochao

import os
from time import strftime as time
from optparse import OptionParser

parser = OptionParser(usage="%prog [-p] path_name [-g] Reference.gtf [-a] Reference.fa [-i] input_fastq_files [-t] num_of_threads", version="%prog 1.0.0")

parser.add_option("-p", 
                  "--path", 
                  dest = "path", 
                  type = "string",
                  help = "The path of project. Absolute path is needed. (eg: /leofs/sunyl_group/ligch/YuHui/analysis/RNA-Seq/mapping)") 

parser.add_option("-g", 
                  "--gtf",
                  dest = "reference_gtf", 
                  type = "string",
                  help = "The annotation GTF file of reference. Absolute path is needed. (eg: /leofs/sunyl_group/yaolsh/ref/hg19/hg.gtf)") 

parser.add_option("-a", 
                  "--fa",
                  dest = "reference_fa", 
                  type = "string",
                  help = "The reference name in .fa format. Absolute path is needed. (eg: /leofs/sunyl_group/yaolsh/ref/hg19/hg.fa)") 

parser.add_option("-i", 
                  "--input",
                  "--fq",
                  dest = "input_groups_and_filenames", 
                  type = "string",
                  help = "The names of fastq for analysis. The format is \"control,fastq1,fastq2:treat,fastq1,fastq2\". Absolute path is needed. (eg: 231-2,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-2/231-2_2.fastq:231-1,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_1.fastq,/leofs/sunyl_group/ligch/YuHui/data/RNA-Seq/231-1/231-1_2.fastq)") 

parser.add_option("-t", 
                  "--thread",
                  dest = "thread", 
                  type = "int",
                  default = 8,
                  help = "The number of threads, default 8.") 

(options, args) = parser.parse_args() 


### Preparation
if options.path and options.reference_gtf and options.reference_fa and options.input_groups_and_filenames and options.thread:

    path            = options.path
    gtf             = options.reference_gtf
    fa              = options.reference_fa
    groups_and_fqs  = options.input_groups_and_filenames.split(":")
    thread          = options.thread
    
    group_1         = groups_and_fqs[0].split(",")[0]
    fq_group_1      = groups_and_fqs[0].split(",")[1:]
    group_2         = groups_and_fqs[1].split(",")[0]
    fq_group_2      = groups_and_fqs[1].split(",")[1:]

    print 
    print "The path of project is: " + path + "\n"
    print "Tophat and cufflinks start at " + time('%Y-%m-%d %H:%M:%S') + "."

    os.chdir(path)

    run_time = open("Run_time", "w")

### Step 1. tophat
    def tophat(path, gtf, fa, group, fq_1, fq_2, thread):
        tophat_group_path = os.path.join(path, "tophat", group)
        os.mkdir(tophat_group_path)
        tophat_cmdline = """tophat \
            -p %(thread)d \
            -G %(gtf)s \
            -o %(tophat_group_path)s \
            %(fa)s \
            %(fq_1)s \
            %(fq_2)s
        """ % (
                {
                    "thread"            : thread,
                    "gtf"               : gtf,
                    "tophat_group_path" : tophat_group_path,
                    "fa"                : fa,
                    "fq_1"              : fq_1,
                    "fq_2"              : fq_2,
                }
              )
        os.system(tophat_cmdline)

    print
    print "=" * 40 + " Tophat starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n"
    run_time.write("=" * 40 + " Tophat starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n")
    os.mkdir( os.path.join(path, "tophat") )
    tophat(path, gtf, fa, group_1, fq_group_1[0], fq_group_1[1], thread)
    tophat(path, gtf, fa, group_2, fq_group_2[0], fq_group_2[1], thread)

### Step 2. cufflinks
    def cufflinks(path, group, thread):
        cufflinks_group_path =  os.path.join(path, "cufflinks", "cufflinks", group)
        os.mkdir(cufflinks_group_path)
        cufflinks_cmdline = """cufflinks \
            -p %(thread)d \
            -o %(cufflinks_group_path)s \
            %(tophat_bam_path)s
        """ % (
                {
                    "thread"                : thread,
                    "cufflinks_group_path"  : cufflinks_group_path,
                    "tophat_bam_path"       : os.path.join(path, "tophat", group, "accepted_hits.bam"),
                }
              )
        os.system(cufflinks_cmdline)

    print
    print "=" * 40 + " Cufflinks starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n"
    run_time.write("=" * 40 + " Cufflinks starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n")
    os.mkdir( os.path.join(path, "cufflinks") )
    os.mkdir( os.path.join(path, "cufflinks", "cufflinks") )
    cufflinks(path, group_1, thread)
    cufflinks(path, group_2, thread)

### Step 3. cuffmerge
    def cuffmerge(cuffmerge_output_path, gtf, fa, thread, assemblies):
        cuffmerge_cmdline = """cuffmerge \
            -o %(cuffmerge_output_path)s \
            -g %(gtf)s \
            -s %(fa)s \
            -p %(thread)d \
            %(assemblies.txt)s
        """ % (
                {
                    "cuffmerge_output_path" : cuffmerge_output_path,
                    "gtf"                   : gtf,
                    "fa"                    : fa,
                    "thread"                : thread,
                    "assemblies.txt"        : assemblies,
                }
              )
        os.system(cuffmerge_cmdline)

    print
    print "=" * 40 + " Cuffmerge starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n"
    run_time.write("=" * 40 + " Cuffmerge starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n")
    cuffmerge_output_path = os.path.join(path, "cufflinks", "cuffmerge") 
    os.mkdir(cuffmerge_output_path)
    with open(os.path.join(cuffmerge_output_path, "assemblies.txt"), "w") as cuffmerge_assemblies:
        out_line_1 = os.path.join(path, "cufflinks", "cufflinks", group_1, "transcripts.gtf")
        out_line_2 = os.path.join(path, "cufflinks", "cufflinks", group_2, "transcripts.gtf")
        cuffmerge_assemblies.write(out_line_1 + "\n" + out_line_2 + "\n")
    assemblies = os.path.join(cuffmerge_output_path, "assemblies.txt")
    cuffmerge(cuffmerge_output_path, gtf, fa, thread, assemblies)

### Step 4. cuffdiff
    def cuffdiff(cuffdiff_output_path, thread, merged_gtf, tophat_group_1_bam, tophat_group_2_bam):
        cuffdiff_cmdline = """cuffdiff \
            -o %(cuffdiff_output_path)s \
            -b %(fa)s \
            -p %(thread)d \
            -L N,T \
            -u %(merged_gtf)s \
            %(tophat_group_1_bam)s \
            %(tophat_group_2_bam)s \
        """ % (
                {
                    "cuffdiff_output_path"  : cuffdiff_output_path,
                    "fa"                    : fa,
                    "thread"                : thread,
                    "merged_gtf"            : merged_gtf,
                    "tophat_group_1_bam"    : tophat_group_1_bam,
                    "tophat_group_2_bam"    : tophat_group_2_bam,
                }
              )
        os.system(cuffdiff_cmdline)

    print
    print "=" * 40 + " Cuffdiff starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n"
    run_time.write("=" * 40 + " Cuffdiff starts at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n")
    cuffdiff_output_path =  os.path.join(path, "cufflinks", "cuffdiff")
    os.mkdir(cuffdiff_output_path)
    merged_gtf = os.path.join(cuffmerge_output_path, "merged.gtf")
    tophat_group_1_bam = os.path.join(path, "tophat", group_1, "accepted_hits.bam")
    tophat_group_2_bam = os.path.join(path, "tophat", group_2, "accepted_hits.bam")
    cuffdiff(cuffdiff_output_path, thread, merged_gtf, tophat_group_1_bam, tophat_group_2_bam)

    run_time.write("=" * 40 + " Analyzer ends at " + time('%Y-%m-%d %H:%M:%S') + " " + "=" * 40 + ".\n")
else:
    print "Error: There is not enough parameters!"
