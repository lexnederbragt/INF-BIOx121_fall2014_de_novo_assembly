#Mapping reads to an assembly and visualising the results

We will use `bwa` for mapping. this is the same program you used for the variant calling module.

####Set up the environment
Load the following modules:

```
module load samtools
module load bwa
module load python2
```

####Indexing the assembly

Your new assembly now becomes the 'reference' for `bwa`. `bwa` needs an index of the sequences to make mapping go faster. For large genomes such as the human genome, this takes a long time. For the small bacterial genome we work with here this is very fast.

Move (using `cd`) to the folder with your final assembled sequenced, e.g. `contigs.fa` for velvet.  

Index the fasta file with:

```
bwa index -a bwtsw ASSEMBLY.FASTA
```

Replace `ASSEMBLY.FASTA` with the name of your fasta file. Run `ls` to check the results, you should see a couple of new files.


####Mapping paired end reads

Mapping the reads using `bwa mem` yields SAM output. Instead of saving this output to disk, we will immediately convert it to a sorted (binary) BAM file by piping into the `samtools`program. 'Sorted' here means that the alignments of the mapped reads are in the order of the reference sequences, rather than random. Finally, we will generate an index of the sorted BAM file for faster searching later on.

First, create a new folder *in the same folder as the `ASSEMBLY.FASTA` file*  and `cd` into it:

```
mkdir bwa
cd bwa
```
Then do the mapping:

```
bwa mem -t 2 ../ASSEMBLY.FASTA \
/data/assembly/MiSeq_Ecoli_MG1655_50x_R1.fastq \
/data/assembly/MiSeq_Ecoli_MG1655_50x_R2.fastq \
| samtools view -buS - | samtools sort - map_pe.sorted
```

Generate an index of the BAM file:

```
samtools index map_pe.sorted.bam
```

Explanation of some of the parameters:

* `../` means 'look in the folder one level up', i.e. where the fasta file is
* `-t 2`tells `bwa mem` to use 2 threads (cpus)
* `-buS`tells `samtools view` that the input is in SAM format (`S`) and to output uncompressed (`u`) BAM format (`b`).
* the `-` for both `samtools` commands indicate that instead of using a file as input, the input comes from a pipe (technically, from 'standard in', or 'STDIN').
* `map_pe.sorted` tells `samtools view` to call the outputfile `map_pe.sorted.bam`

If you would like to have a look at the alignments in the BAM file (which is in binary format), use `samtools view`again:

```
samtools view map_pe.sorted.bam |less
```

####Mapping mate pairs
Repeat the `bwa mem` and `samtools` commands above, but:

* use the mate pair reads `Nextera_MP_R1_50x.fastq` and `Nextera_MP_R2_50x.fastq`
* change the output name to `map_mp.sorted`

####Plotting the insert size distribution
Since we know know where the pairs of reads map, we can obtain he distance between them. That information is stored in the SAM/BAM output in the 9th column, 'TLEN' (observed Template LENgth).

We will use python, and the python modules `pysam` and `R` (through the python `rpy2` module) to plot the distribution of insert sizes for a subset of the alignments. This we will do in another IPython notebook

* Copy the notebook file `/data/assembly/Plot_insertsizes.ipynb` to the folder with the BAM files
* In the terminal, `cd` to the same folder
* Open a new terminal window (log in to the server again) for running the IPython notebook from and in it, `cd` to the folder with the BAM files
* See the instructions for how to start the IPython notebook on the wiki at [https://wiki.uio.no/projects/clsi/index.php/INF-BIOX121_H14_RStudio_IPython](https://wiki.uio.no/projects/clsi/index.php/INF-BIOX121_H14_RStudio_IPython)
* After a little bit, your webbrowser will start with a new tab labelled `IPython dashboard`, and the notebook `Plot_insertsizes` listed
* Click on the notebook name, it will open in a new tab
* Execute the cells as listed.
* For `infile`, use the name of the sorted BAM file for the mapping of the paired end or mate pair reads
* Generate plots for both the paired end mapping *and* the mate pair mapping

**Questions**

* Which insert size distribution is the tightest around the mean?
* Why isn't the mean of the distribution a useful number for the mate pair library?


When you are done with the IPython notebook:

* If you want to save the figures, copy them from the notebook into another program
* Save the notebook
* Close the browser windows
* In the terminal where you started IPython notebook, click ctrl-c and confirm.


####Visualising the assembly in a genome browser
For this part, we will use Integrative Genomics Viewer (IGV), a genome browser developed by the Broad Institute.  Instead of using one of the built-in genomes, we will add the assembly as a new reference genome.

**NOTE** you may need to install IGV first (MAC and Windows users), in that case go through the instructions at [http://www.broadinstitute.org/igv/](http://www.broadinstitute.org/igv/) and install it in your home area on the PC/MAC.

* Download the assembly `fasta` file and the `bam` and `bam.bai` files to the local hard disk of the PC/Mac you are using, see the instructions on the course wiki
* **On the PC** (*NOT* on bioinfcourse.hpc.uio.no) start the IGV program by typing `igv` (Linux), opening the program from the start explorer (Windows), or double clicking on the `igv.command` file (Mac)
* Choose `Genomes --> Load Genome from File…` (**NB** not File --> Load from File...)
* Select the fasta file with your assembly (**NB** the same file as you used for mapping the reads against!)

**Adding the mapped reads**  
Adding tracks to the browser is as simple as uploading a new file:

* Choose `File --> Load from File…`
* Choose the sorted BAM file of the paired end mapping 
* Repeat this for the BAM file of the mate pair mapping 
* You can choose different sequences (contigs/scaffolds) from the drop-down menu at the top. Start browsing (one of) the longest scaffold(s)
* Start browsing!
* Zoom in to see the alignments

**Question:**

* Do you see differences between some of the reads relative to the reference? What are these?
* Is coverage even? Are there gaps in the coverage, or peaks? Where?


####Adding the locations of gaps as another track
It would be convenient to be able to see the location of gaps in the browser. For this purpose run the following command (e.g., in the folder with the `bwa` results). we will use 10 bases as minimum gap length: `-m 10`

```
scaffoldgap2bed.py -i ../<assembly.fasta> -m 10 >gaps.bed
```

This will create a BED file with locations of the gaps. 

* Inspect the BED file
* Add the BED file to the browser (download it first to the PC)
* Drag the track to the top
* Zoom in one gaps and look at the alignments.

**Question:**

* Check for some gaps whether they are spanned by mate pairs? Tip: choose 'view as pairs' for the tracks

####Saving the IGV session
We will get back to this assembly browser, so save your session: `File --> Save Session…`

  