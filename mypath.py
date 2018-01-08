import os
myf = os.path.realpath(__file__)

last = 0
for n in range(len(myf)):
    if myf[n] == '/':
        last = n

dirpath = myf[:last + 1] 
