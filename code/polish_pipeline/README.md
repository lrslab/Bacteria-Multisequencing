The latest one is available at https://github.com/lrslab/Hammerhead/tree/main/Duplex_polishing.

## STEP1. Find the potential modification sites

```shell
minimap -ax map-ont -t ${threads} ${assembler} ${simplex_fastq} > test.sam

samtools view -F 4 -bS -@ ${threads} test.sam > test.bam
samtools sort -@ ${threads}  test.bam > test.sort.bam

samtools mpileup -q 30 --no-output-ins --no-output-ins --no-output-del --no-output-del --no-output-ends test.sort.bam > test.mpileup.txt 

python site_substitution.py -in test.mpileup.txt -cut ${cutoff} -out test.dir_site.txt
grep -v Chr test.dir_site.txt | awk '{print $1 "\t" $2-1 "\t" $2}' > test.dir_site.bed
```



## STEP2. Polish sites using duplex reads

```shell
minimap -ax map-ont -t ${threads} ${assembler} ${duplex_fastq} > duplex.sam

samtools view -F 4 -bS -@ ${threads} duplex.sam > duplex.bam
samtools sort -@ ${threads}  duplex.bam > duplex.sort.bam

samtools mpileup -f ${assembler} -l test.dir_site.bed -q 30 --no-output-ins --no-output-ins --no-output-del --no-output-del --no-output-ends duplex.sort.bam > duplex.mpileup.txt

python count.py -in duplex.mpileup.txt > results.txt
```

**The demo for results:**

```shell
#chr	pos	base	N_A	N_T	N_G	N_C	P_A	P_T	P_G	P_C	polish_base
contig_4	29153	T	0	1	0	13	0.0	0.07142857142857142	0.0	0.9285714285714286	C
contig_6	155419	A	1	0	20	0	0.047619047619047616	0.0	0.9523809523809523	0.0	G
contig_7	60990	A	4	0	24	0	0.14285714285714285	0.0	0.8571428571428571	0.0	G
contig_7	118348	G	25	0	7	0	0.78125	0.0	0.21875	0.0	A
contig_7	123180	C	0	19	0	2	0.0	0.9047619047619048	0.0	0.09523809523809523	T
contig_7	344011	C	0	19	0	4	0.0	0.8260869565217391	0.0	0.17391304347826086	T
```

`chr`, `pos`, `base`  are the base type and position in the reference of potential modification sites.

`N_A`, `N_T`, `N_G`, `N_C` are the number of reads which were mapped as A, T, G, and C base at potential modification sites.

`P_A`, `P_T`, `P_G`, `P_C` are the proportion of reads which were mapped as A, T, G, and C base at potential modification sites.

`polish_base`  is the base after polished. 

**Note**: The resulting sites are just selected by the errors proportion. If you believe that any sites are correct, please manually remove them. The site information in **red** indicates an ambiguous site that is difficult to identify as an error.



## STEP3. Replace any erroneous bases in the assembler with their correct counterparts

```shell
cat results.txt | grep -v pos | awk '{if ($12 == "C") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > C.bed
cat results.txt | grep -v pos | awk '{if ($12 == "G") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > G.bed
cat results.txt | grep -v pos | awk '{if ($12 == "T") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > T.bed
cat results.txt | grep -v pos | awk '{if ($12 == "A") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > A.bed

bedtools maskfasta -fi ${assembler} -bed A.bed -mc A -fo tmp1.fa
bedtools maskfasta -fi tmp1.fa -bed T.bed -mc T -fo tmp2.fa
bedtools maskfasta -fi tmp2.fa -bed G.bed -mc G -fo tmp3.fa
bedtools maskfasta -fi tmp3.fa -bed C.bed -mc C -fo final.fa

# remove the temporary FASTA files
rm tmp1.fa tmp2.fa tmp3.fa
```

The **final.fa**  is the final polished genome assembler.

