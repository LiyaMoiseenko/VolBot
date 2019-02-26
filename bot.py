import urllib.request
import json
import telebot
import time

from bs4 import BeautifulSoup

TOKEN = '617035310:AAGoYgOTJll4RqaNm3rTytT8q9VHtEdRZ40'
bot = telebot.TeleBot(TOKEN)
CHANNEL_NAME = '-1001292979343'


def add_answer():
    try: 
        bot.send_message(CHANNEL_NAME, get_all_data(get_html('https://melbet.org/LiveFeed/Get1x2_VZip?sports=6&count=50&mode=4&cyberFlag=2&partner=8')))
    except Exception:
        pass
#         bot.send_message(CHANNEL_NAME, 'Нет прогозов')


# получение html кода с страницы
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

# перевод из html в строку, а затем в словарь данных
def get_all_data(html):
    soup = BeautifulSoup(html, 'lxml')
    date_all = soup.find('p').text.strip()
    date_all = json.loads(date_all) #str to object - словарь
    return get_value(date_all)

# получение из словаря необходимые данные
def get_value(date_all):
    for val in date_all['Value']:
        nom_set=val['SC']['CP']
        if nom_set==3 and search_in_file(val['N']): #если идет 3ий сет и сигнал игры не отправлялся
            S=val['SC']['FS'] #массив - победы в сетах
            if 'S1' in S and 'S2' in S and S['S1']==S['S2']: #если СЧЕТ 1:1
                if 'E' in val and 'E' in val and 'C' in val['E'][0] and 'C' in val['E'][1]: #если есть коэф победы
                    K=val['SC']['PS'][1]['Value'] #массив - победы в 2ом сете
                    if val['E'][0]['C']>val['E'][1]['C'] and K['S1']>K['S2']: #если коэф 1>2 и в 2ом сете очки 1>2
                        add_in_file(str(val['N']))
                        return val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П2'
                    elif val['E'][0]['C']<val['E'][1]['C'] and K['S1']<K['S2']: #если коэф 1<2 и в 2ом сете очки 1<2
                        add_in_file(str(val['N']))
                        return val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П1'

#поиск в файле игры с определенным номером
def search_in_file(nom):
    f = open('noms.txt', 'r')
    for line in f:
        if line.strip()==str(nom):
            f.close()
            return False
    f.close()
    return True

#добавление в файл номер игры
def add_in_file(nom):
    f = open('noms.txt', 'a')
    f.write(nom + '\n')
    f.close()


@bot.message_handler(commands=['add'])
def add(message):
    # get_all_data(get_html('https://melbet.org/LiveFeed/Get1x2_VZip?sports=6&count=50&mode=4&cyberFlag=2&partner=8'))
    add_answer()

def main():
    while True:
        add_answer()
        time.sleep(5)
    

if __name__ == '__main__':
    main()
