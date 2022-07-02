def merge_in_place(in_list):
    to_merge_list = sorted(in_list)
    i = 0
    end = len(to_merge_list) - 1
    while i < end:
            if (to_merge_list[i][1] - to_merge_list[i+1][0]) >= -1: #overlapping ranges
                #In the case where the first completly consumes the second, we want to just completely discard the 2nd. 
                # Example (1, 17) and (3, 8)
                if not (to_merge_list[i][0] < to_merge_list[i+1][0] and to_merge_list[i][1] > to_merge_list[i+1][1]): 
                    to_merge_list[i] = (to_merge_list[i][0], to_merge_list[i+1][1])
                del to_merge_list[i+1]
            else:
                i += 1
            end = len(to_merge_list) - 1
    print 'input: %s, output: %s' % (in_list, to_merge_list) 
            

merge_in_place([(3,7),(5,8),(9,10),(13,17)])
merge_in_place([(3,7),(13,17)])
merge_in_place([(3,13),(13,17)])
merge_in_place([(3,7),(1,17)])
merge_in_place([(1,17)])
merge_in_place([(3,7),(8,9),(9,10),(13,17),(20,23)])