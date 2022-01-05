# Copyright (c) 2021, 2022 Genome Research Ltd.
#
# Author: Kieron Taylor kt19@sanger.ac.uk
# Author: Marina Gourtovaia mg8@sanger.ac.uk
#
# This file is part of npg_porch
#
# npg_porch is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import os
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import Optional, Dict, List

from npg.porchdb.models import Pipeline as DbPipeline, Task as DbTask, Agent, Event
from npg.porch.models import Task, Pipeline

config = {
    'DB_URL': os.environ.get('DB_URL')
}

engine = create_async_engine(
    config['DB_URL'], future=True
)
session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_DbAccessor():
    'Provides a hook for fastapi to Depend on a DB session in each route'
    async with session_factory() as session:
        async with session.begin():
            yield AsyncDbAccessor(session)


class AsyncDbAccessor:
    '''
    A data access class for routine sqlalchemy operations

    Instantiate with a sqlalchemy AsyncSession
    '''

    def __init__(self, session):
        self.session = session

    async def get_pipeline(self, pipeline: Pipeline):
        if pipeline.name:

            pipeline_result = await self.session.execute(
                select(DbPipeline)
                .filter(name=pipeline.name)
            )
        else:
            pipeline_result = await self.session.execute(
                select(DbPipeline)
                .filter(repository_uri=pipeline.uri)
            )
        return pipeline_result.scalar_one().convert_to_model()

    async def get_all_pipelines(self, name: Optional[str]) -> List[Pipeline]:
        pipelines = []
        if name:
            pipelines = await self.session.execute(
                select(DbPipeline)
                .filter(name=name)
            )
        else:
            pipelines = await self.session.execute(
                select(DbPipeline)
            )

        return [pipe.convert_to_model() for pipe in pipelines.scalars().all()]

    async def get_pipeline_tasks(self, state: str) -> List[Task]:
        if (state):
            tasks = await self.session.execute(
                select(DbTask)
                .filter(state=state)
            )
        else:
            tasks = await self.session.execute(
                select(DbTask)
            )

        return [t.convert_to_model() for t in tasks.scalars().all()]

    async def create_pipeline(self, pipeline) -> Pipeline:
        session = self.session

        pipe = DbPipeline(
            name=pipeline.name,
            version=pipeline.version,
            repository_uri=pipeline.uri
        )

        session.add(pipe)
        await session.commit()
        return pipe.convert_to_model()


    async def create_task(self, agent_id: str, task: Task) -> Task:

        session = self.session
        agent_result = await session.execute(
            select(Agent)
            .filter_by(agent_id=agent_id)
        )
        agent = agent_result.scalar_one()
        pipeline_result = await session.execute(
            select(DbPipeline)
            .filter_by(repository_uri=task.pipeline.uri)
        )
        db_pipeline = pipeline_result.scalar_one()
        # Check they exist and so on
        task.state('READY')

        t = self.convert_task_to_db(task, agent, db_pipeline)
        session.add(t)

        await session.commit()
        # Error handling to follow
        return t.convert_to_model()

    async def claim_tasks(
        self, agent_id: int, pipeline: Pipeline, claim_limit: Optional[int] = 1
    ) -> List[Task]:
        session = self.session

        agent_result = await session.execute(
            select(Agent)
            .filter_by(agent_id=agent_id)
        )
        agent = agent_result.scalar_one()

        potential_runs = await session.execute(
            select(DbPipeline)
            .filter_by(repository_uri=pipeline.uri)
            .filter_by(state='READY')
            .limit(claim_limit)
        )

        runs = potential_runs.scalars().all()
        for run in runs:
            run.agent = agent
            run.state = 'CLAIMED'

        await session.commit()

        work = []
        for run in runs:
            work.append(run.convert_to_model())
        return work

    async def update_task(self, task: Task) -> Task:
        '''
        Allows the modification of state of a task.
        Other fields cannot be changed
        '''
        # Get the matching task from the DB
        pipeline_result = await self.get_pipeline(task.pipeline)
        db_pipe = pipeline_result.scalar_one()
        task_result = await self.session.execute(
            select(DbTask)
            .filter(pipeline=db_pipe)
            .filter(job_descriptor=task.generate_analysis_id())
        )
        og_task = task_result.scalar_one()
        # Check that the updated state is a valid change
        if (og_task):
            comparable_task = og_task.convert_to_model()
            if (comparable_task.task_input_id != task.task_input_id):
                raise Exception('Cannot change task definition. Submit a new task instead')
            og_task.state(task.status)
        else:
            raise Exception('Could not find task to update it')

        return og_task.convert_to_model()
