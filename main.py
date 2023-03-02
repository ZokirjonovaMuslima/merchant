from datetime import datetime

import bcrypt
import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from config import host, user, password, db_name

BOT_TOKEN = '5964724280:AAHxU0BMh-YTfYy9Pf5tKBbzpLYM_XmyQTs'
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
d = {}
d_m = {}
h = {}
p = {}


class Form(StatesGroup):
    name = State()
    username = State()
    balance = State()
    password = State()

    merchant_name = State()
    merchant_username = State()
    merchant_balance = State()
    merchant_passsword = State()

    product_id = State()
    product_name = State()
    product_price = State()
    product_owner = State()

    # - - - - - - - - - Product - - - - - - - - - - -

    @dp.message_handler(commands=['product'])
    async def send_photo(message: types.Message):
        await message.answer('List of fruit🍎🍌')
        rkm3 = InlineKeyboardButton('Backet 🛒', callback_data='prod_apple')
        rkm6 = InlineKeyboardButton('Backet 🛒', callback_data='prod_banana')
        rkm9 = InlineKeyboardButton('Backet 🛒', callback_data='prod_bread')

        rkm5 = InlineKeyboardMarkup().add(rkm3)
        await message.answer_photo(photo=open('media/apple.jpg', 'rb'), reply_markup=rkm5,
                                   caption="Mehirga to'la qarsildoq gold olma \n 150 UZS")

        rkm8 = InlineKeyboardMarkup().add(rkm6)
        await message.answer_photo(photo=open('media/banan.jpg', 'rb'), reply_markup=rkm8,
                                   caption="Africa birinchi nav banan \n100 UZS")

        await message.answer('List of bread🍞🥖')
        rkm11 = InlineKeyboardMarkup().add(rkm9)
        await message.answer_photo(photo=open('media/bread.jpg', 'rb'), reply_markup=rkm11,
                                   caption="Qora non qo'shimcha vitaminlar bilan 500 UZS")

    @dp.callback_query_handler(lambda m: m.data.startswith('prod_'))
    async def apple_ans(call: types.CallbackQuery):
        await call.message.answer('Saved to backet')
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        print(call.from_user.id)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""select id from users where chat_id=(%s);""", (call.from_user.id, )
            )

            user_id = [i for i in cursor.fetchone()]
            cursor.execute(
                f"""select owner from product order by id desc limit 1;"""
            )
            merchant_id = [i for i in cursor.fetchone()]
            cursor.execute(
                f"""select id from product order by id desc limit 1;"""
            )
            product_id = [i for i in cursor.fetchone()]
            date_time = datetime.now()
            cursor.execute(
                f"""insert into history(client, merchant, product, create_data) values('{user_id[0]}', '{merchant_id[0]}', '{product_id[0]}', '{date_time}')"""
            )
            connection.commit()

        await call.message.answer('successful')


# - - - - - - - - - Help - - - - - - - - - - -


@dp.message_handler(commands=['help'])
async def main_menu(message: types.Message):
    await message.answer(f'Hi👋!\t{message.from_user.full_name} Welcome store🏪')
    await message.answer('If you have any problem please contact with us 208-00-00', )
    await message.answer('Если у вас есть какие-либо проблемы, пожалуйста, свяжитесь с нами 208-00-00')
    await message.answer("Agar sizda biron bir muammo bo'lsa, iltimos biz bilan bog'laning 208-00-00")


# - - - - - - - - - About - - - - - - - - - - -


@dp.message_handler(commands=['about'])
async def main_menu(message: types.Message):
    await message.answer(f'Hi👋!\t{message.from_user.full_name} Welcome store🏪')
    await message.answer('Through this bot you can find all kinds of products you need', )
    await message.answer('С помощью этого бота вы можете найти все виды товаров, которые вам нужны')
    await message.answer(
        "Ushbu bot orqali siz o'zingizga kerak bo'lgan barcha turdagi mahsulotlarni topishingiz mumkin")


# - - - - - - - - - Location - - - - - - - - - - -


@dp.message_handler(commands=['location'])
async def send_location(message: types.Message):
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Send your contact  ☎️', request_contact=True)).add(
        KeyboardButton('Send your location 🗺', request_location=True)
    )
    await message.answer('Choose button', reply_markup=markup_request)


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def hand_location(message: types.Message):
    await message.answer(
        'When you order a product, your product will be delivered within 30 minutes 🚘 move /product section')
    await message.answer(
        'При заказе товара ваш товар будет доставлен в течение 30 минут 🚘 переместить /product раздел')
    await message.answer(
        "Mahsulotga buyurtma berganingizda, mahsulotingiz 30 daqiqa ichida yetkazib beriladi 🚘 /product bo'limiga o'ting")


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def hand_contact(message: types.Message):
    await message.answer(
        'When you order a product, your product will be delivered within 30 minutes 🚘 move /product section')
    await message.answer(
        'При заказе товара ваш товар будет доставлен в течение 30 минут 🚘 переместить /product раздел')
    await message.answer(
        "Mahsulotga buyurtma berganingizda, mahsulotingiz 30 daqiqa ichida yetkazib beriladi 🚘 /product bo'limiga o'ting")


# - - - - - - - - - Main Menu - - - - - - - - - - -


@dp.message_handler(commands=['start'])
async def greet(message: types.Message):
    await message.answer(f'Hi👋!\t{message.from_user.full_name} Welcome store🏪')
    rkm1 = InlineKeyboardButton('Client💁', callback_data='client')
    rkm2 = InlineKeyboardButton('Merchant🙋', callback_data='merchant')
    rkm = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(rkm1, rkm2)
    await message.answer('Choose the button⬇', reply_markup=rkm)


# - - - - - - - - - State Client - - - - - - - - - - -

@dp.callback_query_handler(lambda c: c.data == 'client')
async def client_ans(call: types.CallbackQuery):
    await call.message.answer('Enter your full name')
    await Form.name.set()


@dp.message_handler(state=Form.name)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data(
        {"full_name": fullname}
    )

    d.update({"full_name": (message.text)})
    await message.answer("Enter your username")
    await Form.next()


@dp.message_handler(state=Form.username)
async def answer_username(message: types.Message, state: FSMContext):
    username = message.text

    await state.update_data(
        {"username": username}
    )
    d.update({"username": (message.text)})

    await message.answer("Enter sum for your balance")
    await Form.next()


@dp.message_handler(state=Form.balance)
async def answer_balance(message: types.Message, state: FSMContext):
    balance = message.text

    await state.update_data(
        {"balance": int(balance)}
    )
    d.update({"balance": int(message.text)})

    await message.answer("Enter your password")
    await Form.next()


@dp.message_handler(state=Form.password)
async def answer_password(message: types.Message, state: FSMContext):
    password_ = message.text

    await state.update_data(
        {"password": password_}
    )
    d.update({"is_client": True, "password": str(message.text), "chat_id": message.chat.id})

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    b = d.get('password').encode('utf-8')
    a = bcrypt.gensalt()

    _hash = bcrypt.hashpw(b, a).decode('utf-8')
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users(chat_id, name, username, balance, password, is_client)VALUES(%s, %s, %s, %s, %s, %s);""",
            (d.get("chat_id"), d.get("full_name"), d.get("username"), d.get("balance"), _hash, d.get("is_client")))
        connection.commit()
    make_history()
    await message.answer("Successful ✅")
    await message.answer(
        "If you want to order, send location and contact use /location command")
    await message.answer(
        "Если вы хотите заказать, отправьте местоположение и контакт с помощью /location команды")
    await message.answer(
        "Buyurtma bermoqchi bo'lsangiz, manzilni va telefon raqamini yuboring  /location buyrug'i yordamida")
    await state.finish()


