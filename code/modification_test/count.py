import argparse
parser = argparse.ArgumentParser(description="")
parser.add_argument("-in", "--input", type=str, metavar="", required=True, help="input the file")
args = parser.parse_args()

def stats_num(input_base, input_string):
	data = {}

	if input_base == "A":
		num_A = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_C = input_string.count('C') + input_string.count('c')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "T":
		num_T = input_string.count('.') + input_string.count(',')
		num_A = input_string.count('A') + input_string.count('a')
		num_C = input_string.count('C') + input_string.count('c')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "C":
		num_C = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_A = input_string.count('A') + input_string.count('a')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "G":
		num_G = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_C = input_string.count('C') + input_string.count('c')
		num_A = input_string.count('A') + input_string.count('a')

	data["A"] = num_A
	data["T"] = num_T
	data["C"] = num_C
	data["G"] = num_G
	total = num_A + num_T + num_G + num_C

	if total != 0:
		P_A = num_A / total
		P_T = num_T / total
		P_G = num_G / total
		P_C = num_C / total
	else:
		P_A = 0
		P_T = 0
		P_G = 0
		P_C = 0

	mes = str(num_A) + "\t" + str(num_T) + "\t" + str(num_G) + "\t" + str(num_C) + "\t" + str(P_A) + "\t" + str(P_T) + "\t" + str(P_G) + "\t" + str(P_C)

	return(mes)


def loading_info(input_data):
	print("chr\tpos\tbase\tN_A\tN_T\tN_G\tN_C\tP_A\tP_T\tP_G\tP_C")
	with open(input_data) as ff:
		for i in ff:
			i = i.replace("\n", "")
			i = i.split("\t")
			chr = i[0]
			pos = i[1]
			base = i[2]
			string = i[4]

			if i[3] != 0:
				fre = stats_num(base, string)
				print(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre))
	ff.close()

if __name__=="__main__":
    
    loading_info(args.input)

