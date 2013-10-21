
#entropy (for a cluster) = (negative) * (sum over each department in cluster){ P(cluster/dt)  *  log(base2) (p(overall/dt)) }


#need to make a table of overall probabilities to start


#sorted2.txt is the document with the total counts

#31941765 = total number of departments

import math
from operator import itemgetter
import remove_total as R
import dept_ct_fun as DCF

#input file

def entropy_calc(prob_table):


# for finding the total DT in each cluster
	print "in entropy_calc"
	print "making clust_to_count..."	
	
	sum_errors = 0
	counted = open("clust_dept_ct_redo.txt", "r")
	clust_to_count = dict()
	for i, each in enumerate(counted):

		line = each.split("\t")
		if len(line) != 3:
			sum_errors += 1
			#print i
			continue
		clust = int(line[0])
		count = int(line[2])
		if clust_to_count.has_key(clust):
			current = clust_to_count[clust]
			clust_to_count[clust] = current + count
		else:
			clust_to_count[clust] = count

	counted.close()
	print "finished"
	print "The number of invalid lines is " + str(sum_errors) + "\n"
# clust to count maps from cluster to total count of DT in cluster

	print "doing other entropy stuff..."
	efile = open("entropy_list_redo.txt", "w")		
	counted = open("clust_dept_ct_redo.txt", "r")
	entropy = dict() #maps from cluster to entropy sum
	sum_errors = 0

	for i, each in enumerate(counted):
		line = each.split("\t")
		if len(line) != 3:
			print i
			continue
		count = int(line[2])
		dept = str(line[1])
		cluster = int(line[0])
		prob_clust = float(count) / float(clust_to_count[cluster])
		try:
			prob_total = table[dept]
		except KeyError:
			sum_errors += 1
			continue
		if int(clust_to_count[cluster]) == int(count):
			print str(cluster) + " one value " + str(count) + "prob" + str(math.log(prob_total,2))

		ent = prob_clust * (math.log(prob_total, 2))
		if entropy.has_key(cluster):
			current = entropy[cluster]
			entropy[cluster] = current + ent
		else:
			entropy[cluster] = ent

	print "finished"
	print "compiling list..."
	elist = []
	for each in entropy.keys():
		val = entropy[each] * -1
		entropy[each] = val
		elist.append((val, each))

	elist.sort()
	elist.reverse()

	for each in elist:
		entropy, cluster = each
		#print cluster
		efile.write(str(cluster) + "\t" + str(entropy) + "\n")

	print "done\n"
	print ("The number of keyerrors detected is " + str(sum_errors))

def overall_probability_table():

	table = dict()
	print "making probability table..."
	f = open('dept_ct.txt', 'r')
	for i, each in enumerate(f):
		line = each.split("\t")
		dept = line[0]
		if len(line) != 2:
			print i
		temp = int(line[1])
		table[dept] = float(temp)/9870479.0

	print "done"
	return table

if __name__ == "__main__":

	table = overall_probability_table() 
	entropy_calc(table) 
	
