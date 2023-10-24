import banmian
path="./1.jpg"
res=banmian.BanMian(path)
f=open('./res.txt','w+')
for i in res:
    print(i)
    f.write(i)
f.close()
    