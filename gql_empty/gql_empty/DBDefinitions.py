import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable
    """

    __tablename__ = 'plannedlessons'
    
    id = UUIDColumn()
    timeStart=Column(datetime)
    timeEnd=Column(datetime)


    group_id = Column(int)
    teacher_id=Column(ForeignKey('teacher.id'))
    event_id=Column(ForeignKey('event.id'))
    location_id=Column(ForeignKey('location.id'))
    subject_id=Column(ForeignKey('subject.id'))

association_table = Table(
    "association_table",
    BaseModel.metadata,
    Column("group_id", ForeignKey("plannedlessons.group_id")),
    Column("id", ForeignKey("groupstudent.id")),
)

    

class UserModel(BaseModel):
    """Defines a student in the lession
    """

    __tablename__ = 'users'

    id = UUIDColumn()
    # firstname=Column(String)
    # lastname=Column(String)
    
    # group_id=Column(ForeignKey('groupstudent.id'))

    # nameGroup=relationship('GroupStudentModel', back_populates='students')


class GroupModel(BaseModel):
    __tablename__ = 'groups'

    id=UUIDColumn()
    # name=Column(String) 
    # students=relationship('StudentModel', back_populates='nameGroup')

# class TeacherModel(BaseModel):

#     __tablename__ = 'teacher'

#     id = UUIDColumn()
#     firstname=Column(String)
#     lastname=Column(String)

#     subject_id=Column(ForeignKey('subject.id'))

#     namesubject=relationship('SubjectModel', back_populates='teachers')

class SubjectModel(BaseModel):
    __tablename__ = 'subject'

    id=UUIDColumn()
    name=Column(String)
    
    teachers=relationship('TeacherModel', back_populates='namesubject')
class LocationModel(BaseModel):
    __tablename__ = 'location'

    id= UUIDColumn()
    name=Column(String)

class EventModel(BaseModel):
    __tablename__ = 'event'

    id=UUIDColumn()
    type=Column(String)

 

  

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring