from datetime import datetime

import pytest

from .conftest import TestBase
from monitoring_bot.database import Database


class TestDatabase(TestBase):

    @pytest.mark.asyncio
    async def test_create_user(self, new_user):
        status = await Database.insert_into_users(**new_user)
        assert status == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('attribute_name', 'attribute_value', 'method_to_compare', 'expected_value'),
        (
            ('user_id', pytest.lazy_fixture('user_id'), '__eq__', 1),
            ('username', pytest.lazy_fixture('username'), '__ge__', 1),
            ('enter_date', pytest.lazy_fixture('enter_date'), '__ge__', 1),
            ('status', pytest.lazy_fixture('status'), '__ge__', 1),
        )
    )
    async def test_select_user(self, attribute_name, attribute_value, method_to_compare, expected_value):
        result = await Database.select_from_users(where={attribute_name: attribute_value})
        compare = getattr(len(result), method_to_compare)
        assert compare(expected_value)
        user = result[0]
        assert getattr(user, attribute_name) == attribute_value

    @pytest.mark.asyncio
    async def test_select_all_users(self):
        result = await Database.select_from_users()
        assert isinstance(result, list)
        assert len(result) >= 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ('column', 'value'),
        (
            ('status', 'left'),
            ('status', 'banned'),
            ('status', 'member'),
            ('leave_date', datetime.strptime('2024-01-27 10:10:00', '%Y-%m-%d %H:%M:%S')),
            ('enter_date', datetime.strptime('2021-02-05 23:59:59', '%Y-%m-%d %H:%M:%S')),
            ('username', 'random_username'),
            ('has_chat_with_bot', True),
            ('has_chat_with_bot', False),
        )
    )
    async def test_update_user(self, user_id, column, value):
        operation_success = await Database.update_user(user_id=user_id, **{column: value})
        assert operation_success is True

    @pytest.mark.asyncio
    async def test_drop_user(self, user_id):
        operation_status = await Database.delete_user(user_id)
        assert operation_status is True
