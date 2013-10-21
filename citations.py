import matplotlib.pyplot as plt
import math
import numpy as np
import os.path
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr

def papers04_from_file():
	
	out = open("file_04.txt", "w")
	big_file = open("id_yr_clust_grid.txt", "r")
	for each in big_file:
		line = each.split()
		year = int(line[1])
		if year == 2004:
			out.write(each)
	big_file.close()

def first_parse():

	big_file = open("id_yr_clust_grid.txt", "r")
	small_file = open("file_04.txt", "r")
	cluster_to_papers = dict()
	#citing = open("id04_citing.txt", "r")
	#citing_mod = open("citing2.txt", "w")

	paper_to_coords = dict()
	paper_set_big_file = set()
	for each in big_file:
		line = each.split("\t")
		paper = int(line[0])
		x = float(line[4])
		y = float(line[5].strip())
		paper_set_big_file.add(paper)
		paper_to_coords[paper] = (x, y)
	

	paper_set = set()
	for each in small_file:
		line = each.split()
		paper = int(line[0])
		paper_set.add(paper)
		cluster = int(line[2])
		if cluster_to_papers.has_key(cluster):
			cluster_to_papers[cluster].append(paper)
		else:
			cluster_to_papers[cluster] = [paper]
	for each in cluster_to_papers.keys():
		if len(cluster_to_papers[each]) == 0:
			print "ppop"
	for each in citing:
		line = each.split("\t")
		paper = int(line[0])
		citing_paper = int(line[1])
		if paper == citing_paper:
			continue
		if (paper not in paper_set) or (citing_paper not in paper_set_big_file):
			continue
		else:
			citing_mod.write(each)
	citing_mod.close()

	papers_to_citing_papers = dict()
	f = open("citing2.txt", "r")
	for each in f:
		line = each.split("\t")
		paper = int(line[0])
		citing_paper = int(line[1])
		if papers_to_citing_papers.has_key(paper):
			papers_to_citing_papers[paper].append(citing_paper)
		else:
			papers_to_citing_papers[paper] = [citing_paper]
	f.close()

	print "Calculating distance..."
	population = []
	cluster_to_distance_average = dict()
	cluster_to_distance_length = dict()
	for cluster in cluster_to_papers.keys():
		cluster_list = []
		dumbutt = 0.0
		for paper in cluster_to_papers[cluster]:
			x1, y1 = paper_to_coords[paper]
			#dumbutt = 0.0
			if not papers_to_citing_papers.has_key(paper):
				continue
			for citing_paper in papers_to_citing_papers[paper]:
				x2, y2 = paper_to_coords[citing_paper]
				dx = math.pow(x1 - x2, 2)
				dy = math.pow(y1 - y2, 2)
				squared_distance = dx + dy
				if squared_distance != 0.0:
					cluster_list.append(math.sqrt(squared_distance))
					population.append(math.sqrt(squared_distance))
		cluster_to_distance_length[cluster] = len(cluster_list)
		cluster_to_distance_average[cluster] = np.mean(cluster_list)
	
	mean = np.mean(population)
	standard_deviation = np.std(population)
	print "mean " + str(mean)
	print "Std " + str(standard_deviation)
	print "size of population " + str(len(population))
	print "maximum distance " + str(max(population))
	print "minimum distance " + str(min(population))

	zscores = []
	scores_to_clust = dict()
	outfile = open("cluster_zscore.txt", "w")
	out2 = open("sorted.txt", "w")
	for cluster in cluster_to_distance_average.keys():
		if cluster_to_distance_length[cluster] == 0:
			continue
		SE = standard_deviation / (math.sqrt(cluster_to_distance_length[cluster]))
		z = (cluster_to_distance_average[cluster] - mean) / SE
		zscores.append(z)
		scores_to_clust[z] = cluster
		outfile.write(str(cluster) + "\t" + str(z) + "\n")
	
	l = sorted(zscores, key=lambda f: float('-inf') if math.isnan(f) else f)
	l.reverse()
	sumnan = 0	
	for score in l:
		cluster = scores_to_clust[score]
		if math.isnan(score):
			sumnan += 1
		out2.write(str(cluster) + "\t" + str(score) + "\n")
	print sumnan
	
	outfile.close()
	out2.close()

def modify_big_file():

	big_file = open("id_yr_clust_grid_x_y_auth_affil_dpid_dept.txt", "r")
	papers = set()
	out = open("id_yr_clust_grid_x_y.txt", "w")
	for each in big_file:
		line = each.split()
		paper = int(line[0])
		if paper in papers:
			continue
		else:
			out.write(str(paper) + "\t" + str(line[1]) + "\t" + str(line[2]) + "\t" + str(line[3]))
			out.write("\t" + str(line[4]) + "\t" + str(line[5]) + "\n")
			papers.add(paper)
	out.close()
	big_file.close()

def final_corr():

	zfile = open("cluster_zscore.txt", "r")
	efile = open("entropy_list_redo.txt", "r")

	clust_zscore = dict()
	clust_entropy = dict()
	for each in efile:
		line = each.split()
		cluster = int(line[0])
		entropy = float(line[1])
		clust_entropy[cluster] = entropy

	for each in zfile:
		line = each.split()
		cluster = int(line[0])
		zscore = float(line[1])
		clust_zscore[cluster] = zscore
	x = []
	y = []
	for i in range(150000):
		if not clust_zscore.has_key(i) or not clust_entropy.has_key(i):
			continue
		x.append(clust_entropy[i])
		y.append(clust_zscore[i])

	correlation, pvalue = spearmanr(x,y)
	print "spearman " + str(correlation)
	print pvalue

	correlation, pvalue = pearsonr(x,y)
	print "pearson " + str(correlation)
	x2 = []
	y2 = []
	for i in range(150000):
		if not clust_zscore.has_key(i):
			continue
		x2.append(i)
		y2.append(clust_zscore[i])

	x1 = []
	y1 = []
	for i in range(150000):
		if not clust_entropy.has_key(i):
			continue
		x1.append(i)
		y1.append(clust_entropy[i])

	plt.scatter(x,y)
	plt.title('Entropy of a Cluster vs. citing distance (redo)')
	plt.xlabel('Entropy')
	plt.ylabel('Citing Distance z scores')
	plt.savefig('entropy_citingscores_redo.png')
	plt.show()
	efile.close()
	zfile.close()
	
if __name__ == "__main__":
	
	modify_big_file()
	papers04_from_file()	
	first_parse()
	final_corr()



