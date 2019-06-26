#!/usr/bin/python
import os
import boto3
import base64
import json
from botocore.exceptions import ClientError

if "AWS_REGION" in os.environ:
    region_name = os.environ['AWS_REGION']
else:
    region_name = 'us-east-1'

if "SECRET_NAME" in os.environ:
    secret_name = os.environ['SECRET_NAME']
else:
    secret_name = "mozdy/test"

def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            #print('Variable ' + k + ' tried to get replaced but wasnt found on SecretsManager')
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return secret

def replace_env_vars(secret_name, region_name):
    for sk, sv in json.loads(get_secret(secret_name, region_name)).items():
        for k, v in os.environ.items():
            if (v == "replaceme"):
                if (k == sk):
                    # Although we can write to os.environ[var], this won't be reflected in the container as an env var, exporting and running eval will do it.
                    parsedval = sv.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
                    print('export {}="{}"'.format(k, parsedval))
                    #os.environ[k] = str(sv)
                    return k + "=" + parsedval

if __name__ == '__main__':
    replace_env_vars(secret_name, region_name)
