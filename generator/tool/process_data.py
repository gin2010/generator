# -*- coding: utf-8 -*-
# @Date : 2020-01-17
# @Author : water
# @Version  : v1.0
# @Desc  : 20200120之后可删除

import xlrd,xlwt

excel = xlwt.Workbook(encoding = 'utf-8')
sheet = excel.add_sheet('shgz')
#读
wb =xlrd.open_workbook("fpqzgz.xls")
ws = wb.sheet_by_name("sh")
max_row = ws.nrows
write_row = 1
sheet.write(0,0,"编号")
sheet.write(0,1,"规则")
sheet.write(0,2,"描述")
sheet.write(0,3,"值")
sheet.write(0,4,"结果")
sheet.write(0,5,"备注")


for row in range(max_row):
    gz = ws.cell(row,1).value
    keys_values = ws.cell(row,3).value.split("\n")
    for key_value in keys_values[1:]:
        if key_value not in ["","\r",'\n',"\r\n"]:
            print(key_value)
            key,value = key_value.split("：")
            sheet.write(write_row,2,key)
            sheet.write(write_row,3,value)
            sheet.write(write_row,1,ws.cell(row,1).value)
            sheet.write(write_row,4,ws.cell(row,4).value)
            sheet.write(write_row,5,keys_values[0])
            write_row += 1

excel.save("shgz.xls")
