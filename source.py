import config
import telebot
import stayAlive
import getCourse
import subprocess
import qiwi
import crypto
from telebot import types
import sys
bot = telebot.TeleBot(config.TOKEN_TG)

f = open('numbers.txt', 'r')
nums = f.read().split()
f.close()

tickets = ["USDT", "BTC", 'ETH', 'LTC']
currencies = ['RUB']

admin_id = [6251449399]
cur_cur = ''
cur_rate = ''
ind = 1
qiwi_dict = {}
cryp_dict = {}
process = stayAlive.start()


class User_qiwi:
    def __init__(self, amount):
        self.amount = amount
        self.were = None
        self.addr = None
        self.time = None
        self.ticker = None
        self.rate = None


class User_crypto:
    def __init__(self, amount):
        self.num = None
        self.amount = amount
        self.time = None
        self.ticker = None
        self.rate = None


def valid_phone_2(phone):
    return phone in nums


def valid_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone[0] == '7'


def valid_amount(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False


def valid_3(chat_id, msg_id, s):
    t = s.find('№')
    index = int(s[t+1:t+7])
    user = qiwi_dict[index]
    global process
    stayAlive.stop(process)
    ans = qiwi.getLastHis(user.where)
    process = stayAlive.start()
    time = ans[0].replace(' ', '').split('в')
    time[1] = time[1].split(':')
    time = [time[0], int(time[1][0])*60*60+int(time[1][1])*60]

    '##############################################################'
    if ans[3][:-1] == str(round(user.amount*user.rate*0.97, 2)) and ans[0] == user.time and 0 < (time[1]-int(user.time[1])) <= 1800:
        '#########################################################'

        s = s.replace('🔵Проверка оплаты...', '🟢Оплачено')
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=s)
        s = f'<code>{user.addr}</code>\n<code>{user.amount}</code> '+user.ticker
        bot.send_message(chat_id, '✅Ваш платеж подтвержден\nОжидайте пополнение с нашей стороны', parse_mode='html')
        for i in admin_id:
            bot.send_message(i, 'Поступил платеж\n\n' + s, parse_mode='html')
    else:
        bot.send_message(chat_id, '❌Ваш платеж не подтвержден', parse_mode='html')


def valid_1(chat_id, msg_id, s):
    t = s.find('№')
    index = int(s[t+1:t+7])
    user = cryp_dict[index]
    ans = crypto.get_info(config.ADDR, user.ticker)
    t = int(ans[5]) - int(user.time[1])

    '#############################################################'
    if user.amount == ans[3] and user.ticker == ans[4] and user.time[0] == ans[0] and 0 < t <= 1800:
        '#############################################################'

        s = s.replace('🔵Проверка оплаты...', '🟢Оплачено')
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=s)
        s = f'<code>{user.num}</code>\n<code>{round(float(user.amount)*user.rate,2)}</code> ₽'
        bot.send_message(chat_id, '✅Ваш платеж подтвержден\nОжидайте пополнение с нашей стороны', parse_mode='html')
        for i in admin_id:
            bot.send_message(i, 'Поступил платеж\n\n' + s, parse_mode='html')
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=s)
        bot.send_message(chat_id, '❌Ваш платеж не подтвержден', parse_mode='html')


@bot.callback_query_handler(func=lambda c: c.data)
def callback(callback_quary: types.CallbackQuery):
    code = callback_quary.data
    msg_id = callback_quary.json['message']['message_id']
    id = callback_quary.json['from']['id']
    s = callback_quary.json['message']['text']
    if code in ('1', '3'):
        s = s.replace('🟡Ожидает оплаты', '🔵Проверка оплаты...')
        bot.edit_message_text(chat_id=id, message_id=msg_id, text=s)
        if code == '1':
            valid_1(id, msg_id, s)
        else:
            valid_3(id, msg_id, s)
    elif code in ('2', '4'):
        s = s.replace('🟡Ожидает оплаты', '🔴Отменена')
        bot.edit_message_text(chat_id=id, message_id=msg_id, text=s)


def getHisNum(message):
    global ind
    chat_id = message.chat.id
    num = message.text
    num = num.replace(' ', '')
    if len(num) == 16:
        user = cryp_dict[ind]
        user.time = crypto.get_time(message.date)
        user.num = num
        s = f'✅<b>Заявка №{ind:06} успешно создана!</b>\n\n'
        s += '💵<b>Сумма к получению: </b>'+str(round(cur_rate*float(user.amount), 2))+' ₽'
        s += '\n🏦<b>Счет зачисления: </b>'+user.num
        s += '\n\n⏺<b>Статус заявки</b>: 🟡Ожидает оплаты\n\n'
        s += '🕐<b>Время на оплату:</b> 30 минут\n'
        s += '💵<b>Сумма к оплате:</b> <code>'+user.amount+'</code> '+cur_cur+'\n'
        s += '🏦<b>Реквизиты для оплаты: </b><code>'+config.ADDR+'</code> (в сети BEP-20)'
        in_btn_1 = types.InlineKeyboardButton('💵Оплачено', callback_data='1')
        in_btn_2 = types.InlineKeyboardButton('❌Отменить', callback_data='2')
        in_kb = types.InlineKeyboardMarkup(row_width=2)
        in_kb.add(in_btn_1, in_btn_2)
        bot.send_message(chat_id, s, parse_mode='html', reply_markup=in_kb)
        ind += 1
        cancel(message)
    else:
        if num == '❌Отменить':
            cancel(message)
        else:
            bot.send_message(chat_id, '❌Некорректный ввод\nВведите еще раз', parse_mode='html')
            bot.register_next_step_handler(message, getHisNum)


