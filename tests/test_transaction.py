import contextlib
import typing

import pytest
from sqlalchemy.ext import asyncio as sa_async

from db_try import Transaction


@pytest.fixture
async def transaction(async_engine: sa_async.AsyncEngine) -> typing.AsyncIterator[Transaction]:
    async with sa_async.AsyncSession(async_engine, expire_on_commit=False, autoflush=False) as session:
        yield Transaction(session=session)


@pytest.fixture
async def transaction_serializable(async_engine: sa_async.AsyncEngine) -> typing.AsyncIterator[Transaction]:
    async with sa_async.AsyncSession(async_engine, expire_on_commit=False, autoflush=False) as session:
        yield Transaction(session=session, isolation_level="SERIALIZABLE")


async def test_transaction_with_commit(transaction: Transaction) -> None:
    async with transaction:
        assert transaction.session.in_transaction()
        await transaction.commit()
        assert not transaction.session.in_transaction()


async def test_transaction_serializable_with_commit(transaction_serializable: Transaction) -> None:
    async with transaction_serializable:
        assert transaction_serializable.session.in_transaction()
        await transaction_serializable.commit()
        assert not transaction_serializable.session.in_transaction()


async def test_transaction_with_rollback(transaction: Transaction) -> None:
    async with transaction:
        assert transaction.session.in_transaction()
        await transaction.rollback()
        assert not transaction.session.in_transaction()


async def test_transaction_without_commit(transaction: Transaction) -> None:
    async with transaction:
        assert transaction.session.in_transaction()
    assert not transaction.session.in_transaction()


async def test_transaction_with_exception(transaction: Transaction) -> None:
    with contextlib.suppress(Exception):
        async with transaction:
            assert transaction.session.in_transaction()
            msg: typing.Final = "some error"
            raise Exception(msg)  # noqa: TRY002
    assert not transaction.session.in_transaction()
