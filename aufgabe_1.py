import sys
import re


f=open("wikilinks_en.txt",'r')



def format(line):
    if is_main_pattern(line) :
        #[[abc#dfdk|dkfl]]sjkjdk
        if is_pattern_two(line):
           # print(line)
            if "|" in line:
                s=line.rsplit("|",1)
                # abc   dkflsjkjdk
                print(hashtag_delete(delete_first_bracelet(s[0]))+'\t'+delete_last_bracelet(s[-1]),end='')
            #no |
            # abc   abcsjkjdk
            else:
                s=line.rsplit("]]",1)
                print(delete_first_bracelet(hashtag_delete(s[0]))+'\t'+delete_first_bracelet(hashtag_delete(s[0]))+''+s[-1],end='')
        #[[ajdkf#kdlf|dfkd]]
        else:
           # print(line)
            #ajdkf  dfkd
            if "|" in line:
                s=line.rsplit("|",1)
                print(delete_first_bracelet(hashtag_delete(s[0]))+'\t'+delete_last_bracelet(s[-1]),end='')
            # ajdkf  ajdkf
            else:
                print(delete_first_bracelet(hashtag_delete(line[:-3]))+'\t'+delete_last_bracelet(delete_first_bracelet(hashtag_delete(line))),end='')

    else : None


# delete "[[" by the first occurrence.
def delete_first_bracelet(line):
    return line.replace("[[",'',1)

#delete "]]" by the last occurrence.
def delete_last_bracelet(line):
    return (line[::-1].replace("]]"[::--1],'',1))[::-1]


# delete after symbol # , in a str. (only applied in the left side sep. by "|".)
def hashtag_delete(str):
    if '#' in str:
       s=str.split('#',1)
       str=s[0]
    else:str=str
    return str

# if there is a "|" in the line, get the left part.
def the_first_part(str):
    s=str.split("|",1)
    return s[0]

# if there is a "|" in the line, get the right part.
def the_second_part(str):
    s=str.split("|",1)
    return s[1]

#[[abc| ]] , [[abc]],[[abc]]ss,[[\example\]]
#[[abc |]] not inside
def is_main_pattern(line):
    if line.startswith("[[") and re.findall(r'\]\]',line) is not None:
        line=delete_first_bracelet(line)
        line=delete_last_bracelet(line)
       # print(line ,":")
        if "|" in line:
            s=line.rsplit("|",1)
            if re.fullmatch(r'\s',s[-1]):
                is_pattern_one=False
            else: is_pattern_one=True
              #  print("Right")
        elif "|" not in line:
             is_pattern_one=True
             #print("right")
    else: is_pattern_one=False
    return is_pattern_one

#[[abc#djfkd | fjdksaj]]ss
#[[abc ]] not inside.
def is_pattern_two(line):
    s=line.rsplit("]]")
    #print(s)
    if re.fullmatch(r'\n',s[-1]):
         is_pattern_two=False
    else: is_pattern_two=True
    return is_pattern_two


with open('output.txt', 'w+') as outFile:
    sys.stdout = outFile
    for line in f:
        format(line)