def getHisNum2(message):
    global ind
    chat_id = message.chat.id
    addr = message.text
    if addr != '❌Отменить':
        user = qiwi_dict[ind]
        user.time = crypto.get_time(message.date)
        user.ticker = cur_cur
        user.rate = cur_rate
        user.addr = addr
        s = f'✅<b>Заявка №{ind:06} успешно создана!</b>\n\n'
        s += '💵<b>Сумма к получению: </b>'+user.amount+' '+cur_cur
        s += '\n🏦<b>Счет зачисления: </b>'+user.addr
        s += '\n\n⏺<b>Статус заявки</b>: 🟡Ожидает оплаты\n\n'
        s += '🕐<b>Время на оплату:</b> 30 минут\n'
        s += '💵<b>Сумма к оплате:</b> <code>'+str(round(cur_rate*float(user.amount)*0.97, 2))+'</code> ₽\n'
        s += '🏦<b>Реквизиты для оплаты: </b><code>'+nums[ind % (len(nums))-1]+'</code>'
        user.where = nums[ind % (len(nums))-1]
        in_btn_1 = types.InlineKeyboardButton('💵Оплачено', callback_data=f'3')
        in_btn_2 = types.InlineKeyboardButton('❌Отменить', callback_data=f'4')
        in_kb = types.InlineKeyboardMarkup(row_width=2)
        in_kb.add(in_btn_1, in_btn_2)
        bot.send_message(chat_id, s, parse_mode='html', reply_markup=in_kb)
        ind += 1
        cancel(message)
    else:
        cancel(message)


mmin = ''
mmax = ''


def process_a_step(message):
    chat_id = message.chat.id
    amount = message.text.replace(',', '.')
    if valid_amount(amount) and (float(mmin) <= float(amount) <= float(mmax)):
        user = User_qiwi(amount)
        qiwi_dict[ind] = user
        msg = bot.send_message(chat_id, f'✉<b>Укажите Ваш адрес {cur_cur} для зачисления</b>', parse_mode='html')
        bot.register_next_step_handler(msg, getHisNum2)
    else:
        if amount == '❌Отменить':
            cancel(message)
        else:
            bot.send_message(chat_id, '❌Некорректный ввод\nВведите еще раз', parse_mode='html')
            bot.register_next_step_handler(message, process_a_step)


def process_amount_step(message):
    chat_id = message.chat.id
    amount = message.text
    amount = amount.replace(',', '.')
    if valid_amount(amount):
        user = User_crypto(amount)
        cryp_dict[ind] = user
        user.ticker = cur_cur
        user.rate = cur_rate
        msg = bot.send_message(chat_id, '✉<b>Укажите номер карты для зачисления</b>', parse_mode='html')
        bot.register_next_step_handler(msg, getHisNum)
    else:
        if amount == '❌Отменить':
            cancel(message)
        else:
            bot.send_message(chat_id, '❌Некорректный ввод\nВведите еще раз', parse_mode='html')
            bot.register_next_step_handler(message, process_amount_step)


def get_phone_b(message):
    global process
    chat_id = message.chat.id
    phone = message.text
    if valid_phone(phone) and valid_phone_2(phone):
        user = User_qiwi(phone)
        qiwi_dict[chat_id] = user
        stayAlive.stop(process)
        ans = qiwi.getBal(qiwi_dict[message.chat.id].phone)
        if ans:
            process = stayAlive.start()
            bot.send_message(message.chat.id, ans, parse_mode='html')
    else:
        if phone == '❌Отменить':
            cancel(message)
        else:
            bot.send_message(chat_id, 'Некорректный ввод\nВведите еще раз', parse_mode='html')
            bot.register_next_step_handler(message, get_phone_b)


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in admin_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("💱Обмен")
        btn2 = types.KeyboardButton("💰Курсы обмена")
        btn3 = types.KeyboardButton("✉Поддержка")
        markup.add(btn1, btn2, btn3)
    s = 'Вас приветствует полуавтоматический обменный пункт <b>Co1nChange!</b>\n\nУ нас вы можете быстро и выгодно обменять BTC, USDT, LTC и ETH на Российские рубли и в обратном направлении.\n\n&#128100<b>Полная анонимность!</b>\nДля совершения обмена у нас не понадобиться верефицировать карту. Обмен происходит в формате P2P, так что для банка эта операция не будет выглядеть подозрительно.\n\n&#127950<b>Высокая скорость!</b>\nВсе транзакции обрабатываются полуавтоматически. По всем направлениям обмена скорость обработки составляет до 15-20 минут.\n\n💰<b>Выгодные курсы!</b>\nМы получаем данные с бирж и мониторингов в реальном времени и всегда применяем минимальную комиссию, чтобы предлагать лучшые курсы.'
    bot.send_message(message.chat.id, s, reply_markup=markup, parse_mode='html')


