import gspread

Dict = {
    'A': 'ID',
    'B': 'Категория',
    'C': 'ФИО Участника',
    'D': 'Номер телефона',
    'E': 'Город/регион',
    "F": "Вид спорта",
    'G': "Название отеля",
    'H': "Номер комнаты",
    'I': "Приглашенные гости",
}


def add_info(user_data):
    gc = gspread.service_account(filename="data/service_account.json")

    try:
        sh = gc.open('UserInfo')
    except Exception:
        gc.create("UserInfo")
        sh = gc.open('UserInfo')
    
    sh.share('sibintecompany@gmail.com', perm_type='user', role='writer')
    
    worksheet = sh.sheet1

    if len(worksheet.col_values(1)) == 0:
        for key in Dict.keys():
            worksheet.update(key + '1', Dict[key])

    id = len(worksheet.col_values(1))
    user_data["A"] = id
    
    for key in user_data.keys():
            worksheet.update(key + f'{id + 1}', user_data[key])