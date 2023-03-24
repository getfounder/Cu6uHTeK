import gspread

gc = gspread.service_account()
sh = gc.open('Test')
sh.share('sibintecompany@gmail.com', perm_type='user', role='writer')
worksheet = sh.sheet1

d = {
    'A' : '123123',
    'B' : 'NAme',
    'C' : 'Numb'
}
for a in d.keys():
    worksheet.update(a+'2', d[a])

print(worksheet.get('A1'))
print(worksheet.get('B1'))
print(worksheet.get('C1'))
