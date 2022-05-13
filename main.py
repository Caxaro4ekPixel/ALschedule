import time
import telebot
from telebot import types
import sqlite3
import requests
import difflib
import xmltodict
import threading
from dateutil.parser import parse
import calendar
import io
from telegram import ParseMode
from datetime import datetime
import logging


def log(mess, log_type='info'):
    logging.basicConfig(filename='logging file.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level='INFO')
    if log_type == 'info':
        logging.info(mess)
    elif log_type == 'error':
        logging.error(mess)


bot =


@bot.message_handler(commands=['start'])
def start(message):
    log(f"send start {message.chat.id, message.chat.username, message.text}")
    if message.chat.type == 'group':
        relese_id = message.text.replace("/start ", "")
        response = requests.get(f'https://api.anilibria.tv/v2/getTitle?id={relese_id}').json()
        if "error" in response:
            bot.send_message(message.chat.id, '🧐Такого релиза не существует!🧐')
        else:
            bottons = [[types.InlineKeyboardButton(text="Да", callback_data='1')],
                       [types.InlineKeyboardButton(text="Нет", callback_data='0')]]
            bot.send_message(message.chat.id, f'Релиз: {response["names"]["ru"]}?\nID: {relese_id}',
                             reply_markup=types.InlineKeyboardMarkup(bottons))
    else:
        bot.send_message(message.chat.id,
                         'Этот бот используется в каналах! Для использования нужно прописать /start [id релиза]')


@bot.message_handler(commands=['update'])
def update(message):
    log(f"select update {message.chat.id, message.chat.username, message.text}")
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    relese_id = message.text.replace("/update ", "")
    cur.execute(f'''select * from chats where id={message.chat.id}''')
    chat = cur.fetchone()

    response = requests.get(f'https://api.anilibria.tv/v2/getTitle?id={relese_id}').json()
    if "error" in response:
        bot.send_message(message.chat.id, '🧐Такого релиза не существует!🧐')
    elif chat:
        cur.execute(f'''update chats set id_relese={relese_id} where id={message.chat.id}''')
        bot.send_message(chat_id=message.chat.id, text="✅Перезапись успешно прошла!✅")

    con.commit()
    cur.close()
    con.close()


@bot.message_handler(commands=['stop'])
def stop(message):
    log(f'send stop {message.chat.id, message.chat.username, message.text}')
    if message.chat.id in [253296124, 734264203, 1625017611]:
        bot.send_message(message.chat.id, "Bot is deactivated")
        bot.stop_bot()


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data == '1':

        con = sqlite3.connect('db.db')
        cur = con.cursor()
        cur.execute(f'''select * from chats where id={call.message.chat.id}''')
        chat = cur.fetchone()
        if chat:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Запись из этого чата уже есть, воспользуйтесь командой /update id')
        else:
            relese_id = call.message.text.split('\n')[1].replace('ID: ', '')
            cur.execute(
                f'''insert into chats (id, name, 'id_relese') values ({call.message.chat.id}, '{call.message.chat.title}', {int(relese_id)})''')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='✅Успешно добавлено!✅')

        con.commit()
        cur.close()
        con.close()

    elif call.data == '0':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Тогда перепроверь id и попробуй снова /start id')


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