# - - - - - - - - - State Merchant - - - - - - - - - - -

@dp.callback_query_handler(lambda c: c.data == 'merchant')
async def client_ans(call: types.CallbackQuery):
    await Form.merchant_name.set()
    await call.message.answer("Enter your name")


@dp.message_handler(state=Form.merchant_name)
async def answer_name_(message: types.Message, state: FSMContext):
    merchant_name = message.text
    await state.update_data(
        {"name": merchant_name}
    )

    d_m.update({"name": str(message.text)})

    await message.answer("Enter your username")
    await Form.next()


@dp.message_handler(state=Form.merchant_username)
async def answer_password_m(message: types.Message, state: FSMContext):
    merchant_username = message.text
    await state.update_data(
        {"merchant_username": merchant_username}
    )

    d_m.update({"merchant_username": (message.text)})

    await message.answer("Enter your Balance")
    await Form.next()


@dp.message_handler(state=Form.merchant_balance)
async def answer_id(message: types.Message, state: FSMContext):
    merchant_balance = message.text
    await state.update_data(
        {"merchant_balance": merchant_balance}
    )

    d_m.update({"merchant_balance": (message.text)})

    await message.answer("Enter your password")
    await Form.next()


@dp.message_handler(state=Form.merchant_passsword)
async def answer_fullname(message: types.Message, state: FSMContext):
    merchant_password = message.text

    await state.update_data(
        {"merchant_password": merchant_password}
    )
    d_m.update({"is_client": False, "merchant_password": str(message.text), "chat_id": message.chat.id})

    await message.answer("Enter your product id")
    await Form.next()