def cancel(message):
    if message.from_user.id not in admin_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("💱Обмен")
        btn2 = types.KeyboardButton("💰Курсы обмена")
        btn3 = types.KeyboardButton("✉Поддержка")
        markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'ℹВозврат в главное меню', reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['exchange'])
def exchange(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('USDT')
    btn2 = types.KeyboardButton('BTC')
    btn3 = types.KeyboardButton('ETH')
    btn4 = types.KeyboardButton('LTC')
    btn5 = types.KeyboardButton('❌Отменить')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, '✉Выберите валюту, которую хотите купить или продать:', reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['support'])
def support(message):
    s = '✉Поддержка\n\nЕсли у вас возникли какие-либо сложности при работе с ботом, либо Вы хотели бы задать вопрос - наш оператор с радостью поможет Вам разобраться.\n\n@Co1nChange_help (свободный график по выходным)'
    bot.send_message(message.chat.id, s, parse_mode='html')


@bot.message_handler(commands=['rates'])
def rates(message):
    ans = getRate()
    bot.send_message(message.chat.id, ans, parse_mode='html')


def getRate():
    ans = '💰<b>Курсы обмена</b>\n\n'
    for ticket in tickets:
        for currency in currencies:
            ans += f'🔘<b>Валюта:</b> {ticket}:\n'
            price = getCourse.get_price(ticket, currency)
            ans += f'\t⬇<b>Покупка</b>: 1 {ticket} → {price}₽\n'
            ans += f'\t⬆<b>Продажа</b>: {round(price*0.97,2)}₽ → 1 {ticket}\n\n'
    return ans


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global process
    chat_id = message.chat.id
    if message.text == '💱Обмен':
        exchange(message)
    elif message.text == 'Баланс':
        msg = bot.reply_to(message, 'Баланс какого номера qiwi вывести?')
        bot.register_next_step_handler(message, get_phone_b)
    elif message.text == '💰Курсы обмена':
        rates(message)
    elif message.text == '❌Отменить':
        cancel(message)
    elif message.text == '✉Поддержка':
        support(message)
    elif message.text in tickets:
        global cur_rate
        s = '💵Выбрана валюта: '+message.text+'\n\n'
        rate = getCourse.get_price(message.text, 'RUB')
        cur_rate = rate
        s += f'\t⬇<b>Покупка</b>: 1 {message.text} → {rate}₽\n'
        s += f'\t⬆<b>Продажа</b>: {round(rate*0.97,2)}₽ → 1 {message.text}\n\n'
        s += '✉Выберите направление обмена:'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(message.text+' → RUB')
        btn2 = types.KeyboardButton('RUB → '+message.text)
        btn3 = types.KeyboardButton('❌Отменить')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, s, reply_markup=markup, parse_mode='html')
    elif ' → ' in message.text:
        global cur_cur
        tmp = message.text.replace(' → ', ' ')
        _from, to = tmp.split()
        cur_cur = to
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton('❌Отменить')
        markup.add(btn3)
        global mmin, mmax
        if 'BTC' in (_from, to):
            mmin, mmax = '0.001', '0.5'
        elif 'USDT' in (_from, to):

            '#############################################'
            mmin, mmax = '50', '4000'
            '##################################################'

        elif 'ETH' in (_from, to):

            '#################################################'
            mmin, mmax = '0.02', '1'
            '#####################################################'

        else:
            mmin, mmax = '0.5', '10'
        if _from == 'RUB':
            s = f'💵<b>Обмен российских рублей на </b>'+to+'\n\nℹ<b>Курс обмена:</b> '+str(round(cur_rate*0.97))+f'₽ → 1 {to}\n'
            s += (f'⬇<b>Минимальная сумма:</b> {mmin} '+to+f'\n⬆<b>Максимальная сумма:</b> {mmax} '+to+'\n\n')
            s += (f'✉<b>Укажите сколько {to} вы хотите купить:</b>')
            msg = bot.send_message(chat_id, s, reply_markup=markup, parse_mode='html')
            bot.register_next_step_handler(msg, process_a_step)
        else:
            cur_cur = _from
            s = f'💵<b>Обмен {_from} на российские рубли</b>\n\nℹ<b>Курс обмена:</b> '+f'1 {_from} → ' + str(cur_rate)+'₽\n'
            s += (f'⬇<b>Минимальная сумма:</b> {mmin} '+_from+f'\n⬆<b>Максимальная сумма:</b> {mmax} '+_from+'\n\n')
            s += (f'✉<b>Укажите сколько {_from} вы хотите продать:</b> (с точностью до тысячных)')
            msg = bot.send_message(chat_id, s, reply_markup=markup, parse_mode='html')
            bot.register_next_step_handler(msg, process_amount_step)


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
