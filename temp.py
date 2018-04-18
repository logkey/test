

ll=['123','312','xxfs','sd']

ll.append('end')
ll.insert(2,'22')
del ll[-1]

magicians = ['alice', 'david', 'carolina']
for magician in magicians:
    print(magician.title() + ", that was a great trick!")
    print("I can't wait to see your next trick, " + magician.title() + ".\n")
num=[]
for numx in range(3,31):
    if numx%3 ==0:
        num.append(numx)
print num

print num[0:3]
print num[:3]
yuanzu=('cc','1','22','333','aa')
num.sort(reverse=True)
zd={'name':'jack','age':8,'age':'tttt'}
print type(zd)
print zd['age']
