import sys
import math
import string
                    
def get_spreadsheet_array(num_columns=36):
    spreadsheet_index = []
    max_char_width = int(math.ceil(math.log(num_columns, 26)))
    i = 0
    for j in range(1, max_char_width+1):
        for l in range (0, (26**j)):
            if i < 26:
                spreadsheet_index.append(string.lowercase[i].upper())
                i += 1
                if i == num_columns:
                    return spreadsheet_index
            else:
                for k in range(0, 26):
                    spreadsheet_index.append(spreadsheet_index[l] + string.lowercase[k].upper())
                    i += 1
                    if i == num_columns:
                        return spreadsheet_index
                        
                        
print get_spreadsheet_array(int(sys.argv[1]))