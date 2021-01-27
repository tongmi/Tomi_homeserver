#File Tomi_Encoding.py
#Tomi_Encoding Module on Linux
#Version:0.1
#Producer:Qinian
#QQ:3343977167
#codes list
codelist=r"abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#encodding list
encodinglist=r"8asfDghjklwertyuiopmnbzxcvqZX0VBN3ASdFGHJKLP9WERTYUIO"
#Functions
def encode(code):
    lenth=len(code)
    encoded=""
    for i in range(0,lenth):
        try:
            buf=codelist.index(code[i])
            encoded=encoded+encodinglist[buf]
        except:
            encoded=encoded+code[i]
    return encoded
def decode(encoding):
    lenth=len(encoding)
    code=""
    for i in range(0,lenth):
        try:
            buf=encodinglist.index(encoding[i])
            code=code+codelist[buf]
        except:
            code=code+encoding[i]
    return code
