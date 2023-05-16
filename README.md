# longreadbin

## PROJECT OUTLINE

This repository contains the scripts and result files used in running the pipeline for Long Read Binning project. The details of the pipeline is described below.

The dataset for this project was obtained from NCBI SRA under bioproject PRJNA527877. Only samples collected from USA-P1 were used. It contains:
- Raw sequences (in .fastq format): Illumina (short reads), ONT (long reads)
- Assemblies (in .fasta format): Megahit (short reads), Flye (long reads)

## PIPELINE

1. Download data.
Dataset was downloaded from NCBI archive, with specifics mentioned as above. The downloaded files were decompressed using `gzip`, and processed to match the format requirements of software tools used for the rest of the pipeline.

```
gzip -d *.fastq.gz *.fasta.gz
sed -i 's/@/>/g' *.fastq
sed -i 's/@/>/g' *.fasta
```

2. Run Medaka. 
Medaka is a software tool to polish assemblies using raw sequence reads. It performs best when ran on long read assembly with long read sequences. This step is included to improve the quality of the long read assembly before polishing with short reads. Output of medaka is saved as `sample_medaka.fasta`.
```
NPROC=$(nproc)
medaka_consensus -i sample_ONT.fastq -d sample_Flye.fasta -o outdir -t ${NPROC} -m r941_min_high_g303
```
3. Run NextPolish.
NextPolish is another software tool to polish assemblies. It was used on the corrected long read assembly (output by medaka) with the raw short read sequences. Output of NextPolish is saved as sample_polished.fasta.
    1. Prepare sgs.fofn, which is a list of fastq files to be passed onto.
    ```
    ls sample_R1.fq sample_R2.fq > sgs.fofn
    ```
    2. Create an nprun.cfg file. For this step, we followed the tutorial on the NextPolish wiki page and used the default settings. Details can be found [here](https://nextpolish.readthedocs.io/en/latest/TUTORIAL.html).

    ```
    nextPolish nprun.cfg
    ```
4. Generate NG50 plot.
NG50 plotted for 3 different assemblies for comparison: `sample_polished.fasta`, `sample_Flye.fasta`, and `sample_Megahit.fasta`.

5. Merge the assemblies.
Simply concatenate the short read contigs to the polished contigs.

6. Align `merged.fasta` all-vs-all pairwise with `minimap2` (align every sequence with every other).
Before binning the polished contigs, any contigs that have high similarity in genetic contents need to be identified and deduplicated. 
    1. Find the overlaps of genetic contents between the short read contigs (src) and long read contigs (lrc) by running an all-vs-all pairwise alignment on the merged `contig.fasta` file. Minimap2 was used to perform the alignment, which outputs a `.paf` file containing the resulting information.
    ```
    minimap2 -aX merged.fasta merged.fasta > aligned.sam
    ```
    2. Extract the cluster information from the `.paf` file (automatically generated). From the list of clusters, we can obtain a list of src that aligned to lrc (i.e., duplicates), which can be safely removed from the `merged.fasta` file.

7. Align the short read sequences to the final assembly.
Finally, the short reads are aligned to the deduplicated polished assembly. Bowtie2 was used for this step. The output BAM file was sorted using samtools before next step.

8. Binning.
The finalized assembly file and sorted BAM file are used to run MetaBAT 2, a software tool to cluster metagenomic data into taxonomic bins. 
