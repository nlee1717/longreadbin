# longreadbin

[ PROJECT OUTLINE ]

[ PIPELINE ]
1. Download data from: NIH SSR
2. Process fastq/fasta files (change @ to >)
3. Run medaka on long read contigs (metaFlye, .fasta) with raw long read (ONT, .fastq) > sample_medaka.fasta
4. Run NextPolish on sample_medaka.fasata with raw short read (ILLUMINA, .fastq) > sample_polished.fasta
5. Generate NG50 plot: compare polished.fasta, LR assembly (Flye), and SR assembly (MegaHit)
6. Merge SR assembly and polished assembly > merged.fasta
7. Align merged.fasta all_vs_all pairwise with minimap2 (align every sequence with every other) > .paf 
8. Analysis on paf files *** > clusters.txt
9. Remove the sr contigs that aligned to lr contigs, from the merged.fasta > clustered_assembly.fasta 
10. Align SR to clustered_assembly.fasta (bowtie) > .BAM file > sort
11. Run genomeCoverageBed to get abundance estimate (samtools view -b <BAM> | genomeCoverageBed -ibam stdin -g hg18.genome)
12. Run metabat2 with clustered_assembly.fasta and BAM file > depth.txt & cluster.fa