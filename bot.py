# import csv
# from datetime import datetime
# import requests
# from bs4 import BeautifulSoup


# def get_html(url):
#     response = requests.get(url)
#     return response.text #возвращает html код


# def get_all_links(html):
#     soup = BeautifulSoup(html, 'lxml')
#     try:
#         tds = soup.find('div', id='blockContent').find_all('span', class_='team').text.strip()
#     except:
#         tds = ''
#     links = []
#     for td in tds:
#         links.append(td)
#     return links


# def text_before_word(text, word):
#     line = text.split(word)[0].strip()
#     return line



# def main():
#     start = datetime.now()
#     url = 'https://melbet.org/ru/live/volleyball'
#     #all_links = get_all_links(get_html(url))
#     #for link in all_links:
#     #    print(link)
#         #html = get_html(link)
        
#         #data = get_page_data(html)
#         #write_csv(i, data)
#     html = requests.get(url).text
#     soup = BeautifulSoup(html, 'lxml')
#     timers = soup.find('h1', id='h1')

#     #for timer in timers:
#     print(timers.text.strip())

#     end = datetime.now()
#     total = end - start
#     print(str(total))
#     a = input()

# if __name__ == '__main__':
#     main()

#     g_data = soup.find_all("span", {"class", "sportIco s6"})
#     for item in g_data:
#         print(item.text)

# import csv
# import urllib.request

# from bs4 import BeautifulSoup


# BASE_URL = 'http://www.weblancer.net/projects/'


# def get_html(url):
#     response = urllib.request.urlopen(url)
#     return response.read()


# def get_page_count(html):
#     soup = BeautifulSoup(html)
#     paggination = soup.find('div', class_='pages_list text_box')
#     return int(paggination.find_all('a')[-2].text)


# def parse(html):
#     soup = BeautifulSoup(html)
#     table = soup.find('table', class_='items_list')
#     rows = table.find_all('tr')[1:]

#     projects = []
#     for row in rows:

#         cols = row.find_all('td')

#         projects.append({
#             'title': cols[0].a.text,
#             'categories': [category.text for category in cols[0].find_all('noindex')],
#             'price': cols[1].text.strip().split()[0],
#             'application': cols[2].text.split()[0]
#         })

#     return projects

# def save(projects, path):
#     with open(path, 'w') as csvfile:
#         writer = csv.writer(csvfile)

#         writer.writerow(('Проект', 'Категории', 'Цена', 'Заявки'))

#         writer.writerows(
#             (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
#         )

# def main():
#     total_pages = get_page_count(get_html(BASE_URL))

#     print('Всего найдено %d страниц...' % total_pages)

#     projects = []

#     for page in range(1, total_pages + 1):
#         print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
#         projects.extend(parse(get_html(BASE_URL + "page=%d" % page)))

#     print('Сохранение...')
#     save(projects, 'projects.csv')



import urllib.request
import json
import telebot
import time

from bs4 import BeautifulSoup

TOKEN = '617035310:AAGoYgOTJll4RqaNm3rTytT8q9VHtEdRZ40'
bot = telebot.TeleBot(TOKEN)
CHANNEL_NAME = '-1001292979343'

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def add_answer(message):
def add_answer():
     # bot.send_message(message.chat.id, "Введите расписание для " )
    try: 
#         print('Нет 12')
        # bot.send_message(message.chat.id, get_all_data(get_html('https://melbet.org/LiveFeed/Get1x2_VZip?sports=6&count=50&mode=4&cyberFlag=2&partner=8')))
        bot.send_message(CHANNEL_NAME, get_all_data(get_html('https://melbet.org/LiveFeed/Get1x2_VZip?sports=6&count=50&mode=4&cyberFlag=2&partner=8')))
    except Exception:
        pass
        # print('Нет 1200')
        # # bot.send_message(message.chat.id, 'Нет прогозов')
        bot.send_message(CHANNEL_NAME, 'Нет прогозов')

    # bot.register_next_step_handler(sent, hello)


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
                    # print(val['N'])
                    K=val['SC']['PS'][1]['Value'] #массив - победы в 2ом сете
                    if val['E'][0]['C']>val['E'][1]['C'] and K['S1']>K['S2']: #если коэф 1>2 и в 2ом сете очки 1>2
                        # bot.send_message(message.chat.id, 'Как тебя зовут1?')
                        # add_answer
                        # print(val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П2')
                        add_in_file(str(val['N']))
                        return val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П2'
                    elif val['E'][0]['C']<val['E'][1]['C'] and K['S1']<K['S2']: #если коэф 1<2 и в 2ом сете очки 1<2
                        # bot.send_message(message.chat.id, 'Как тебя зовут2?')
                        # add_answer
                        # print(val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П1')
                        add_in_file(str(val['N']))
                        return val['L']+'\n'+str(val['N'])+'\n'+val['O1']+' - '+val['O2']+'\n'+val['SC']['CPS']+ ' П1'
        #         elif return str('Нет')
        #     elif return str('Нет счета 1:1')
        # elif return str('Нет 3го сета')

#поиск в файле игры с определенным номером
def search_in_file(nom):
    f = open('noms.txt', 'r')
    for line in f:
        if set(line.split(' '))==set(nom.split(' ')):
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
    # try: 
    #     bot.polling(none_stop=True, interval=5)
    # except Exception:
    #     pass
    # if not SINGLE_RUN:
    while True:
        add_answer()
        time.sleep(5)
    

if __name__ == '__main__':
    main()
