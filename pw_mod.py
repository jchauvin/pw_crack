#!/usr/bin/python


# This is the dictionary of characters, and their potential substitutions in a password
pw_swap_dict = {
	'a' : [ '4', '@' ],
	'e' : [ '3' ],
	'i' : [ '1' ],
        'o' : [ '0' ],
	'l' : [ '1' ]
}


def find_indexes(str, ch):

  ''' Find all indexes in the string str of the character ch and return a list '''

  # traverse the str and make a generator of all indexes of the passed in character
  for i, ltr in enumerate(str):
	  if ltr == ch:
	    yield i



def pw_swap(password, dict):

  ''' Takes a password and then generates a list of comparable passwords with certain
  character substitutions.  i.e.  a=4, e=3, etc '''


  pw_set = set()
  pw_set.add(password)
  #print "Generating alternative passwords based on passed in value - ", password

  # Save the original password so we can reset it later in the for loops  
  pw_orig = password


  # Loop through the dictionary of list substitutions.  Each key will be the character to replace, and the
  # values in the dictionary will be lists of possible substitutions.  i.e. e => 3, a => @, etc.  
  for key in sorted(dict.keys()):

   # Loop through the list of substitutions for the current letter
   for swap in dict[key]:

     # Generate a list of indexes of all occurances of the current char
     indexes =  find_indexes(password, key)

     #  Loop through the indexes that were generated above.
     for i in indexes:

       password = pw_orig

       # Convert the password to a list to better manage it
       plist = list(password)
       # Set the current index to the current possible substitution value
       plist[i] = swap

       # Add this current version of the password to the password set
       pw_set.add(''.join(plist))
 

       # Loop through the dictionary again this time changinge all other key -> substitution pairs.  In a sense the only 
       # thing static is this loop is the index / character swap set above.  Everything else in the password is changed
       # as that stays constant
       for key2 in sorted(dict.keys()):
         for swap2 in dict[key2]: 
           # Traverse the password and swap out a character with its substitution if found
           for x, c in enumerate(plist):
             if plist[x] == key2:
               plist[x] = swap2
               # If the current version of the password is not in the password set, then add it
               if not ''.join(plist) in pw_set:
                 pw_set.add(''.join(plist))

	     
  return list(pw_set)



def generate_pwswap_dict(filename):

  ''' will generate a dictionary of characters and their possible substutions based on a file passed in.  '''
 
  return 1
  



def main():

        pw_list = pw_swap("hellostga", pw_swap_dict)
        print pw_list
        print 
        print
        print pw_swap("helloworldgoodbyehard", pw_swap_dict)




if __name__ == '__main__':
   main()

