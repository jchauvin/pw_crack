#!/usr/bin/python

import crypt

passwords = [ "3gg", "3ggs", "passw0rd", "password", "abc123", "letmein", "p4ssw0rd" ]

def main():

  pwfile = open('password.txt', 'wb') 

  for i in passwords:
    print i
    pwfile.write(crypt.crypt(i, "HX"))
    pwfile.write("\n")

   


if __name__ == "__main__":
    main()
