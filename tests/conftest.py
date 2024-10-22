import asyncio
import sys
from datetime import datetime

import pytest

from monitoring_bot.database import Base


class TestBase:

    @pytest.fixture(scope="session")
    def init_database(self):
        return Base.metadata.create_all()

    @pytest.fixture()
    def user_id(self):
        return 11111

    @pytest.fixture()
    def user_id_to_update(self):
        return 22222

    @pytest.fixture()
    def user_id_to_delete(self):
        return -11111

    @pytest.fixture()
    def username(self):
        return 'username'

    @pytest.fixture()
    def enter_date(self):
        return datetime.strptime('2020-01-27 12:12:12', '%Y-%m-%d %H:%M:%S')

    @pytest.fixture()
    def status(self):
        return 'member'

    @pytest.fixture()
    def new_user(self, user_id, username, enter_date, status):
        return dict(user_id=user_id, username=username, enter_date=enter_date, status=status)

    @pytest.fixture()
    def user_to_update(self, user_id_to_update, username, enter_date, status):
        return dict(user_id=user_id_to_update, username=username, enter_date=enter_date, status=status)

    @pytest.fixture()
    def user_to_delete(self, user_id_to_delete, enter_date, status):
        return dict(user_id=user_id_to_delete, username='to_delete', enter_date=enter_date, status=status)
