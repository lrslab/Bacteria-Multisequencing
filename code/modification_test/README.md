To check whther the modification lead to this kind of substutitions, we used the whole-genome amplication datasets of *Acinetobacter pittii* generated from the R10.4.1 and R9.4.1 sequencing.

The following cammands were used to map reads against the reference.

```shell
minimap2 -ax map-ont -t 20 {reference.mmi} {input.fastq} > out.sam
samtool view -bS -@ 10 out.sam | samtools sort -@ 10 > out.bam
samtools index out.bam
```

Getting the proportion of mapping base for each potential modified site by following cammands, here, we only focus on the substitution.

```shell
samtools mpileup -f {reference.fa} -l {site.bed} --no-output-ends --no-output-ins --no-output-ins --no-output-del --no-output-del out.bam > out.info
```

Demo for the output file

```shell
ab1_chrom_pilon_pilon_pilon	5736	C	7	,,,,,..	ECQDQ{S
ab1_chrom_pilon_pilon_pilon	103712	C	10	..,,,...,,	{{{;={QQU3
ab1_chrom_pilon_pilon_pilon	118823	C	4	.,,,	{6K{
ab1_chrom_pilon_pilon_pilon	185802	C	1	.	{
ab1_chrom_pilon_pilon_pilon	190852	C	4	..,T	=B{{
ab1_chrom_pilon_pilon_pilon	210611	C	10	,,.t,.,.T,	{{:E9{{Q{A
ab1_chrom_pilon_pilon_pilon	230481	C	7	,,,..,,	?E{N{N9
ab1_chrom_pilon_pilon_pilon	273139	C	14	T..,t,T,,,Tt.t	{H{2{{{{{6{FU:
ab1_chrom_pilon_pilon_pilon	370205	C	6	...Ta,	{{{QH.
ab1_chrom_pilon_pilon_pilon	494994	C	12	..T..T,,,...	{{7{{{K{{{{4
```

The pyhon script can help to count the number of four types of mapped base:

``` shell
python count.py -in {input.info} > output.info
```

Demo for the output file

```shell
#chromsome	position	reference_base	number_of_A_base	number_of_T_base	number_of_G_base	number_of_C_base proportion_of_A_base	proportion_of_T_base	proportion_of_G_base	proportion_of_C_base

#chr	pos	base	N_A	N_T	N_G	N_C	P_A	P_T	P_G	P_C
ab1_chrom_pilon_pilon_pilon	5736	C	0	0	0	7	0.0	0.0	0.0	1.0
ab1_chrom_pilon_pilon_pilon	103712	C	0	0	0	10	0.0	0.0	0.0	1.0
ab1_chrom_pilon_pilon_pilon	118823	C	0	0	0	4	0.0	0.0	0.0	1.0
ab1_chrom_pilon_pilon_pilon	185802	C	0	0	0	1	0.0	0.0	0.0	1.0
ab1_chrom_pilon_pilon_pilon	190852	C	0	1	0	3	0.0	0.25	0.0	0.75
ab1_chrom_pilon_pilon_pilon	210611	C	0	2	0	8	0.0	0.2	0.0	0.8
ab1_chrom_pilon_pilon_pilon	230481	C	0	0	0	7	0.0	0.0	0.0	1.0
```

Demo code for plotting

```R
ggplot(df_3, aes(x=group,y=num, fill=base)) + 
    geom_bar(stat="identity",width=0.5,position='fill', alpha=0.5) +
    facet_wrap(~type) + theme_bw() +  xlab("") +
    geom_text(aes(label = num), position = position_fill(vjust=0.5)) + 
  	theme(axis.text.y=element_text(size=12, color="black"),
    	axis.text.x=element_text(size=12, color="black", angle=30, vjust = 0.5, hjust=0.5),
        axis.title=element_text(size=12, color="black"),
        legend.text = element_text(size=12, color="black"),
        strip.text = element_text(size=12, color="black"),
        legend.title = element_blank(), legend.position = "right") +
  	scale_y_continuous(name="Matched base proportion") +
  	scale_fill_manual(values=c("A"="#3cb346",
                             "C"="#00abf0",
                             "G" ="#942d8d", 
                             "T" ="#eeb401"))
```

Demo figure

[alt text](Demo.png)

