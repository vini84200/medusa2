from django.test.client import Client
import pytest
from django.utils.datetime_safe import datetime
from guardian.shortcuts import assign_perm
from escola.models import *
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.urls import reverse
from django.test.testcases import TestCase

pytestmark = pytest.mark.django_db

class TestPermissionToLider(TestCase):
    def test_doesnt_allow_two_lideres(self):
        pass