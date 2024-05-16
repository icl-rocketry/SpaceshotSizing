import xlwings as xw

wb = xw.Book('HalfCatSim_v1.3.4.xlsx')
sheet = wb.sheets['Motor Simulation']
#print(f"Ox Disp = {sheet['G6'].value}")
tank_OD = 7
sheet['G3'].value = tank_OD
sheet['K4'].value = tank_OD
print(f"For tank OD {tank_OD}, Impulse = {sheet['O18'].value}")
tank_OD = 6.5
sheet['G3'].value = tank_OD
sheet['K4'].value = tank_OD
print(f"For tank OD {tank_OD}, Impulse = {sheet['O18'].value}")
wb.close()