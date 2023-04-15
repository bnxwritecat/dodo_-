from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from aiogram.dispatcher import FSMContext
from pytube import YouTube
from confing import token 
import logging
import sqlite3
import time
import os

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

db_users = sqlite3.connect('users.db')
cursor_users = db_users.cursor()
cursor_users.execute("""
    CREATE TABLE IF NOT EXISTS users (
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        username VARCHAR(255),
        id_user INTEGER,
        phone_number INTEGER
    ); 
""")
cursor_users.connection.commit()

inline_buttons = [ 
    InlineKeyboardButton('Отправить номер', callback_data='number'),
    InlineKeyboardButton('Отправить местоположение', callback_data='location'),
    InlineKeyboardButton('Заказать еду', callback_data='order')
]
button = InlineKeyboardMarkup().add(*inline_buttons)

num_button = [
    KeyboardButton('Подтвердить номер', request_contact=True)
]
loc_button = [
    KeyboardButton('Подтвердить локацию', request_location=True)
]

number = ReplyKeyboardMarkup(resize_keyboard=True).add(*num_button)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(*loc_button)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}')
    await message.answer("В этом боте вы можете оставить свой заказ на пиццу.\n\nНо не забывайте оставить ваш адрес и контактный номер!!!", reply_markup=button)
    cursor_users = db_users.cursor()
    cursor_users.execute("SELECT * FROM users")
    result = cursor_users.fetchall()
    if result == []:
        cursor_users.execute(f"INSERT INTO users VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    db_users.commit()

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'number':
        await get_num(call.message)
    elif call.data == 'location':
        await get_loc(call.message)


@dp.message_handler(commands='contact')
async def get_num(message:types.Message):
    await message.answer('Подтвердите свой номер', reply_markup=number)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def add_number(message:types.Message):
    cursor = db_users.cursor()
    cursor.execute(f"UPDATE users SET phone_number = '{message.contact['phone_number']}' WHERE id_user = {message.from_user.id};")
    db_users.commit()
    await message.answer("Ваш номер успешно добавлен.",reply_markup=button)

db_address = sqlite3.connect('address.db')
cursor= db_address.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS address (
        id_user INTEGER,
        address_longtitude INTEGER,
        address_latitude INTEGER
    );
""")
cursor.connection.commit()

@dp.message_handler(commands='location')
async def get_loc(message:types.Message):
    await message.answer("Подтвердите адресс.", reply_markup=location)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def add_loc(message:types.Message):
    address = f"{message.location.longitude}, {message.location.latitude}"
    cursor = db_address.cursor()
    cursor.execute('SELECT * FROM address')
    res = cursor.fetchall()
    if res == []:
            cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    db_address.commit()
    await message.answer("Ваш адрес успешно записан", reply_markup=types.ReplyKeyboardRemove())

db_orders = sqlite3.connect('orders.db')
cursor_orders = db_orders.cursor()
cursor_orders.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        title VARCHAR(255),
        address_destination VARCHAR(255),
        date_time_order VARCHAR(255)
    );
""")
cursor_orders.connection.commit()

@dp.message_handler(text = [1,2,3,4,5,7,8,9,10,11,12,13,14,15])
async def add_order(message:types.Message):
    cursor_orders = db_orders.cursor()
    if message.text =='1':
        cursor_orders.execute(f"INSERT INTO orders VALUES('пицца 4 СЫРА', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали пиццу 4 сыра')
    elif message.text =='2':
        cursor_orders.execute(f"INSERT INTO orders VALUES('ВИНО', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали вино')
    if message.text =='3':
        cursor_orders.execute(f"INSERT INTO orders VALUES('Крылышки', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали  Крылышки')
    if message.text =='4':
        cursor_orders.execute(f"INSERT INTO orders VALUES('Куриные ножки', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали куринные ножки')
    if message.text =='5':
        cursor_orders.execute(f"INSERT INTO orders VALUES('Куриные ножки с сыром', 'None', '{time.ctime()}');")
    if message.text =='6':
            cursor_orders.execute(f"INSERT INTO orders VALUES('Куриные ножки с соусом тартар', 'None', '{time.ctime()}');")
            await message.answer('Вы заказали куринные ножки с соусом тартар')    
    if message.text =='7':
        cursor_orders.execute(f"INSERT INTO orders VALUES('шаур дош', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали шаур дош')    
    if message.text =='8':
        cursor_orders.execute(f"INSERT INTO orders VALUES('пиво', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали пиво ')    
    if message.text =='9':
        cursor_orders.execute(f"INSERT INTO orders VALUES('шаурма капченая', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали шаурму копченую')  
    if message.text =='10':
        cursor_orders.execute(f"INSERT INTO orders VALUES('курица додо', 'None', '{time.ctime()}');")
        await message.answer('курица додо')    
    if message.text =='11':
        cursor_orders.execute(f"INSERT INTO orders VALUES('пепси 1 литр', 'None', '{time.ctime()}');")
        await message.answer('пепси 1 литр')    
    if message.text =='12':
        cursor_orders.execute(f"INSERT INTO orders VALUES('спрайт 1 литр', 'None', '{time.ctime()}');")
        await message.answer('  спрайт 1 литр')    
    if message.text =='13':
        cursor_orders.execute(f"INSERT INTO orders VALUES('фанта 1 литр', 'None', '{time.ctime()}');")
        await message.answer('фанта 1 литр')    
    if message.text =='14':
        cursor_orders.execute(f"INSERT INTO orders VALUES('кола 1 литр', 'None', '{time.ctime()}');")
        await message.answer('кола 1 литр')    
    if message.text =='15':
        cursor_orders.execute(f"INSERT INTO orders VALUES('love box', 'None', '{time.ctime()}');")
        await message.answer('Вы заказали love box')    

    db_orders.commit()
    await message.reply("ожидайте еду")


executor.start_polling(dp)