from collections import Counter

def first():

	print "in first..."
	paper_set = set()
	f = open("id_yr_clust_grid_x_y_auth_affil_dpid_dept.txt", "r")
	out = open("file_edit.txt", "w")
	out2 = open("clust_dept.txt", "w")
	for each in f:
		line = each.strip().split("\t")
		author = line[6]
		paper = int(line[0])
		clust = int(line[2])
		dept = str(line[9]).lower()
		if paper in paper_set:
			continue
		paper_set.add(paper)
		out.write(each)
		out2.write(str(clust) + "\t" + str(dept)+ "\n")

	f.close()
	out.close()
	out2.close()	
	print "done"

def remove():

	print "in remove..."
	f = open("clust_dept.txt", "r")
	out = open("clust_dept_removed.txt", "w")
	for index, line in enumerate(f):
		line_arr1 = line.strip().split("\t")
		line_arr  = line_arr1[1].split()
		out.write(str(line_arr1[0] + "\t"))
		for i in range(len(line_arr)):
			if line_arr[i] == "department" or line_arr[i] == "dept." or line_arr[i] == "dept" or line_arr[i] == "of" or line_arr[i] == "depts." :	
				if i == len(line_arr) - 1:
					out.write("\n")
					break
				continue
			elif line_arr[i] == "c.s." :
				out.write("computer science")
			elif line_arr[i] == "cis" :
				out.write("computer and information science")
			elif line_arr[i] == "sci." :
				out.write("science")
			elif line_arr[i] == "eng." :
				out.write("engineering")
			elif line_arr[i] == "lib." :
				out.write("library")
			elif line_arr[i] == "info." :
				out.write("information")
			elif line_arr[i] == "comp." :
				out.write("computer")
			elif line_arr[i] == "elec." :
				out.write("electrical")
			elif line_arr[i] == "mgmt." :
				out.write("management")
			elif line_arr[i] == "conserv." :
				out.write("conservation")
			elif line_arr[i] == "sciences" :
				out.write("science")
			elif line_arr[i] == "appl." :
				out.write("applied")
			elif line_arr[i] == "civ." :
				out.write("civil")
			elif line_arr[i] == "pub." :
				out.write("public")
			elif line_arr[i] == "hlth." :
				out.write("health")
			elif line_arr[i] == "theor." :
				out.write("theoretical")
			elif line_arr[i] == "numer." :
				out.write("numerical")
			elif line_arr[i] == "different." :
				out.write("differential")
			#elif line_arr[i] == "de" :
			#	if i == len(line_arr) - 1:
			#		out.write("\n")
			#		break
			#	continue
			elif line_arr[i] == "/x":
				if i == len(line_arr) - 1:
					out.write("\n")
					break
				continue
			elif line_arr[i] == "ii" or line_arr[i] == "i" or line_arr[i] == "iii":
				if i == len(line_arr) - 1:
					out.write("\n")
					break
				continue
			else :
				out.write(line_arr[i].lower())

				
			if i == len(line_arr) - 1 :
				out.write("\n")
			else:
				out.write(" ")

	f.close()
	out.close()

#  additional check needed because some departments are just "Department I" and then the whole line
#  gets stripped and results in an index error later.  This is also added on to eliminate possible foreign departments

	f = open("clust_dept_removed.txt", "r")
	out = open("clust_dept_removed_final.txt", "w")

	sum_lines = 0

	for i, each in enumerate(f):

		line = each.strip().split("\t")
		if len(line) != 2:
			print i
			sum_lines += 1
			continue
		flag = False
		for this in line[1].split():
			if "departament" in this or this == "depto." or this == "de" or "departamemt" in this or this == "dpto." or this == "departmento" or this == "arpeges" or this == "dpt." or this =="physik" or this == "matiere" or this == "estuctura" or this == "biologia":
				flag = True
				break
			if "d'" in this or "l'" in this or "cristal" in this:
				flag = True
				break
		if flag:
			continue
		else:
			out.write(each)

	f.close()
	out.close()
	print "done"

def combine_total():

	f = open("clust_dept_removed_final.txt", "r")
	out = open("dept_ct.txt", "w")

	dept_ct = dict()

	for i, each in enumerate(f):
		line = each.strip().split("\t")
		if len(line) != 2:
			print i
			print line
			continue
		dept = line[1]
		if dept_ct.has_key(dept):
			current = dept_ct[dept]
			dept_ct[dept] = current + 1
		else:
			dept_ct[dept] = 1
	total_count = []
	for each in dept_ct.keys():
		count = dept_ct[each]
		total_count.append((count, each))

	total_count.sort()
	total_count.reverse()
	for each in total_count:
		count, dept = each

		out.write(str(dept.strip()) + "\t" + str(count) + "\n")

	f.close()
	out.close()

def combine_cluster():

	f = open("clust_dept_removed_final.txt", "r")
	out = open("clust_dept_ct_redo.txt", "w")
	
	clust_to_depts = dict()
	for each in f:
		line = each.strip().split("\t")
		cluster = int(line[0])
		dept = line[1]

		if clust_to_depts.has_key(cluster):
			clust_to_depts[cluster].append(dept)
		else:
			clust_to_depts[cluster] = [dept]


	for cluster in clust_to_depts.keys():
		
		dept_list = clust_to_depts[cluster]
		dept_ct = Counter(dept_list)
		for dept in dept_ct.keys():
			count = dept_ct[dept]
			out.write(str(cluster) + "\t" + str(dept.strip()) + "\t" + str(count) + "\n")
		


if __name__ == "__main__":

	first()
	remove()
	combine_total()
	combine_cluster()
