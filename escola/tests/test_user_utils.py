#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 19:01.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import pytest
from mixer.backend.django import mixer

from escola import user_utils
from django.contrib.auth.models import User, Group



@pytest.fixture()
def user(db):
    return mixer.blend(User)

class TestUserGiveAdmin:
    @pytest.fixture('class')
    def user_after(self, user):
        """
        :param User user:
        :return: User
        """
        user_utils.give_admin(user)
        return user

    def test_user_is_staff_after(self, user_after):
        """

        :param User user:
        :return:
        """
        assert(user_after.is_staff is True, "O usuario deve ser marcado como staff ao ser adimin")

    def test_user_is_in_group_admin(self, user_after):
        assert user_utils.get_admin_group() in user_after.groups.all()


class TestGetAdminGroup:
    def test_get_group_is_consistent(self):
        assert user_utils.get_admin_group() == user_utils.get_admin_group()

    def test_get_group_is_instance_of_group(self):
        assert isinstance(user_utils.get_admin_group(), Group)