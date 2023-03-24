import gspread

gc = gspread.service_account(filename="data/service_account.json")

sh = gc.create('UserInfo')
sh.share('vitalii.kupin1@gmail.com', perm_type='user', role='owner')
sh = gc.open('UserInfo')