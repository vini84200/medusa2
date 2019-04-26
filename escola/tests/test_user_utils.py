#  Developed by Vinicius José Fritzen
#  Last Modified 25/04/19 17:02.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import pytest
from django.contrib.auth.models import User, Group
from mixer.backend.django import mixer
from rolepermissions.checkers import has_role

from escola import user_utils
from escola.models import Turma, Profile, Aluno, Professor

pytestmark = pytest.mark.django_db


def assert_is_in_group(user, group):
    assert group in user.groups.all()


class TestUserGiveAdmin:
    @pytest.fixture()
    def user(self, db):
        return mixer.blend(User, is_staff=False)

    @pytest.fixture()
    def user_after(self, user):
        """
        :param User user:
        :return: User
        """
        user_utils.give_admin(user)
        return user

    def test_user_is_staff_after(self, user):
        """

        :param User user:
        :return:
        """
        print(user.is_staff)
        assert (user.is_staff == False)
        user_utils.give_admin(user)
        print(user.is_staff)
        assert (user.is_staff == True)

    def test_user_is_in_group_admin(self, user_after):
        assert_is_in_group(user_after, user_utils.get_admin_group())


class TestGetAdminGroup:
    def test_get_group_is_consistent(self):
        assert user_utils.get_admin_group() == user_utils.get_admin_group()

    def test_get_group_is_instance_of_group(self):
        assert isinstance(user_utils.get_admin_group(), Group)

    def test_group_name_is_admin(self):
        assert user_utils.get_admin_group().name == "Admin"


class TestCreateAdminUser:

    def test_if_user_is_created(self):
        assert isinstance(user_utils.create_admin_user('pedrozinho', '12345678'), User)

    def test_if_user_is_in_admin_group(self):
        assert user_utils.get_admin_group() in user_utils.create_admin_user('pedrozinho2', '12345678').groups.all()

    def test_if_user_is_created_with_email(self):
        assert isinstance(user_utils.create_admin_user('pedrozinho3', '12345678', email='superpetrus@gmail.com'), User)


class TestCreateAlunoUser:
    @pytest.fixture()
    def turma(self, db):
        return mixer.blend(Turma)

    @pytest.fixture()
    def user(self, turma):
        return user_utils.create_aluno_user('username', '1234567', turma, 'Pedro dos Username'), turma

    def test_have_a_Profile(self, user):
        assert isinstance(user[0].profile_escola, Profile)
        assert user[0].profile_escola.is_aluno is True
        assert user[0].profile_escola.is_professor is False

    def test_has_a_AlunoObject(self, user):
        assert isinstance(user[0].aluno, Aluno)

    def test_is_with_aluno_role(self, user):
        assert has_role(user[0], 'aluno')


class TestGetAllAlunosGroup:
    def test_all_alunos_is_consistent(self):
        assert user_utils.get_all_alunos_group() == user_utils.get_all_alunos_group()

    def test_is_instance(self):
        assert isinstance(user_utils.get_all_alunos_group(), Group)

    def test_name_its_right(self):
        assert user_utils.get_all_alunos_group().name == "Todos_Alunos"


class TestGetTurmaAlunosGroup:
    @pytest.fixture()
    def turma(self, db) -> Turma:
        return mixer.blend(Turma)

    def test_all_alunos_is_consistent(self, turma):
        assert user_utils.get_turma_alunos_group(turma.pk) == user_utils.get_turma_alunos_group(turma.pk)

    def test_is_instance(self, turma):
        assert isinstance(user_utils.get_turma_alunos_group(turma.pk), Group)

    def test_name_its_right(self, turma):
        assert user_utils.get_turma_alunos_group(turma.pk).name == f"Alunos_{turma.pk}"


class TestCreateUser:
    def test_is_instance_of(self):
        assert isinstance(user_utils.create_user('asidadovij', '123456789'), User)

    def test_has_profile(self):
        assert isinstance(user_utils.create_user('dfsdvfdf', '12345678').profile_escola, Profile)

    def test_with_email_has_profile(self):
        assert isinstance(user_utils.create_user('dfsdvfdf', '12345678', email='pefmvsv@hotmail.com').profile_escola,
                          Profile)

    def test_is_instance_of_with_email(self):
        assert isinstance(user_utils.create_user('asidadovij', '123456789', email='dkmvksnb@gmail.com'), User)

    def test_is_email_set(self):
        assert user_utils.create_user('asidadosaavij', '123456789',
                                      email='dkmvdksnb@gmail.com').email == 'dkmvdksnb@gmail.com'


class TestCreteProfessor:
    @pytest.fixture()
    def user(self):
        return user_utils.create_professor_user('username', '1234567', 'Pedro dos Username')

    def test_has_profile(self, user):
        assert isinstance(user.profile_escola, Profile)
        assert user.profile_escola.is_aluno is False
        assert user.profile_escola.is_professor is True

    def test_is_instance_off(self, user):
        assert isinstance(user, User)

    def test_is_in_group_all_professores(self, user):
        assert_is_in_group(user, user_utils.get_all_professor_group())

    def test_has_professor_object(self, user):
        assert isinstance(user.professor, Professor)


class TestGetAllProfessor:
    def test_all_professor_is_consistent(self):
        assert user_utils.get_all_professor_group() == user_utils.get_all_professor_group()

    def test_is_instance(self):
        assert isinstance(user_utils.get_all_professor_group(), Group)

    def test_name_its_right(self):
        assert user_utils.get_all_professor_group().name == "Todos_Professor"
