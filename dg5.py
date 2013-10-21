from scipy.stats.stats import pearsonr
from operator import itemgetter
import sys
import math
from collections import Counter
import grid_counts


def difference_grid(grid1, grid2, id_dict_to_grid, out, totals, counters):

	total1 = totals[grid1]
	total2 = totals[grid2]
	counter1 = counters[grid1]
	counter2 = counters[grid2]

	list1 = counter1.keys()
	d = dict()

	print "in for loop..."
	# because we want the 20 words that define grid 1
	for each in list1 : 
		
		if counter1.has_key(each):
			fa = float(counter1[each])/float(total1)
		else :
			fa = 0
		if counter2.has_key(each) :
			fb = float(counter2[each])/float(total2)
		else :
			fb = 0
		difference = math.fabs(fa - fb)
		d[each] = difference
	print "done"

	c = Counter(d)
	f3 = open('tstat_words.txt', 'w')
	x = sorted(c.items(), key=itemgetter(1), reverse=True)
	if len(x) <= 40:
		for each in x:	
			f3.write(str(each) + "   " + "" "\n")
	else: 
		for i in range(40) :
			f3.write(str(x[i]) + "   " + "" "\n")

	# get two grids find the fraction and then get the difference between the fractions and see if its greater than delta

	word_arr = []
	f3.close()
	f3 = open('tstat_words.txt', 'r')
	for each in f3 :
		line = each.split()
		word = line[0].strip("('',")
		word_arr.append(word)


	word_set = set(word_arr)


	grida = grid1
	gridb = grid2

	grid_membership = []
	word_in_grid = []

	papers_to_titles_dict = dict()

	print "Making dict of papers to titles..."
	g = open('2011_id_word_bi.txt', 'r')
	for each in g :
		line = each.split()
		if line[1] not in word_set :
			continue
		if papers_to_titles_dict.has_key(line[0]) :
			papers_to_titles_dict[line[0]].append(line[1])
		else :
			papers_to_titles_dict[line[0]] = [line[1]]
	print "finished"
	g.close()

	list_of_papers = []

	print "Filling grid vector..."
	f = open('id_yr_type_disc_grid.txt', 'r')
	for each in f :
		line = each.split()
		temp = int(line[4])
		if int(line[1]) != 2011 or (not papers_to_titles_dict.has_key(line[0])):
			continue
		if temp == grida :
			grid_membership.append(1)
			list_of_papers.append(line[0])
		elif temp == gridb :
			grid_membership.append(0)
			list_of_papers.append(line[0])
		else :
			continue

	print "finished"
	f.close()

	print "finding wordlist for a grid..."

	corr_list = []

	for word in word_arr :

		word_in_grid = [0]*len(list_of_papers)

		for i, each in enumerate(list_of_papers) :
			if papers_to_titles_dict.has_key(each) :
				for this_word in papers_to_titles_dict[each] :
					if str(word) == str(this_word) :
						word_in_grid[i] = 1
						break

		(correlation, two_tailed_pvalue) = pearsonr(grid_membership, word_in_grid)
		corr_list.append((correlation, word))

	corr_list.sort()
	corr_list.reverse()

	out.write(str(grid1) + ":\n")
	print grid1
	for i in range(21) :
		print corr_list[i]
		out.write(str(corr_list[i]) + "\n")

def total_count():
	totals_array = [0]*5000
	counter_array = [[] for _ in range(5000)]

	f2 = open('2011_id_word_bi.txt', 'r')

	for line in f2:
		a = line.split()
		grid = int(id_dict_to_grid[a[0]])
		totals_array[grid] += 1
		counter_array[grid].append(a[1])

	return totals_array, counter_array




if __name__ == "__main__":

	test = sys.argv[1]

	if test == "scrap":
		out = open('scrap.txt', 'w')
		print "in scrap"
	else :
		out = open('out4.txt', 'w')
	f = open('id_yr_type_disc_grid.txt', 'r')
	id_dict_to_grid = dict()
	for line in f:
		a = line.split()
		if int(a[1]) != 2011:
			continue
		id_dict_to_grid[a[0]] = int(a[4])

	f.close()

	totals, counters = total_count = total_count()
	counter_array = [{}]*5000
	for i in range(len(counters)):
		counter_array[i] = Counter(counters[i])

	for i in range(2000):
		if totals[2000 + i] == 0:
			continue
		difference_grid(2050 + i, 0, id_dict_to_grid, out, totals, counter_array)





