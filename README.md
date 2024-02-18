# Simple telegram chat manager
___
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram)
![Static Badge](https://img.shields.io/badge/poetry-1.7.1-darkblue)
![Static Badge](https://img.shields.io/badge/aiogram-3.3.0-blue)
![Static Badge](https://img.shields.io/badge/asyncpg-0.29.0-orange)
![Static Badge](https://img.shields.io/badge/sqlalchemy-2.0.25-red)
![Static Badge](https://img.shields.io/badge/pydantic-2.5.3-white)
![Static Badge](https://img.shields.io/badge/pytest-7.0.0-yellow)
![Static Badge](https://img.shields.io/badge/loguru-0.7.2-green)
![Static Badge](https://img.shields.io/badge/docker-24.0.7-blue)


## Installation

### 1) Add .env file to project root

#### Example of .env file
```dotenv
BOT_TOKEN=token
ADMIN_ID=123
CHAT_ID=-101
CHANNEL_ID=-102
CHANNEL_USERNAME=channel_username
MODERATOR_USERNAME=moderator_username
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhast
DB_PORT=3107

```

### 2) Run project

```commandline
docker compose up --build
```

## Architecture

```puppet
/
│   .env
│   .gitignore
│   poetry.lock
│   pyproject.toml
│   README.md
│
├───monitoring_bot
│   │   constants.py
│   │   database.py
│   │   main.py    <- base module
│   │   utils.py
│   │   __init__.py
│   │
│   └───handlers
│       │   admin.py
│       │   chat.py
│       │   filters.py
│       │   user.py
│       └───__init__.py
│
└───tests
    │   conftest.py
    │   test_database.py
    └───__init__.py

```

## Tasks:
* [X] Handle chats joins (and rejoins)
* [X] Handle channels lefts
* [X] Handle chats lefts 
* [X] Ask a people when entering a chat to make sure they are not bots 
* [X] Provide info for me about every participant of channel/chat
* [ ] Collect and send data about who react on messages (is it possible in telegram? - No)
* [X] For admin: show banned users and unban users
* [X] For admin: ban users
* [ ] For admin: receive different message types from users: docs, geo, files, etc
* [X] Deny user messages if they aren't subscribed on a channel 
