import requests
import json
import config
import datetime


def get_time(ts):
    date = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y')
    H = datetime.datetime.fromtimestamp(ts).strftime('%H')
    M = datetime.datetime.fromtimestamp(ts).strftime('%M')
    S = int(H)*60*60+int(M)*60
    return date, str(S)


def get_info(address, tok):
    if tok != 'ETH':
        url = f'''https://api.bscscan.com/api
      ?module=account
      &action=tokentx
      &address={address}
      &page=1
      &offset=5
      &startblock=0
      &endblock=999999999
      &sort=desc
      &apikey={config.API_BSCSCAN}'''
        url = url.replace('\n      ', '')
        r = requests.get(url)
        t = json.loads(r.text)
        for i in t['result']:
            to = i['to']
            tokenSymblo = i['tokenSymbol'].replace('BSC-USD', 'USDT').replace('BTCB', 'BTC')
            if to == address.lower() and tokenSymblo == tok:
                date, time = get_time(int(i['timeStamp']))
                _from = i['from']
                value = '{:.10f}'.format(int(i['value'])/(10**(int(i['tokenDecimal']))))
                value = value[0:value.find('.')+4]
                return [date, _from, to, value, tokenSymblo, time]
    else:
        url = f'''https://api.etherscan.io/api
      ?module=account
      &action=txlist
      &address={address}
      &startblock=0
      &endblock=99999999
      &page=1
      &offset=10
      &sort=desc
      &apikey={config.API_ETHERSCAN}'''
        url = url.replace('\n      ', '')
        r = requests.get(url)
        t = json.loads(r.text)
        for i in t['result']:
            to = i['to']
            if to == address.lower():
                date, time = get_time(int(i['timeStamp']))
                _from = i['from']
                value = str(int(i['value'])/(10**(len(i['value'])+2)))
                value = value[0:value.find('.')+4]
                tokenSymblo = 'ETH'
                return [date, _from, to, value, tokenSymblo, time]
