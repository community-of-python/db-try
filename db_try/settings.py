import os
import typing


DB_TRY_RETRIES_NUMBER: typing.Final = int(os.getenv("DB_TRY_RETRIES_NUMBER", "3"))
