import re
from os import getenv

from dotenv import load_dotenv
from loguru import logger as log


load_dotenv()

token = getenv('BOT_TOKEN')
admin_id = int(getenv('ADMIN_ID'))
chat_id = int(getenv('CHAT_ID'))
channel_id = int(getenv('CHANNEL_ID'))
channel_username = getenv('CHANNEL_USERNAME')
moderator_username = getenv('MODERATOR_USERNAME')
db_user = getenv('POSTGRES_USER')
db_password = getenv('POSTGRES_PASSWORD')
db_name = getenv('POSTGRES_DB')
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')

connection_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

log_level = "DEBUG"
log_path = "logs\\bot.log"
log_format = "{time:YYYY:MMM:DD:ddd:HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
log.add(log_path, format=log_format, colorize=True, enqueue=True, level=log_level)

check_new_member_buttons_texts = [
    "залупа", "эльф", "обезъяна", "лошадь", "будка", "черешня", "перхоть", "падаль",
    "себека", "бот", "задрот", "хейтер", "машина", "тачка", "банан", "овощ",
]

# NEW USER MESSAGES TEXT
first_bot_user_private_chat_message = (f"Для того чтобы пользоваться ботом необходимо подписаться на канал:\n\n"
                                       f"@{channel_username}")
new_user_approve_message = "Привет, @{}!\n\nПожалуйста подтверди что ты человек, нажав на соответствующую кнопку ниже"
user_passes_chat_verification_message = "Пользователь @{} прошел верификацию в чате"

# MEMBERS MESSAGES TEXT
greetings_message = "Привет, напиши мне сообщение и я перешлю его Михаилу\n\nП.С. Всякую херню не предлагать"

# BANNED / LEFT
banned_or_left_user_message = (f"В данный момент у Вас нет возможности подписаться на канал.\n\n"
                               f"Для дополнительной информации свяжитесь с @{moderator_username}")

# CHAT CALLBACK QUERIES
congratulations = "congratulations"
these_buttons_not_for_you = "This buttons not for you"
correct_new_member_answer = "correct_new_member_answer"
wrong_new_member_answer = "wrong_new_member_answer"
new_member_answer = correct_new_member_answer, wrong_new_member_answer

# ADMIN TEXTS
admin_appreciates_it = "Михаил оценил ваше сообщение: 👍"
admin_disrespects_it = "Михаил осуждает это: 👎"
admin_saw_it = "Михаил прочитал сообщение."

# ADMIN CALLBACK QUERIES
admin_thumbs_up = "admin_thumbs_up"
admin_read = "admin_read"
write_an_answer = "write_an_answer_to_user_{}"
move_to_trash = "move_to_trash"
i_want_to_ban_user = "i_want_to_ban_user_{}"
admin_thumbs_down = "admin_thumbs_down"
ban_user_query = "ban_user_{}"
cancel_ban_user = "cancel_ban_user"

# BAN USER REGEXP
ban_user_regexp = re.compile(r"^ban_user_\d+$")
want_to_ban_user_regexp = re.compile(r"^i_want_to_ban_user_\d+$")
write_an_answer_regexp = re.compile(r"^write_an_answer_to_user_\d+$")
