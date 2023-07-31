## STEP1. find the potential modification sites

```shell
minimap -ax map-ont -t ${threads} ${assembler} ${simplex_fastq} > test.sam

samtools view -F 4 -bS -@ ${threads} test.sam > test.bam
samtools sort -@ ${threads}  test.bam > test.sort.bam

samtools mpileup -q 30 --no-output-ins --no-output-ins --no-output-del --no-output-del --no-output-ends test.sort.bam > test.mpileup.txt 

python site_substitution.py -in test.mpileup.txt -cut ${cutoff} -out test.dir_site.txt
grep -v Chr test.dir_site.txt | awk '{print $1 "\t" $2-1 "\t" $2}' > test.dir_site.bed
```



## STEP2. polish sites with duplex reads

```shell
minimap -ax map-ont -t ${threads} ${assembler} ${duplex_fastq} > duplex.sam

samtools view -F 4 -bS -@ ${threads} duplex.sam > duplex.bam
samtools sort -@ ${threads}  duplex.bam > duplex.sort.bam

samtools mpileup -f ${assembler} -l test.dir_site.bed -q 30 --no-output-ins --no-output-ins --no-output-del --no-output-del --no-output-ends duplex.sort.bam > duplex.mpileup.txt

python count.py -in duplex.mpileup.txt > results.txt
```



**the demo for results:**

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