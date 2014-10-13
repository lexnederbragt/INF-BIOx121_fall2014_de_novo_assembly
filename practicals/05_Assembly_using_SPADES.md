#Assembly using SPADES

Spades was written as an assembly program for bacterial genomes, from regular, as well as from whole-genome amplified samples. It performed very well in the GAGE-B competition, see [http://ccb.jhu.edu/gage_b/](http://ccb.jhu.edu/gage_b/). SPAdes also works well, sometimes even best, when given high-coverage datasets.

Before assembly, SPADES will error-correct the reads.

###Using SPADES

Spades can be used with paired end and mate pair data:

* The `--careful` flag is used to reduce the number of mismatches and short indels. 
* For each read file, a flag is used to indicate whether it is from a paired end (`--pe`) or mate (`--mp`) pair dataset, followed by a number for the dataset, and a number for read1 or read2. For example: `--pe1-1` and `--pe1-2` indicate pared end data set 1, read1 and read2, respectively.
* Similarly, use `--mp-1-1` and `--mp1-2` for the mate pair files. 
* Spades assumes mate pairs are in the orientation as they are in the original files coming from the Illumina instrument: <-- and --> ('outie' orientation, or 'rf' for reverse-forward). Our reads are in the --> and <-- ('innie', 'fr' for forward-reverse) orientation, so we add the `--mp1-fr` flag to let SPADES know about this
* both for PacBio or MinION (Oxford Nanopore) reads, the `--pacbio` flag is used
  
Other parameters:

* `-t` number of threads (CPUs) to use for calculations
* `--memory` maximum memory usage in Gb
* `-k` k-mers to use (this gives room for experimenting!)
* `-o` name of the output folder


####Assembly options

* Most interesting would be Illumina MiSeq reads combined with Oxford Nanopore MinION reads
* You could also try MiSeq paired end reads (more than we used for velvet) with the Mate Pair reads. 


####Setting up the assembly

To enable SPAdes, run:

```
module load spades
```

First, create a new folder called `/usit/abel/u1/YOUR_USERNAME/assembly/spades` and `cd` into it.  
We will save the output from the command using `>spades.out` in a file to be able to follow progress. `2>&1` makes sure any error-messages are written to the same file.
Run the assembly as follows:

**NOTE** the assembly will take several hours, so use the `screen` command! See [https://wiki.uio.no/projects/clsi/index.php/Tip:using_screen](https://wiki.uio.no/projects/clsi/index.php/Tip:using_screen)

**NOTE** we use different files for the paired end reads


**For paired end Illumina with MinION data:**

```
spades.py -t 2 -k 21,33,55,77 --careful --memory 33 \
--pe1-1 /data/assembly/MiSeq_Ecoli_MG1655_110721_R1.fastq \
--pe1-2 /data/assembly/MiSeq_Ecoli_MG1655_110721_R2.fastq \
--pacbio /data/assembly/Ecoli_R7_MinION.fasta \
-o ASM_NAME >spades.out 2>&1
```

**For paired end Illumina with Illumina mate Pairs:**

```
spades.py -t 2 -k 21,33,55,77 --careful --memory 33 \
--pe1-1 /data/assembly/MiSeq_Ecoli_MG1655_110721_R1.fastq \
--pe1-2 /data/assembly/MiSeq_Ecoli_MG1655_110721_R2.fastq \
--mp1-1 /data/assembly/Nextera_MP_R1_50x.fastq \
--mp1-2 /data/assembly/Nextera_MP_R2_50x.fastq \
--mp1-fr -o ASM_NAME >spades2.out 2>&1
```

If the assembly is running in a 'screen', you can follow the output by checking the `out` file.  

**TIP**: use this command to track the output as it is added to the file. Use ctrl-c to cancel.

```
tail -f spades.out
```

####SPADES output
* error-corrected reads
* contigs for each individual k-mer assembly
* final `contigs.fasta` and `scaffolds.fasta` (which are identical)

You can have a look at the lengths of the largest sequence(s) with

```
fasta_length contigs.fasta |sort -nr |less
```


####Re-using error-corrected reads

Once you have run SPADES, you will have files with the error-corrected reads in `spades_folder/corrected/`. There will be one file for each input file, and one additional one for unpaired reads (where during correction, one of the pairs was removed from the dataset). Instead of running the full SPADES pipeline for your next assembly, you could add the error-corrected reads from the previous assembly. This will save time by skipping the error-correction step. I suggest to not include the files with unpaired reads.

Error-corrected read files are compressed, but SPADES will accept them as such (no need to uncompress).

Changes to the command line when using error-corrected reads:

* point to the error-corrected read files instead of the raw read files
* add the `--only-assembler` flag to skip correction

###Next steps
As for the previous assemblies, you could map reads back to the assembly, run reapr and visualise in the browser.

**NOTE** please log your results in the spreadsheet at http://bit.ly/INFBIO2.
