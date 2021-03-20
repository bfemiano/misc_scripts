letters_start = ["U", "A", "T"]
def p(letters, word):
    for i in range(len(letters)):
          if len(letters) > 1:	
              word.append(letters[i])
              p([l for l in letters if l != letters[i]], word)
              word.pop()
          else:
              print(''.join(word + letters))

p(letters_start, [])
     