def check():
    while True:
        log(f"start check new sub")
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        cur.execute('''SELECT * FROM lastReles''')

        response = requests.get(f'https://subsplease.org/rss/?t')
        dict_list = xmltodict.parse(response.text)['rss']['channel']['item']

        last_time = cur.fetchone()[1]
        list_title = []
        for i in dict_list:
            list_title.append({
                'title': i['title'],
                'link': i['link'],
                'pubDate': calendar.timegm(parse(i['pubDate']).utctimetuple()),
                'category': i['category'],
                'size': i['subsplease:size']
            })

        alerts_list = {}
        max = last_time
        for i in list_title:
            if i['pubDate'] > last_time:
                if i['pubDate'] > max:
                    max = i['pubDate']
                    cur.execute(f'''UPDATE lastReles set date={i['pubDate']} WHERE id=1''')
                a = str(i['category']).split(' ')
                a = a[0:len(a) - 2]
                a = " ".join(x for x in a)
                alerts_list[a] = []
            else:
                break

        for i in list_title:
            if i['pubDate'] > last_time:
                a = str(i['category']).split(' ')
                a = a[0:len(a) - 2]
                a = " ".join(x for x in a)
                alerts_list[a].append({
                    'series': str(i['title']).split(' ')[-3],
                    'title': i['title'],
                    'link': i['link'],
                    'pubDate': i['pubDate'],
                    'category': i['category'],
                    'size': i['size']
                })
            else:
                break

        alerts = []
        cur.execute('''SELECT * FROM relesAL''')
        releseAL = cur.fetchall()
        for i in alerts_list:
            for f in releseAL:
                if similarity(i, f[1].replace('-', ' ')) > 0.75:
                    file_list = []
                    log(f"new sub {i}")

                    temp = str(f[2]) + ' / ' + str(f[3]) + '\n\n<b>[' + str(
                        alerts_list[i][0]['series']) + ' серия]</b> | <a href="https://www.anilibria.tv/release/' + \
                           f[
                               1] + '.html">[❤️]</a> ... <a href="https://backoffice.anilibria.top/resources/release-resources/' + str(
                        f[0]) + '">[🖤]</a>'

                    temp = temp + "\n\n"
                    for j in alerts_list[i]:
                        response = requests.get(j['link'], allow_redirects=True)
                        file = io.BytesIO()
                        file.write(response.content)
                        file.seek(0, 0)
                        file.name = str(j['category']).split(' ')[-1] + '_' + str(f[2]) + '.torrent'
                        file_list.append(types.InputMediaDocument(file))

                        temp = temp + '◢◤<a href="' + j['link'] + '">[' + str(j['category']).split(' ')[
                            -1] + ' - ' + str(j['size']) + ']</a>◥◣\n'
                    temp = temp + "\n\n#NewSub"
                    alerts.append([temp, file_list, f[0]])

        cur.execute('''SELECT * FROM chats''')
        chats = cur.fetchall()
        for i in alerts:
            for f in chats:
                if i[2] == f[2]:
                    log(f"send info message in chat {f[0]} relese {f[2]}")
                    bot.send_message(f[0], i[0], parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                    bot.send_media_group(f[0], i[1])
                    cur.execute(
                        f'''update chats set time_alerts='{datetime.now()}' where id={f[0]} and id_relese={f[2]}''')

        con.commit()
        cur.close()
        con.close()
        time.sleep(300)


def getSchedule():
    while True:
        log(f"start get AL schedule")
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM relesAL')
        res = cur.fetchall()
        release_al_old = []
        for i in res:
            release_al_old.append({
                "id": i[0],
                "code": i[1],
                "name_ru": i[2],
                "name_en": i[3],
                "name_alt": i[4],
                "updated": i[5],
                "series": i[6]
            })

        response = requests.get(f'https://api.anilibria.tv/v2/getSchedule').json()
        release_al_new = []
        for i in response:
            for j in i['list']:
                release_al_new.append({
                    "id": j['id'],
                    "code": j['code'],
                    "name_ru": j['names']['ru'],
                    "name_en": j['names']['en'],
                    "name_alt": j['names']['alternative'],
                    "updated": (j['updated'] if j['updated'] is not None else -1),
                    "series": (j['type']['series'] if j['type']['series'] is not None else -1)
                })

        temp_old_id = []
        temp_new_id = []
        temp_id_rm = []

        for i in release_al_old:
            temp_old_id.append(i['id'])

        for i in release_al_new:
            temp_new_id.append(i['id'])

        for i in temp_old_id:
            if i in temp_new_id:
                temp_new_id.remove(i)
            elif i not in temp_new_id:
                temp_id_rm.append(i)

        for i in temp_id_rm:
            cur.execute(f'DELETE FROM relesAL WHERE id = {i}')

        for i in release_al_new:
            if i['id'] in temp_new_id:
                cur.execute(
                    f"""INSERT INTO relesAL (id, code, name_ru, name_en, name_alt, updated, series) VALUES ({i['id']}, "{i['code']}", "{i['name_ru']}", "{i['name_en']}", "{i['name_alt']}", {i['updated']}, {i['series']})""")
            elif not temp_new_id:
                break
        con.commit()
        cur.close()
        con.close()
        time.sleep(86400)


def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)


def checkTime():
    while True:
        con = sqlite3.connect('db.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM lastTimeUpdates')
        _time = cur.fetchone()
        response = requests.get(f'https://api.anilibria.tv/v2/getUpdates?since={_time[1]}&limit=100').json()
        if response:
            last_up = response[0]["updated"] + 1
            for i in response:
                cur.execute(f'SELECT * FROM chats WHERE id_relese = {i["id"]}')
                relese = cur.fetchone()
                if relese:
                    if relese[3]:
                        log(f"send info message timer {relese[0]}")
                        timer = datetime.fromtimestamp(i["updated"]) - datetime.strptime(relese[3],
                                                                                         '%Y-%m-%d %H:%M:%S.%f')
                        days = timer.days
                        _time = convert_to_preferred_format(timer.seconds)
                        if days >= 0:
                            # 734264203 relese[0]
                            bot.send_message(chat_id=relese[0], text=f"🕘Серия вышла за: {days} дней и {_time}🕘\n\n#Time")
            cur.execute(f'UPDATE lastTimeUpdates SET timestamp = {last_up}')
            con.commit()
            cur.close()
            con.close()
        time.sleep(5)


thread1 = threading.Thread(target=check)
thread1.start()
thread2 = threading.Thread(target=getSchedule)
thread2.start()
thread3 = threading.Thread(target=checkTime)
thread3.start()

if __name__ == '__main__':
    # try:
    bot.polling(none_stop=True)
    # except Exception as err:
    #     log(f"ERROR {Exception} and {err}", "error")
