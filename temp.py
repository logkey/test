#!/usr/bin/env python
#coding=UTF-8

aaaa=['123','sdfsfs','4342','vcbr1']
bbbb=[]
while aaaa:
    bbbb.append(aaaa.pop())
print aaaa
print sorted(bbbb)


def dog(name,type='dog'):
    print('my '+type+'\'s name is '+name)


def get_formatted_name(first_name, last_name, middle_name=''):

    if middle_name:
        full_name = first_name + ' ' + middle_name + ' ' + last_name
    else:
        full_name = first_name + ' ' + last_name
    return full_name.title()

# musician = get_formatted_name('jimi', 'hendrix')
# print(musician)
# musician = get_formatted_name('john', 'hooker', 'lee')
# print(musician)
def printchar(*get_char):
    for i in get_char:
        print (i)
printchar('a','b','v')


class Tog(object):
    def __init__(self):
        self