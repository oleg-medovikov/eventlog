from pandas import DataFrame, to_datetime
import requests
from datetime import datetime, timedelta

from clas import User
from conf import GORZDRAV_API

col_dict = {
    'date': 'Дата',
    'idDocumentMis': 'Номер документа в МИС',
    'status': 'status',
    'result': 'результат',
    'emdTypeName': 'Тип ЭМД',
        }


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
        df['date'] = to_datetime(df['date']).dt.strftime('%Y-%m-%d  %H:%M')
        d = DataFrame()
        for key, value in col_dict.items():
            d[value] = df[key]
        return d

    else:
        return DataFrame()
