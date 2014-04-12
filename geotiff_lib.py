#added comment
f = open('geotiff_jars', 'r')
outFile = open('geotiff_jars.txt', 'w')
for line in f.readlines() :
	outFile.write(line[line.rfind('/')+1:])
outFile.close()
