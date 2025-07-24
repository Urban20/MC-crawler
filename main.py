from mcserver import  *
from data import *


c = Crawler(tag="minecraft")
c1 = Crawler(tag="A+Minecraft+Server")

info1 = c.info()
info2 = c1.info()

for x in info1 :
    print(x)
for x in info2:
    print(x)