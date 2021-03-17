# -*- coding: utf8 -*-
import openpyxl

wb = openpyxl.load_workbook(filename = 'c:\\Users\\jazzt\\desktop\\NAM-IP\\bull.xlsm')
ws = wb['Inventaire']
none_cell = 0
value_cell = 0
zero_cell = 0
for row in ws.iter_rows(min_row=7, max_col=34, max_row=678):
    for cell in row:
      if  cell.value == None:
          none_cell = none_cell + 1
      elif cell.value == 0 :
           zero_cell  = zero_cell + 1
      else :
            value_cell = value_cell + 1

print("cell vide ", none_cell)
print("cell à zero",zero_cell)
print("cell remplie",value_cell)