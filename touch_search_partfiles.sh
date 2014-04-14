#!/usr/bin/env zsh
for m in 07 08 09 10 11 12;
do
	for d in 01 02 03  04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31;
	do
		for h in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23;
		do
			for s in 0 1 2 3 4 5 6 7 8 9 10;
			do
				snakebite mv "/metamx-magnetic-share/audience_data/raw/y=2013/m=$m/d=$d/H=$h/searches-part-m-0000$s.bz2" "/metamx-magnetic-share/audience_data/raw/y=2014/m=$m/d=$d/H=$h/part-m-0000$s.bz2" 
			done
			snakebite touchz "/metamx-magnetic-share/audience_data/raw/y=2013/m=$m/d=$d/H=$h/_SUCCESS"
			echo "renaming parts and touching _SUCCESS file for 2013 $m-$d-$h"
		done
	done
done

for m in 01 02 03 04;
do
	for d in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31;
	do
		for h in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23;
		do
			for s in 0 1 2 3 4 5 6 7 8 9 10;
			do
				snakebite mv "/metamx-magnetic-share/audience_data/raw/y=2014/m=$m/d=$d/H=$h/searches-part-m-0000$s.bz2" "/metamx-magnetic-share/audience_data/raw/y=2014/m=$m/d=$d/H=$h/part-m-0000$s.bz2" 
			done
			snakebite touchz "/metamx-magnetic-share/audience_data/raw/y=2014/m=$m/d=$d/H=$h/_SUCCESS"
			echo "renaming parts and touching _SUCCESS file for 2014 $m-$d-$h"
		done
	done
done
