#!/usr/bin/python -tt

import crypt
import pw_mod
import argparse
from datetime import date,datetime,timedelta
now = datetime.today()

pw_swap_dict = {
        'a' : [ '4', '@' ],
        'e' : [ '3' ],
        'i' : [ '1' ],
        'o' : [ '0' ],
        'l' : [ '1' ]
}

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
YELLOW = '\033[93m'
FAIL = '\033[91m'
RED = '\033[91m'
ENDC = '\033[0m'



def getSalt(cryptPass):

  ''' Will take an encrypted password, determine its hashing algorithim, and then determine the pw salt '''

  #  Determine the Hashing type.  If the first character isn't a $ then it most likely is an old hashing
  #  algorithm with the first 2 characters being the salt
  try :

    if cryptPass[:1] == '$' :
      ctype = cryptPass.split("$")[1]
    else: 
      ctype = "NONE"
  except Exception,e :
    print "Exception - ", e

  if ctype == '1' or ctype == '6':
    print OKBLUE+"[+] Hash type SHA-512 detected ... "+ENDC
    print OKBLUE+"[+] Be Patient ... "+ENDC
    salt = cryptPass.split("$")[2]
    insalt = "$" + ctype + "$" + salt + "$"
  else:
    insalt = cryptPass[0:2]

  return insalt



def crackPass(cryptPass):

  ''' Will attempt to crack a passed in password by going through a dictionary and testing the encrypted pw, against
      all dictionary words, as well as all potential dictionary words with certain common character substitutions '''

  # Determine what the salt of the current encrypted password is
  salt = getSalt(cryptPass)

  dictFile = open('dictionary.txt', 'r')

  # Loop through all words in the dictionary file
  for word in dictFile.readlines():
    word = word.strip('\n')

    wordList = pw_mod.pw_swap(word, pw_swap_dict)
    #print "wordList = ", wordList

    for pwWord in wordList:
      # Encrypt the current dictionary word using the salt from the passed in encrypted pw
      cryptWord = crypt.crypt(pwWord,salt)
      if ( cryptWord.strip('\n') == cryptPass.strip('\n') ):
        return pwWord

  dictFile.close()
  return False



def processPassFile(passFilename, outFilename):
 
  ''' Open passed in password file to crack and go by it line by line processing each password '''
 
  # Open the password file that holds the encrypted passwords
  try :
    passFile = open(passFilename, 'r')
    outFile = open(outFilename, 'wb')
  except Exception, e:
    print "Exception:", e

  today = date.today()
  outFile.write(today.strftime("%A %d. %B %Y"))
  outFile.write("\n===============================================================\n\n")

  
  for line in passFile.readlines():
 
    try :

      username = line.split(':')[0]  
      password = line.split(':')[1]  

    except Exception, e :

      print "Exception:", e
      return

    if password != '!' and password != 'x' and password != '*' and password != 'X':
      print OKBLUE + "[*] Cracking Password - "+ password + " For user - " + username + ENDC
      #crackPass(line.strip('\n'))
      pwWord = crackPass(password)
      if pwWord:
        time = str(datetime.today() - now)
        print OKGREEN + "[+] Found Password: "+pwWord+" User:"+username+" Crypt Pass:"+password+" Time:" + time + "\n" + ENDC
        outFile.write("[+] Found Password: "+pwWord+" User:"+username+" Crypt Pass:"+password+" Time:" + time + "\n")
        outFile.flush()
      else:
        print FAIL + "[-] Password Not Found : "+password+"\n" + ENDC

  passFile.close()
  outFile.write("\n===============================================================\n\n")
  outFile.close()




def processCfile(cFilename):

  ''' Open passed in character substitiution file go line by line building the pw_swap_dict dictionary struct '''

  # Open the password file that holds the encrypted passwords
  try :
    cFile = open(cFilename, 'r')
  except Exception, e:
    print "Exception:", e

  global pw_swap_dict
  pw_swap_dict = {}

  for line in cFile.readlines():

    key = line.strip('\n').split(':')[0]
    for i in line.strip('\n').split(':')[1:]:
      if key in pw_swap_dict:
        pw_swap_dict[key].append(i)
      else:
        pw_swap_dict[key] = [i]

  cFile.close()





def main():

  parser = argparse.ArgumentParser()

  parser.add_argument("-p","--pwfile", default="shadow", help="password file to process")
  #parser.add_argument("-p","--pwfile", required=True, default="shadow", help="password file to process")
  parser.add_argument("-d","--dfile", help="dictionary file to use", default="dictionary.txt")
  parser.add_argument("-c","--cfile", help="character substitution file to use", default="None")
  parser.add_argument("-o","--resultfile", help="File correct password guesses are written to",
default="foundpasswords.txt")
  args = parser.parse_args()


  if args.cfile != "None":
    processCfile(args.cfile)


  #processPassFile('./shadow')
  processPassFile(args.pwfile, args.resultfile)




if __name__ == '__main__':
   main()

