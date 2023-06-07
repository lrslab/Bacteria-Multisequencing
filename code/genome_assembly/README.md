To get the substitutions and indels from the Quast results, using the following code:

```shell
awk '{print $1 "\t" $45 "\t" $46}' transposed_report.tsv  | grep -v Assembly > tmp_file.txt 
sed -i 's/.fq//g' tmp_file.txt
sed -i 's/.seed1./_seed1_/g' tmp_file.txt 
sed -i 's/.seed2./_seed2_/g' tmp_file.txt 
sed -i 's/.seed3./_seed3_/g' tmp_file.txt 
sed -i 's/.seed4./_seed4_/g' tmp_file.txt 
sed -i 's/.seed5./_seed5_/g' tmp_file.txt 
sed -i 's/R941./R941_/g' tmp_file.txt
sed -i 's/simplex./simplex_/g' tmp_file.txt
sed 's/_/\t/g' tmp_file.txt | awk '{print $1 "\t" $2"_"$5 "\t" $3 "\t" $4 "\t" $6 "\t" $7}' > final_file.txt
```

Then we can get the following table

```shell
bac	type	coverage	seed	mis	indels
Acinetobacter_pittii	R941_ngs	100	seed1	0.05	0.33
Acinetobacter_pittii	R941_ont	100	seed1	0.13	6.13
Acinetobacter_pittii	R941_ngs	100	seed2	0.46	0.87
Acinetobacter_pittii	R941_ont	100	seed2	0.54	6.51
Acinetobacter_pittii	R941_ngs	100	seed3	0.00	0.46
Acinetobacter_pittii	R941_ont	100	seed3	0.00	6.49
Acinetobacter_pittii	R941_ngs	100	seed4	0.31	0.46
Acinetobacter_pittii	R941_ont	100	seed4	0.28	6.37
Acinetobacter_pittii	R941_ngs	100	seed5	0.26	0.56
Acinetobacter_pittii	R941_ont	100	seed5	0.31	6.56
```

To ensure the accuracy and reliability of our results, we implemented a stringent quality control approach that involved removing the highest and lowest values for each metric at each assembly coverage for each bacterium. We then calculated the average value from the remaining three values to represent the performance of each assembly method for each bacterium. The following python code can help us to achieve the target:

```python
data = {}
with open("file_name") as ff:
        for i in ff:
                i = i.replace("\n", "")
                i = i.split("\t")
                mes = i[0] + "_" + i[1] + "_" + i[2]

                if mes not in data.keys():
                        data[str(mes)] = {}
                        data[str(mes)]["mis"] = []
                        data[str(mes)]["indels"] = []
                        
                data[str(mes)]["mis"].append(float(i[4]))
                data[str(mes)]["indels"].append(float(i[5]))
ff.close()

for i in data.keys():
        data[str(i)]["mis"].remove(max(data[str(i)]["mis"]))
        data[str(i)]["mis"].remove(min(data[str(i)]["mis"]))

        data[str(i)]["indels"].remove(max(data[str(i)]["indels"]))
        data[str(i)]["indels"].remove(min(data[str(i)]["indels"]))

        mis = sum(data[str(i)]["mis"]) / len(data[str(i)]["mis"])
        indel =  sum(data[str(i)]["indels"]) / len(data[str(i)]["indels"])

        print(i.replace("_", "\t") + "\t" + str(mis) + "\t" + str(indel))
```

We get the following table (please add the header):

```shell
bac	type	coverage	mis	indels
Acinetobacter_pittii	R941_ngs	100	0.20666666666666667	0.49333333333333335
Acinetobacter_pittii	R941_ont	100	0.24	6.456666666666667
Acinetobacter_pittii	R941_ngs	10	7.993333333333333	7.676666666666667
Acinetobacter_pittii	R941_ont	10	37.04	76.27333333333333
Acinetobacter_pittii	R941_ngs	110	0.2733333333333334	0.41333333333333333
Acinetobacter_pittii	R941_ont	110	0.2733333333333333	6.326666666666667
Acinetobacter_pittii	R941_ngs	120	0.07666666666666666	0.48666666666666664
Acinetobacter_pittii	R941_ont	120	0.13	6.316666666666666
Acinetobacter_pittii	R941_ngs	20	0.10333333333333333	0.58
```

This table can be used to plot the figure using R package, ggplot2.

