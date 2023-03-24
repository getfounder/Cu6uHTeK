import config as cfg

import gspread
from gspread_formatting import *

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
        sh = gc.create('UserInfo')
        sh.share('sibintecompany@gmail.com', perm_type='user', role='owner')
        sh = gc.open('UserInfo')
    
    
    
    worksheet = sh.sheet1

    if len(worksheet.col_values(1)) == 0:
        for key in Dict.keys():
            worksheet.update(key + '1', Dict[key])
        formating(worksheet, 1, (164, 194, 244), True, "CENTER")

        for setting in cfg.Cell_Settings:
            set_column_width(worksheet, *setting)

    id = len(worksheet.col_values(1))
    
    for key in user_data.keys():
        worksheet.update(key + f'{id + 1}', user_data[key])

    if len(user_data["I"]) * 8 > cfg.Cell_Settings[-1][-1]:
        set_column_width(worksheet, "I", len(user_data["I"]) * 8)

    if len(user_data["C"]) * 8 > cfg.Cell_Settings[-1][-1]:
        set_column_width(worksheet, "C", len(user_data["C"]) * 8)

    formating(worksheet, id + 1, cfg.Color_Settings[user_data["B"]])


def formating(worksheet, id, color, is_bold=False, align="LEFT"):

    fmt = CellFormat(
        backgroundColor=Color(*[x / 255 for x in color]),
        textFormat=TextFormat(bold=is_bold),
        horizontalAlignment=align
        )

    format_cell_range(worksheet, f'A{id}:I{id}', fmt)