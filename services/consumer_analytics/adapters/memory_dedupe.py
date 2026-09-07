import boto3
import os
import time
from botocore.exceptions import ClientError



class DynamoDedupe:
    def __init__(self, table_name: str | None = None, ttl_seconds: int = 86400 ):
        self._table = boto3.resource("dynamodb").Table(
            table_name or os.environ["DEDUPE_TABLE"]
        )
        self._ttl = ttl_seconds

    def claim(self, key: str) -> bool:
        try:
            self._table.put_item(
                Item={"pk": key, "expires_at": int(time.time())+ self._ttl},
                ConditionExpression="attribute_not_exists(pk)",
            )

            return True
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise
    