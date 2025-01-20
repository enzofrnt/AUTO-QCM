from behave import fixture, use_fixture
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.runner import DiscoverRunner
from django.test.testcases import TestCase


def before_scenario(context, scenario):
    # Nettoyer la base de données avant chaque scénario
    TestCase().setUpClass()
    
def after_scenario(context, scenario):
    # Nettoyer après chaque scénario
    TestCase().tearDownClass()