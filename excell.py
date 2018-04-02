#!/usr/bin/env python
#coding=UTF-8

import xlsxwriter
import cv2
img=cv2.imread('1.jpg',1)
#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
size=img.shape
print size
workbook = xlsxwriter.Workbook('hello.xlsx',{'constant_memory': True})
worksheet1 = workbook.add_worksheet('pic')
worksheet1.set_column(0,size[0],0.19)
#max row=1048576,max column='A:XFD' as 16384=0:16383 C:\Users\Public\PycharmProjects\untitled\
def xhex(a):
    if a<16:
        return ('0'+hex(a)).replace("0x",'')
    if a>=16:
        return hex(a).replace("0x",'')



for row in range(0,size[0]):
    worksheet1.set_row(row, 2.5)
    for col in range(0,size[1]):
        (b,g,r)= img[row, col]
        RGB='#'+(xhex(r)+xhex(g)+xhex(b))
        #print RGB
        format = workbook.add_format()
        # format.set_pattern(1)
        format.set_bg_color(RGB)
        worksheet1.write_blank(row,col,None,format)


workbook.close()

print 'Done!'