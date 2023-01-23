from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass



def AsyncSessionFromInfo(info):
    print('obsolete function used AsyncSessionFromInfo, use withInfo context manager instead')
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#
import datetime


#user GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonsForUser_
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id) # jestlize rozsirujete, musi byt tento vyraz
    
    @strawberryA.field(description="""PlannedLessons""")
    async def plans(self, info: strawberryA.types.Info)->typing.List['PlannedLessonGQLModel']:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonsForUser_(session,  self.id)
            return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result

#group GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonsForGroup_
@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""PlannedLessons""")
    async def plans(self, info: strawberryA.types.Info)->typing.List['PlannedLessonGQLModel']:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonsForGroup_(session,  self.id)
            return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    

#facility GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonsForFacility_
@strawberryA.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return FacilityGQLModel(id=id) 

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""PlannedLessons""")
    async def plans(self, info: strawberryA.types.Info)->typing.List['PlannedLessonGQLModel']:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonsForFacility_(session,  self.id)
            return result


#event GQL
from gql_plannedlessons.GraphResolvers import resolverPlansForEvent
@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id) 

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""list of plans that has the same event""")
    async def plans(self, info: strawberryA.types.Info)->typing.List['PlannedLessonGQLModel']:
        result = await resolverPlansForEvent(AsyncSessionFromInfo(info), self.id)
        return result
        


#plannedLessons GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonById, resolvePlannedLessonPage ,resolveUserLinksForPlannedLesson, resolveGroupLinksForPlannedLesson, resolveFacilityLinksForPlannedLesson
from gql_plannedlessons.GraphResolvers import resolveUnavailablePLsForPlannedLesson, resolveUnavailableUsersForPlannedLesson, resolveUnavailableFacilitiesForPlannedLesson
@strawberryA.federation.type(keys=["id"], description="""Entity representing a planned lesson for timetable creation""")
class PlannedLessonGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result 
          
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""""")
    async def users(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        result = await resolveUserLinksForPlannedLesson(AsyncSessionFromInfo(info),self.id)
        result2 = [UserGQLModel(id=item.user_id) for item in result]
        return result2

    @strawberryA.field(description="""""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]: 
        result = await resolveGroupLinksForPlannedLesson(AsyncSessionFromInfo(info),self.id)
        result2 = [GroupGQLModel(id=item.group_id) for item in result]
        return result2

    @strawberryA.field(description="""""")
    async def facilities(self, info: strawberryA.types.Info) -> List["FacilityGQLModel"]: 
        result = await resolveFacilityLinksForPlannedLesson(AsyncSessionFromInfo(info),self.id)
        result2 = [FacilityGQLModel(id=item.facility_id) for item in result]
        return result2

    @strawberryA.field(description="""""")
    async def unavailablePlans(self, info: strawberryA.types.Info)->typing.List['UnavilablePlanGQLModel']:
        result = await resolveUnavailablePLsForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result
    
    @strawberryA.field(description="""""")
    async def unavailableUsers(self, info: strawberryA.types.Info)->typing.List['UnavilableUserGQLModel']:
        result = await resolveUnavailableUsersForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result
    
    @strawberryA.field(description="""""")
    async def unavailableFacilities(self, info: strawberryA.types.Info)->typing.List['UnavilableFacilityGQLModel']:
        result = await resolveUnavailableFacilitiesForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result


#unavilablePlan GQL
from gql_plannedlessons.GraphResolvers import resolveUnavailablePLById 
@strawberryA.federation.type(keys=["id"],description="""Unavailable pLan""")
class UnavailablePlanGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveUnavailablePLById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Plan that unavailable""")
    async def plan(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result



#unavailableUser GQL
from gql_plannedlessons.GraphResolvers import resolveUnavailableUserById 
@strawberryA.federation.type(keys=["id"],description="""Unavailable users""")
class UnavailableUserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveUnavailableUserById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Plan that unavailable""")
    async def plan(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result


#unavailableFacility GQL 
from gql_plannedlessons.GraphResolvers import resolveUnavailableFacilityById 
@strawberryA.federation.type(keys=["id"],description="""Unavailable facilities""")
class UnavailableFacilityGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveUnavailableFacilityById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Plan that unavailable""")
    async def plan(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

#Query
from gql_plannedlessons.GraphResolvers import resolveUserById, resolveUserAll, resolveGroupById, resolveGroupAll,resolveFacilityById, resolveFacilityAll
from gql_plannedlessons.GraphResolvers import resolveEventById,resolveEventAll
from gql_plannedlessons.GraphResolvers import  resolveUnavailablePLAll, resolveUnavailableUserAll, resolveUnavailableFacilityAll

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    #planned lesson
    @strawberryA.field(description="""Finds a lesson by id""")
    async def planned_lesson_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all lessons""")
    async def planned_lesson_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[PlannedLessonGQLModel]:
        result = await resolvePlannedLessonPage(AsyncSessionFromInfo(info), skip, limit)
        return result

    #user
    @strawberryA.field(description="""Finds a User by id""")
    async def user_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserGQLModel,None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all Users""")
    async def user_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UserGQLModel]:
        result = await resolveUserAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #group
    @strawberryA.field(description="""Finds a Group by id""")
    async def group_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[GroupGQLModel,None]:
        result = await resolveGroupById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all Groups""")
    async def group_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[GroupGQLModel]:
        result = await resolveGroupAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #facility
    @strawberryA.field(description="""Finds a Facility by id""")
    async def facility_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[FacilityGQLModel,None]:
        result = await resolveFacilityById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all Facilites""")
    async def facility_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[FacilityGQLModel]:
        result = await resolveFacilityAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #event
    @strawberryA.field(description="""Finds a Event by id""")
    async def event_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventGQLModel,None]:
        result = await resolveEventById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all Events""")
    async def event_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[EventGQLModel]:
        result = await resolveEventAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #unavailable planned lesson
    @strawberryA.field(description="""Finds an unavailable planned lesson by id""")
    async def unavailable_plan_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[UnavailablePlanGQLModel,None]:
        result = await resolveUnavailablePLById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all unavailable planned lessons""")
    async def unavailable_plan_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UnavailablePlanGQLModel]:
        result = await resolveUnavailablePLAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #unavailable user
    @strawberryA.field(description="""Finds an unavailable user by id""")
    async def unavailable_user_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[UnavailableUserGQLModel,None]:
        result = await resolveUnavailableUserById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all unavailable users""")
    async def unavailable_user_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UnavailableUserGQLModel]:
        result = await resolveUnavailableUserAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #unavailable facility
    @strawberryA.field(description="""Finds an unavailable facility by id""")
    async def unavailable_facility_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[UnavailableFacilityGQLModel,None]:
        result = await resolveUnavailableUserById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all unavailable facilities""")
    async def unavailable_facility_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UnavailableFacilityGQLModel]:
        result = await resolveUnavailableUserAll(AsyncSessionFromInfo(info), skip, limit)
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))