```R
df <- read.csv("final_file.txt", sep = "\t", header = T)

ggplot(df, aes(x=coverage, color=type, y=mis, group=type)) + 
	geom_line(size=1) +  geom_point(size=2) + theme_bw()  + 
	scale_x_continuous(name="", limits = c(0,120), breaks=seq(0,120,20)) +
	scale_y_continuous(name="substitutions per 100 kbp",
                     breaks=c(0.00390625, 0.015625, 0.0625,0.25,1,4,16,64), 
                     labels = c(0.00390625, 0.015625, 0.0625,0.25,1,4,16,64),
                     limits = c(0.001,64),expand = c(0,0),trans = "log2") +
	theme(axis.text=element_text(size=12, color="black"),
      		axis.title=element_text(size=12, color="black"),
       		legend.text = element_text(size=12, color="black"),
        	strip.text = element_text(size=12, color="black", face="italic"),
        	legend.title = element_blank(), legend.position = "bottom") +  
	facet_grid("~bac") + 
	scale_color_manual(values=c("R941_ont"="#9ecae1",
                              "R941_ngs"="#bbd9ea",
                              "simplex_ont" ="#fec44f", 
                              "simplex_ngs" ="#fee7b8",
                              "duplex" = "#fc9272"))
```

And we get the following demo figure for Mismatches per 100 Kbp.


![alt text](demo/substitution.png)


R code for Indels:

```R
ggplot(df, aes(x=coverage, color=type, y=indels, group=type)) + 
	geom_line(size=1) +  geom_point(size=2) +  theme_bw()  + 
	facet_grid("~bac") +  
	scale_x_continuous(name = "", limits = c(0,120), breaks=seq(0,120,20)) +
	scale_y_continuous(name="Indels per 100 kbp",
                     breaks=c(0.25,1,4,16,64,256),
                     labels = c(0.25,1,4,16,64,256),
                     limits = c(0.25,256), expand = c(0,0),trans = "log2") +
	scale_color_manual(values=c("R941_ont"="#9ecae1",
                              "R941_ngs"="#bbd9ea",
                              "simplex_ont" ="#fec44f", 
                              "simplex_ngs" ="#fee7b8",
                              "duplex" = "#fc9272")) +
	theme(axis.text=element_text(size=12, color="black"),
        axis.title=element_text(size=12, color="black"),
        legend.text = element_text(size=12, color="black"),
        strip.text = element_text(size=12, color="black", face="italic"),
        legend.title = element_blank(), legend.position = "bottom")
```

Demo figure for Indels per 100 Kbp:

![alt text](demo/Indels.png)



Demo table for BUSCO

```shell
bac	type	coverage	busco
Acinetobacter_pittii	duplex	10.7	98.1
Bacillus_cereus	duplex	8.9	95.8
Enterococcus_faecium	duplex	31.2	99.5
Escherichia_coli	duplex	4.1	73.4
Klebsiella_pneumoniae	duplex	18.9	98.2
Pseudomonas_aeruginosa	duplex	7.1	98
Salmonella_enterica	duplex	6.2	94.6
Staphylococcus_aureus	duplex	14.4	99.8
Acinetobacter_pittii	simplex_ngs	110	99.46666666666665
Acinetobacter_pittii	simplex_ngs	80	99.33333333333333
Acinetobacter_pittii	simplex_ont	120	99.26666666666667
Acinetobacter_pittii	R941_ngs	40	99.39999999999999
Acinetobacter_pittii	R941_ont	10	83.3
Acinetobacter_pittii	R941_ont	20	94.2
Acinetobacter_pittii	R941_ngs	30	99.23333333333335
Acinetobacter_pittii	simplex_ngs	100	99.33333333333333
Acinetobacter_pittii	R941_ngs	10	99.33333333333333
Acinetobacter_pittii	R941_ngs	90	99.33333333333333
Acinetobacter_pittii	simplex_ont	60	99.2
```



R code for BUSCO

```R
ggplot(df, aes(x=coverage, color=type, y=busco, group=type)) + 
  geom_line(size=1) + geom_point(size=2) + facet_grid("~bac") +  theme_bw() + 
  scale_x_continuous(name="", limits = c(0,120), breaks=seq(0,120,20)) + 
  scale_y_continuous(name="Busco scope") +
  scale_color_manual(values=c("R941_ont"="#9ecae1",
                              "R941_ngs"="#bbd9ea",
                              "simplex_ont" ="#fec44f", 
                              "simplex_ngs" ="#fee7b8",
                              "duplex" = "#fc9272")) +
	theme(axis.text=element_text(size=12, color="black"),
        axis.title=element_text(size=12, color="black"),
        legend.text = element_text(size=12, color="black"),
        strip.text = element_text(size=12, color="black", face="italic"),
        legend.title = element_blank(), legend.position = "bottom")
```



Demo figure for BUSCO

![alt text](demo/busco.png)