# - - - - - - - - - State Product - - - - - - - - - - -


@dp.message_handler(state=Form.product_id)
async def product(message: types.Message, state: FSMContext):
    product_id = message.text
    await state.update_data(
        {"product_id": product_id}
    )

    p.update({"Product_id": int(message.text)})

    await message.answer("Enter your product name")
    await Form.next()


@dp.message_handler(state=Form.product_name)
async def product(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(
        {"product_name": product_name}
    )

    p.update({"Product_name": str(message.text)})

    await message.answer("Enter your product price")
    await Form.next()


@dp.message_handler(state=Form.product_price)
async def product(message: types.Message, state: FSMContext):
    product_price = message.text
    await state.update_data(
        {"product_price": product_price}
    )

    p.update({"Product_price": int(message.text)})

    await message.answer("Enter your products owner")
    await Form.next()


@dp.message_handler(state=Form.product_owner)
async def product(message: types.Message, state: FSMContext):
    product_owner = message.text
    await state.update_data(
        {"product_owner": product_owner}
    )

    p.update({"Product_owner": int(message.text)})

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    b = d_m.get('merchant_password').encode('utf-8')
    a = bcrypt.gensalt()

    hash = bcrypt.hashpw(b, a).decode('utf-8')

    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users(chat_id, name, username, balance, password, is_client) VALUES (%s, %s, %s, %s, %s, %s);""",
            (d_m.get("chat_id"), d_m.get("name"), d_m.get("merchant_username"), d_m.get("merchant_balance"), hash,
             d_m.get("is_client")))
        connection.commit()

    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO product(name, price, owner)
                VALUES('{p.get("Product_name")}', '{p.get("Product_price")}','{p.get("Product_owner")}');"""
        )
        connection.commit()
    await state.finish()
    await message.answer("Successful ✅")
    await greet(message)

    # - - - - - - - - - History - - - - - - - - - - -

    make_history()


def make_history():
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""select id from users order by id desc limit 1;"""
        )
        user_id = [i for i in cursor.fetchone()]
        cursor.execute(
            f"""select owner from product order by id desc limit 1;"""
        )
        merchant_id = [i for i in cursor.fetchone()]
        cursor.execute(
            f"""select id from product order by id desc limit 1;"""
        )
        product_id = [i for i in cursor.fetchone()]
        date_time = datetime.now()
        cursor.execute(
            f"""insert into history(client, merchant, product, create_data) values('{user_id[0]}', '{merchant_id[0]}', '{product_id[0]}', '{date_time}')"""
        )
        connection.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
