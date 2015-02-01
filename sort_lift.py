import csv
from itertools import groupby

def sort_by(x):
	(dt, p, l1, l2, l3, l, index) = x
	return int(p)

with open('/Users/bfemiano/category_lift.csv000', 'r') as lift_file:
	items = []
	for line in lift_file.readlines():
		items.append(line.strip('\n\r').split(','))
	items = sorted(items, key=sort_by, reverse=True)
	with open('sorted_lift_by_score.csv', 'wb') as out_file:
		writer = csv.writer(out_file, delimiter=',')
		groups = []
		for k,grp in groupby(items, lambda x: int(x[1])):
			 groups.append(list(grp))
		for g in groups:
			g_s = sorted(g, key=lambda x : int(x[6]), reverse=True)
			writer.writerows(g_s)