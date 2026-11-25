"""POST /hit - add one to the visit count and return the new total."""
import json
import os

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event, context):
    try:
        # ADD is atomic, so two visits at the same moment are both counted
        result = table.update_item(
            Key={"id": "site"},
            UpdateExpression="ADD visits :one",
            ExpressionAttributeValues={":one": 1},
            ReturnValues="UPDATED_NEW",
        )
        visits = int(result["Attributes"]["visits"])
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Cache-Control": "no-store"},
            "body": json.dumps({"visits": visits}),
        }
    except Exception as exc:
        print(f"Could not update the counter: {exc}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "could not update the counter"}),
        }
