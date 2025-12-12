from dotenv import load_dotenv
import os
import telebot
import psycopg2

load_dotenv()
botExcursions = telebot.TeleBot(os.getenv("botKey"))

def get_cursor():
    conn = psycopg2.connect(
        dbname=os.getenv("dbname"),
        user=os.getenv("user"), 
        password=os.getenv("password"), 
        host=os.getenv("host")
    )
    return conn, conn.cursor()

user_state = {} 
user_text = {}