import requests
import json
import config
import datetime
apikey = config.API_BSCSCAN_2
addr = '0x12f1Bdc09F46BE3E5025b233537E897A2BbdE9b9'


def get_time(ts):
    date = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y')
    H = datetime.datetime.fromtimestamp(ts).strftime('%H')
    M = datetime.datetime.fromtimestamp(ts).strftime('%M')
    S = int(H)*60*60+int(M)*60
    return date, S


def get_info(address):
    url = f'''https://api.bscscan.com/api
      ?module=account
      &action=tokentx
      &address={address}
      &page=1
      &offset=5
      &startblock=0
      &endblock=999999999
      &sort=asc
      &apikey={apikey}'''
    url = url.replace('\n   ', '')
    r = requests.get(url)
    t = json.loads(r.text)
    for i in t['result']:
        date, time = get_time(int(i['timeStamp']))
        _from = i['from']
        to = i['to']
        value = str(round(int(i['value'])/(10**(int(i['tokenDecimal']))), 2))
        tokenName = i['tokenName']
        tokenSymblo = i['tokenSymbol']
