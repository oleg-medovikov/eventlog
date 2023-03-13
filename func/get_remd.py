from pandas import DataFrame, to_datetime
import requests
from datetime import datetime, timedelta
import re

from clas import User
from conf import GORZDRAV_API

col_dict = {
    'date': 'Дата',
    'idDocumentMis': 'Номер документа в МИС',
    'status': 'status',
    'result': 'результат',
    'emdTypeName': 'Тип ЭМД',
        }


def clear_fio_snils(df: 'DataFrame') -> 'DataFrame':
    for i in df.index:
        if 'Имя пациента' or 'СНИЛС' in df.at[i, 'result']:
            for name in re.findall(r"(?<=\[).*?(?=\])", df.at[i, 'result']):
                res = df.at[i, 'result'].replace(name, 'скрытое ИМЯ или СНИЛС')
                df.loc[i, 'result'] = res
    return df


def get_remd(USER: 'User') -> 'DataFrame':
    "отправляем запрос к апи горздрава"
    START = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    END = datetime.now().strftime('%Y-%m-%d')

    body = {
        "dateBegin":         START + "T21:00:00.000Z",
        "dateEnd":           END + "T20:59:59.999Z",
        "oidMo":             [USER.org_code],
        "pageSize":          100,
        "currentPageNumber": 0,
        "tableType":         "REMD",
            }
    res = requests.post(GORZDRAV_API, json=body)
    if res.status_code == 200:
        df = DataFrame(data=res.json())
        df = clear_fio_snils(df)
        df['date'] = to_datetime(df['date']).dt.strftime('%Y-%m-%d  %H:%M')
        d = DataFrame()
        for key, value in col_dict.items():
            d[value] = df[key]
        return d

    else:
        df = DataFrame()
        df.loc[0, 'error'] = res.text
        return df
