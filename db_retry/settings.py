import os
import typing


DB_RETRY_RETRIES_NUMBER: typing.Final = int(os.getenv("DB_RETRY_RETRIES_NUMBER", "3"))
