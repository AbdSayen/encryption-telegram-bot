import telebot
import base64
from config import key

bot = telebot.TeleBot(key)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(
            message.chat.id, 
            "👋 Добро пожаловать в Шифровальню!\n\n"
            "🔒 *Выберите действие:*\n"
            "1️⃣ - Создать шифр\n"
            "2️⃣ - Расшифровать шифр\n"
            "3️⃣ - Подробнее о программе",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при отправке сообщения. Попробуйте еще раз")
        print(f"Error in start_message: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if message.text == "1":
            msg = bot.send_message(message.chat.id, "📝 Введите текст для шифровки:")
            bot.register_next_step_handler(msg, get_text_to_encrypt)
        elif message.text == "2":
            msg = bot.send_message(message.chat.id, "🛠 Введите шифр для расшифровки:")
            bot.register_next_step_handler(msg, get_cipher_to_decrypt)
        elif message.text == "3":
            show_details(message)
        else:
            bot.send_message(message.chat.id, "⚠️ Неверный выбор. Пожалуйста, попробуйте снова")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Что-то пошло не так. Попробуйте еще раз")
        print(f"Error in handle_message: {e}")

def get_text_to_encrypt(message):
    try:
        text = message.text
        msg = bot.send_message(message.chat.id, "🔑 Введите ключ-слово для шифрации:")
        bot.register_next_step_handler(msg, lambda m: create_cipher(m, text))
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при вводе текста для шифровки. Попробуйте еще раз")
        print(f"Error in get_text_to_encrypt: {e}")

def create_cipher(message, text):
    try:
        key = message.text
        cipher_text = encrypt(text, key)
        bot.send_message(
            message.chat.id, 
            f"🔐 *Ваш шифр:* `{cipher_text}`\n\n"
            "🔄 Вы можете расшифровать его, выбрав пункт 2",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при создании шифра. Попробуйте еще раз")
        print(f"Error in create_cipher: {e}")

def get_cipher_to_decrypt(message):
    try:
        cipher_text = message.text
        msg = bot.send_message(message.chat.id, "🔑 Введите ключ-слово для расшифровки:")
        bot.register_next_step_handler(msg, lambda m: decrypt_cipher(m, cipher_text))
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при вводе шифра для расшифровки. Попробуйте еще раз")
        print(f"Error in get_cipher_to_decrypt: {e}")

def decrypt_cipher(message, cipher_text):
    try:
        key = message.text
        decrypted_text = decrypt(cipher_text, key)
        bot.send_message(
            message.chat.id, 
            f"📝 *Расшифрованный текст:* `{decrypted_text}`",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при расшифровке текста. Попробуйте еще раз")
        print(f"Error in decrypt_cipher: {e}")

def show_details(message):
    try:
        bot.send_message(
            message.chat.id, 
            "ℹ️ *О программе*\n\n"
            "Эта программа позволяет зашифровать и расшифровать текст с использованием ключевого слова\n"
            "🔄 Для шифровки используется перемещение символов на основе ключевого слова\n"
            "💬 Шифр отображается латиницей\n\n"
            "💬 Связь с разработчиком: @abdurrsss",
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка при отображении информации о программе. Попробуйте еще раз")
        print(f"Error in show_details: {e}")

def encrypt(text, key):
    try:
        result = []
        for i in range(len(text)):
            c = text[i]
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(c) + ord(key_char))
            result.append(encrypted_char)
        encrypted_text = ''.join(result)
        return convert_to_base64(encrypted_text)
    except Exception as e:
        print(f"Error in encrypt: {e}")
        return "⚠️ Ошибка при шифровании текста"

def decrypt(cipher_text, key):
    try:
        decoded_text = convert_from_base64(cipher_text)
        result = []
        for i in range(len(decoded_text)):
            c = decoded_text[i]
            key_char = key[i % len(key)]
            decrypted_char = chr(ord(c) - ord(key_char))
            result.append(decrypted_char)
        return ''.join(result)
    except Exception as e:
        print(f"Error in decrypt: {e}")
        return "⚠️ Ошибка при расшифровке текста"

def convert_to_base64(text):
    try:
        text_bytes = text.encode('utf-8')
        return base64.b64encode(text_bytes).decode('utf-8')
    except Exception as e:
        print(f"Error in convert_to_base64: {e}")
        return "⚠️ Ошибка при конвертации в Base64"

def convert_from_base64(base64_text):
    try:
        text_bytes = base64.b64decode(base64_text)
        return text_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error in convert_from_base64: {e}")
        return "⚠️ Ошибка при конвертации из Base64"

bot.polling()
