import re 
import sys

sys.stdout = open('prueba.txt','w')
with open('servers.data','r',encoding='utf-8') as sv:
    for l in sv:
        try:
            sel = l.replace(re.search(r'motd: [^|]+',l).group(0),'')
            print(sel.strip())
        except: continue