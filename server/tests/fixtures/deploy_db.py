from collections import UserList
import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from .orm_session import sync_session, async_session
from npg.porchdb.models import (
    Pipeline, Task, Event, Token
)
from main import app

@pytest.fixture
def minimum_data():
    'Provides one or two of everything'

    pipeline = Pipeline(
        name='ptest one',
        repository_uri='pipeline-test.com',
        version='0.3.14'
    )
    job_finder_token = Token(
        pipeline=pipeline,
        description='OpenStack host, job finder'
    )
    job_runner_token = Token(
        pipeline=pipeline,
        description='Seqfarm host, job runner'
    )
    b_event = a_event = Event(
        token=job_finder_token,
        change='Created'
    )
    tasks = [
        Task(
            pipeline=pipeline,
            events=[a_event],
            job_descriptor='aaaaaaaaa',
            definition={
                'to_do': 'stuff',
                'why': 'reasons'
            }
        ),
        Task(
            pipeline=pipeline,
            events=[b_event],
            job_descriptor='bbbbbbbbb',
            definition={
                'to_do': 'stuff',
                'why': 'reasons'
            }
        )
    ]
    entities = UserList(
            [pipeline, job_finder_token, job_runner_token, b_event, a_event])
    for t in tasks:
        entities.append(t)
    return entities


@pytest.fixture
def sync_minimum(sync_session, minimum_data):
    sync_session.add_all(minimum_data)
    sync_session.commit()
    return sync_session


@pytest_asyncio.fixture
async def async_minimum(async_session, minimum_data):
    async_session.add_all(minimum_data)
    await async_session.commit()
    return async_session


@pytest_asyncio.fixture()
async def fastapi_testclient(async_session) -> TestClient:
    '''
    Provides an uvicorn TestClient wrapping the application

    No data: Combine with another fixture to have test data, e.g.
    `def my_test(data_fixture, fastapi_testclient)`
    '''
    async with async_session.begin():
        yield TestClient(app)