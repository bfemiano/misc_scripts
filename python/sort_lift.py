import csv
from itertools import groupby

with open('/Users/bfemiano/category_lift.csv000', 'r') as lift_file:
	items = []
	for line in lift_file.readlines():
		items.append(line.strip('\n\r').split(','))
	items = sorted(items, key=lambda x: int(x[1]), reverse=True)
	with open('sorted_lift_by_score.csv', 'wb') as out_file:
		writer = csv.writer(out_file, delimiter=',')
		groups = [list(grp) for k,grp in groupby(items, lambda x: int(x[1]))]
		for g in groups:
			writer.writerows(sorted(g, key=lambda x : int(x[6]), reverse=True)[0:10])