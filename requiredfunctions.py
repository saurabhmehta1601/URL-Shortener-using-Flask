from random import randint
import string
import re

def createid():
    id=''
    chars=string.printable[:62]
    for i in range(6):
        char=chars[randint(0,61)]
        id+=char
    return id


def isLink(link):
    pattern=re.compile('https?://(w{3}\.)?\w+\.\w+')
    if(str(pattern.match(link))=="None"):
        return False
    else:
        return True

