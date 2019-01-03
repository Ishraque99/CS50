import sys

if len(sys.argv) != 2:
    print("Error 1: This program accepts 1 command line argument")
    exit(1)

key = int(sys.argv[1])%26
p = str(input("plaintext: "))

for i in range(len(p)):
    c = p[i]
    if (str.isalpha(c) and str.isupper(c)):
    
        d = chr(((ord(c) - 65) + key)%26 + 65)
        print(d, end="")
        
    elif (str.isalpha(c) and str.islower(c)):
        e = chr(((ord(c) - 97) + key)%26 + 97)
        print(e, end="")
    
    else:
        print(c, end="")
print()