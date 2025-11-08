import os
import typing


DB_UTILS_RETRIES_NUMBER: typing.Final = int(os.getenv("DB_UTILS_RETRIES_NUMBER", "3"))
