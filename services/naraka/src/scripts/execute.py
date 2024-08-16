import sys
import string

BLACKLIST  =['FLAG','cat']
# BLACKLIST = ""
# You cannot change the value of FLAG, FLAG can only be filled with sys.argv[2]
FLAG = sys.argv[2]

def security_check(user_input, blacklist):
    for bl in blacklist:
        if bl in user_input:
            return 1

if __name__ == "__main__":
    user_input = sys.argv[1]
    if(security_check(user_input,BLACKLIST)):
        print("too bads")
    else:
        try:
            user_input = eval(user_input)
        except Exception as e:
            pass
        exec(user_input)
