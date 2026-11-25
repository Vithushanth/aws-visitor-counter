import importlib
import json
import os
import sys

import boto3
from moto import mock_aws

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@mock_aws
def test_counts_up():
    os.environ.update(TABLE_NAME="counter", AWS_DEFAULT_REGION="eu-west-2",
                      AWS_ACCESS_KEY_ID="test", AWS_SECRET_ACCESS_KEY="test")
    boto3.client("dynamodb").create_table(
        TableName="counter", BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
    )
    import app
    importlib.reload(app)
    first = app.handler({}, None)
    second = app.handler({}, None)
    assert first["statusCode"] == 200
    assert json.loads(first["body"]) == {"visits": 1}
    assert json.loads(second["body"]) == {"visits": 2}
