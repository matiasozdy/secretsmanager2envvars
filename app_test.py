import pytest
import app
import boto3
import os
import json
from moto import mock_secretsmanager
from botocore.exceptions import ClientError
from nose.tools import assert_raises

@mock_secretsmanager
def test_get_secret_value():
    conn = boto3.client('secretsmanager', region_name='us-east-1')

    create_secret = conn.create_secret(Name='test-secret',
                                       SecretString='foosecret')
    result = app.get_secret('test-secret', 'us-east-1')
    assert result == 'foosecret'


@mock_secretsmanager
def test_secret_not_found():
    conn = boto3.client('secretsmanager', region_name='us-east-1')
    with assert_raises(app.ClientError):
        result = app.get_secret('test-nonexistent-secret', 'us-east-1')

@mock_secretsmanager
def test_getjsonfromsecrets():
    os.environ['TEST'] = 'replaceme'
    conn = boto3.client('secretsmanager', region_name='us-east-1')
    create_secret = conn.create_secret(Name='test-secret',
                                       SecretString='{"TEST": "testingChange"}')
    assert app.replace_env_vars('test-secret', 'us-east-1') == "TEST=testingChange"

def test_envvars_region():
   assert os.environ['AWS_REGION'] == 'us-east-1'

def test_envvars_sname():
   assert os.environ['SECRET_NAME'] == 'test-secret'

def test_no_envvars_region():
   del os.environ['AWS_REGION']
   assert app.region_name == 'us-east-1'

def test_no_envvars_region():
   del os.environ['SECRET_NAME']
   assert app.secret_name == 'test-secret'

