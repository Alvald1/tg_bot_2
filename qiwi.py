import getHistory
import unidecode
import stayAlive
from bs4 import BeautifulSoup


def getLastHis(phone):
    f = open('config.txt', 'r', encoding="utf-8")
    text = f.read()
    arr = [i.split() for i in text.split('\n')]
    ans = ''
    f.close()
    for i in arr:
        if i[1] == phone:
            ans = i
            break
    stayAlive.getMove(ans)
    soup = []
    date = str()
    getHistory.getHis()
    with open('tmp.txt', 'r', encoding="utf-8") as f:
        text = f.read()
        soup.append(BeautifulSoup(text, 'html.parser'))
        try:
            date = soup[0].contents[1].contents[1].contents[0].contents[2].contents[0].contents[0].contents[0].contents[1].contents[0].contents[1].contents[0].contents[0].contents[1].contents[0]
            num_from = soup[0].contents[1].contents[1].contents[0].contents[2].contents[0].contents[0].contents[0].contents[1].contents[0].contents[1].contents[0].contents[3].next_sibling.contents[1].contents[0]
            name_from = soup[0].contents[1].contents[1].contents[0].contents[2].contents[0].contents[0].contents[0].contents[1].contents[0].contents[1].contents[0].contents[3].contents[1].contents[0]
            total = soup[0].contents[1].contents[1].contents[0].contents[2].contents[0].contents[0].contents[0].contents[0].contents[0].contents[0].contents[0].contents[1].contents[0]
        except Exception:
            try:
                num_from = soup[0].contents[1].contents[1].contents[0].contents[1].contents[1].contents[0].contents[0][14:]
                total = soup[0].contents[1].contents[1].contents[0].contents[1].contents[3].next_element.contents[0].contents[0].contents[0].contents[0].contents[0].contents[0].contents[0].contents[1].contents[0]
                date = soup[0].contents[1].contents[1].contents[0].contents[1].contents[3].next_element.contents[0].contents[0].contents[0].contents[0].next_sibling.contents[0].contents[1].contents[0].contents[0].contents[1].contents[0]
                name_from = 'Аноним'
            except Exception:
                return ("Что-то пошло не так")

    return [date, num_from, name_from, unidecode.unidecode(total)[:-2]+'₽']


def getBal(phone):
    f = open('config.txt', 'r', encoding="utf-8")
    text = f.read()
    arr = [i.split() for i in text.split('\n')]
    ans = ''
    f.close()
    for i in arr:
        if i[1] == phone:
            ans = i
            break
    stayAlive.getMove(ans)
    getHistory.getBal()
    with open('bal.txt', 'r', encoding="utf-8") as f:
        text = f.read()
        return text+'₽'
