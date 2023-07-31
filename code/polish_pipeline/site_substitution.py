import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("-in", "--input", type=str, metavar="", required=True, help="")
parser.add_argument("-cut", "--cutoff", type=float, metavar="", required=True, help="")
parser.add_argument("-out", "--output", type=str, metavar="", required=False, help="", default="result.txt")
args = parser.parse_args()

def calculate_distance(chrom, pos, string, cutoff):
	def calcualte_abs(num_1, num_2, total_1, total_2):
		value_1 = int(num_1)/int(total_1)
		value_2 = int(num_2)/int(total_2)
		abs_value = float(format(abs(value_1 - value_2), '.3f'))
		return(abs_value)

	dict = {}
	for i in string:
		dict[i] = dict.get(i, 0) + 1

	for i in ["A", "T", "G", "C", "a", "t", "g", "c"]:
		if i not in dict.keys():
			dict[str(i)] = 0 

	Forward_depth = dict["A"] + dict["C"] + dict["G"]+ dict["T"]
	Reverse_depth = dict["a"] + dict["c"] + dict["g"]+ dict["t"]
	min_depth = 25

	if Forward_depth >= min_depth and Reverse_depth >= min_depth:
		absA = calcualte_abs(dict["A"], dict["a"], Forward_depth, Reverse_depth)
		absT = calcualte_abs(dict["T"], dict["t"], Forward_depth, Reverse_depth) 
		absG = calcualte_abs(dict["G"], dict["g"], Forward_depth, Reverse_depth)
		absC = calcualte_abs(dict["C"], dict["c"], Forward_depth, Reverse_depth)
		Manhattan_distance = absA + absT + absC + absG
		MAE = float(format(Manhattan_distance / 2, '.3f'))

		if MAE >= float(cutoff):
			mes = str(chrom) + "\t" + str(pos) + "\t" + str(MAE) + "\t"
			mes += str(absA) + "\t" + str(absT) + "\t" + str(absG) + "\t" + str(absC) + "\t"
			mes += str(dict["A"]) + "," + str(dict["T"]) + "," + str(dict["G"]) + "," + str(dict["C"]) + ","
			mes += str(dict["a"]) + "," + str(dict["t"]) + "," + str(dict["g"]) + "," + str(dict["c"])
			return(mes)
	else:
		pass

def get_direction_info(inputfile, outputfile, cutoff):
	header = "Chr\tPos\tMAE\tabsA\tabsT\tabsG\tabsC\tA,T,G,C,a,t,g,c"
	with open(outputfile, "w") as fo:
		fo.write(header + "\n")
		with open(inputfile) as ff:
			for base in ff:
				base = base.replace("\n", "")
				base = base.split("\t")

				if int(base[3]) >= 50:
					chrom = str(base[0])
					pos = str(base[1])
					string = str(base[4])
					if calculate_distance(chrom, pos, string, float(cutoff)):
						fo.write(calculate_distance(chrom, pos, string, float(cutoff)) + "\n")
		ff.close()
	fo.close()

if __name__=="__main__":
	get_direction_info(args.input, args.output, args.cutoff)