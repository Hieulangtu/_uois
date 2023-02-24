from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from gql_plannedlessons.DBFeeder import predefineAllDataStructures

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
from gql_plannedlessons.GraphResolvers import resolveUnavailablesForUser, resolverPlanLinksForUser 
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

    @strawberryA.field(description="""""")
    async def unavailableUsers(self, info: strawberryA.types.Info)->typing.List['UnavailableUserGQLModel']:
        result = await resolveUnavailablesForUser(AsyncSessionFromInfo(info), self.id)
        return result
    
    @strawberryA.field(description="""""")
    async def userPlans(self, info: strawberryA.types.Info)->typing.List['UserPlanGQLModel']:
        result = await resolverPlanLinksForUser(AsyncSessionFromInfo(info), self.id)
        return result
    

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result

#group GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonsForGroup_, resolverPlanLinksForGroup
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

    @strawberryA.field(description="""""")
    async def groupPlans(self, info: strawberryA.types.Info)->typing.List['GroupPlanGQLModel']:
        result = await resolverPlanLinksForGroup(AsyncSessionFromInfo(info), self.id)
        return result
    

    

#facility GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonsForFacility_
from gql_plannedlessons.GraphResolvers import resolveUnavailablesForFacility, resolverPlanLinksForFacility
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
    
    @strawberryA.field(description="""""")
    async def unavailableFacilities(self, info: strawberryA.types.Info)->typing.List['UnavailableFacilityGQLModel']:
        result = await resolveUnavailablesForFacility(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""""")
    async def facilityPlans(self, info: strawberryA.types.Info)->typing.List['FacilityPlanGQLModel']:
        result = await resolverPlanLinksForFacility(AsyncSessionFromInfo(info), self.id)
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
        
################################################################################################################

#plannedLessons GQL
from gql_plannedlessons.GraphResolvers import resolvePlannedLessonById, resolvePlannedLessonPage ,resolveUserLinksForPlannedLesson, resolveGroupLinksForPlannedLesson, resolveFacilityLinksForPlannedLesson
from gql_plannedlessons.GraphResolvers import resolveUnavailablePLsForPlannedLesson
from gql_plannedlessons.GraphResolvers import resolveUpdatePlannedLesson
from gql_plannedlessons.GraphResolvers import resolveInsertUserPlan, resolveInsertGroupPlan, resolveInsertFacilityPlan, resolveInsertUnavailablePL
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
    
    @strawberryA.field(description="""planned lesson's name (like Informatika or Matematika)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""return user""")
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
    async def event(self, info: strawberryA.types.Info)->Union[EventGQLModel,None]:
        result = await resolveEventById(AsyncSessionFromInfo(info), self.event_id)
        return result

    
    @strawberryA.field(description="""""")
    async def groupPlans(self, info: strawberryA.types.Info)->typing.List['GroupPlanGQLModel']:
        result = await resolveGroupLinksForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""""")
    async def userPlans(self, info: strawberryA.types.Info)->typing.List['UserPlanGQLModel']:
        result = await resolveUserLinksForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""""")
    async def facilityPlans(self, info: strawberryA.types.Info)->typing.List['FacilityPlanGQLModel']:
        result = await resolveFacilityLinksForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""""")
    async def unavailablePlans(self, info: strawberryA.types.Info)->typing.List['UnavailablePlanGQLModel']:
        result = await resolveUnavailablePLsForPlannedLesson(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""Returns the planned lesson editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['PlannedLessonEditorGQLModel', None]:
        return self
    
#plannedlesson update GQL 
@strawberryA.input
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    event_id: Optional[strawberryA.ID] = None


#PlannedLesson Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable planned lesson""")
class PlannedLessonEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await PlannedLessonGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def plannedLesson(self, info: strawberryA.types.Info) -> PlannedLessonGQLModel:
        result = await PlannedLessonGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the planned lesson data""")
    async def update(self, info: strawberryA.types.Info, data: PlannedLessonUpdateGQLModel) -> "PlannedLessonEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdatePlannedLesson(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = PlannedLessonEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result
    
    @strawberryA.field(description="""Create new group plan - create group for lesson """)
    async def add_group_plan(self, info: strawberryA.types.Info, group_id: uuid.UUID) -> 'GroupPlanGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertGroupPlan(session, None, extraAttributes={ 'group_id': group_id, 'plannedlession_id': self.id})
            return result
    
    @strawberryA.field(description="""Create new user plan - create user for lesson """)
    async def add_user_plan(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'UserPlanGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertUserPlan(session, None, extraAttributes={ 'user_id': user_id, 'plannedlession_id': self.id})
            return result

    @strawberryA.field(description="""Create new facility plan - create facility for lesson """)
    async def add_facility_plan(self, info: strawberryA.types.Info, facility_id: uuid.UUID) -> 'FacilityPlanGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertFacilityPlan(session, None, extraAttributes={ 'facility_id': facility_id, 'plannedlession_id': self.id})
            return result
    
    @strawberryA.field(description="""Create new unavailable plan """)
    async def add_unavailable_plan(self, info: strawberryA.types.Info, startDate: datetime.date, endDate: datetime.date) -> 'UnavailablePlanGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertUnavailablePL(session, None, extraAttributes={ 'startDate': startDate, 'endDate':endDate, 'plannedlession_id': self.id})
            return result

################################################################################################################

#unavailablePlan GQL
from gql_plannedlessons.GraphResolvers import resolveUnavailablePLById 
from gql_plannedlessons.GraphResolvers import resolveUpdateUnavailablePL
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
    
    @strawberryA.field(description=""" reason for unavailibility (like National's day or training course)""")
    def reason(self) -> str:
        return self.reason

    @strawberryA.field(description="""Plan that unavailable""")
    async def plannedLesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result
    
    @strawberryA.field(description="""Returns the Unavailable plan editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['UnavailablePlanEditorGQLModel', None]:
        return self


#unavailable planned lesson update GQL 
@strawberryA.input
class UnavailablePlanUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    startDate: Optional[datetime.datetime] = None
    endDate: Optional[datetime.datetime] = None


#unavailable planned lesson GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable unavailable planned lesson""")
class UnavailablePlanEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await UnavailablePlanGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def unavailablePlan(self, info: strawberryA.types.Info) -> UnavailablePlanGQLModel:
        result = await UnavailablePlanGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the unavailable planned lesson data""")
    async def update(self, info: strawberryA.types.Info, data: UnavailablePlanUpdateGQLModel) -> "UnavailablePlanEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateUnavailablePL(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UnavailablePlanEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

################################################################################################################

#unavailableUser GQL
from gql_plannedlessons.GraphResolvers import resolveUnavailableUserById 
from gql_plannedlessons.GraphResolvers import resolveUserById 
from gql_plannedlessons.GraphResolvers import resolveUpdateUnavailableUser
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
    
    @strawberryA.field(description=""" reason for unavailibility (like dovolenou)""")
    def reason(self) -> str:
        return self.reason

    @strawberryA.field(description="""Information User that unavailable""")
    async def user(self, info: strawberryA.types.Info) -> Union[UserGQLModel,None]:
        result = await resolveUserById (AsyncSessionFromInfo(info), self.user_id)
        return result
    
    @strawberryA.field(description="""Returns the Unavailable User editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['UnavailableUserEditorGQLModel', None]:
        return self

#unavailable user update GQL 
@strawberryA.input
class UnavailableUserUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    startDate: Optional[datetime.datetime] = None
    endDate: Optional[datetime.datetime] = None


#unavailable User Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable unavailable user""")
class UnavailableUserEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await UnavailableUserGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def unavailableUser(self, info: strawberryA.types.Info) -> UnavailableUserGQLModel:
        result = await UnavailableUserGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the unavailable User data""")
    async def update(self, info: strawberryA.types.Info, data: UnavailableUserUpdateGQLModel) -> "UnavailableUserEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateUnavailableUser(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UnavailableUserEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

################################################################################################################

#unavailableFacility GQL 
from gql_plannedlessons.GraphResolvers import resolveUnavailableFacilityById 
from gql_plannedlessons.GraphResolvers import resolveFacilityById
from gql_plannedlessons.GraphResolvers import resolveUpdateUnavailableFacility
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
    
    @strawberryA.field(description=""" reason for unavailibility (like under-reconstruction)""")
    def reason(self) -> str:
        return self.reason

    @strawberryA.field(description="""Infor Facility that unavailable""")
    async def facility(self, info: strawberryA.types.Info) -> Union[FacilityGQLModel,None]:
        result = await resolveFacilityById(AsyncSessionFromInfo(info), self.facility_id)
        return result

    @strawberryA.field(description="""Returns the Unavailable Facility editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['UnavailableFacilityEditorGQLModel', None]:
        return self

#unavailable Facility update GQL 
@strawberryA.input
class UnavailableFacilityUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    startDate: Optional[datetime.datetime] = None
    endDate: Optional[datetime.datetime] = None

#unavailable Facility Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable unavailable Facility""")
class UnavailableFacilityEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await UnavailableFacilityGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def unavailableFacility(self, info: strawberryA.types.Info) -> UnavailableFacilityGQLModel:
        result = await UnavailableFacilityGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the unavailable Facility data""")
    async def update(self, info: strawberryA.types.Info, data: UnavailableFacilityUpdateGQLModel) -> "UnavailableFacilityEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateUnavailableFacility(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UnavailableFacilityEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

################################################################################################################

#userPlan GQL
from gql_plannedlessons.GraphResolvers import resolveUserPlanById
from gql_plannedlessons.GraphResolvers import resolveUpdateUserPlan
@strawberryA.federation.type(keys=["id"],description="""Intermediate User and Plan""")
class UserPlanGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveUserPlanById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Planned Lesson""")
    async def plannedLesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result

    @strawberryA.field(description="""User""")
    async def user(self, info: strawberryA.types.Info) -> Union[UserGQLModel,None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), self.user_id)
        return result

    @strawberryA.field(description="""Returns the user-plan editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['UserPlanEditorGQLModel', None]:
        return self

#User-Plan update GQL 
@strawberryA.input
class UserPlanUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    user_id: Optional[strawberryA.ID] = None

#User-Plan Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable User-Plan""")
class UserPlanEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await UserPlanGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def userPlan(self, info: strawberryA.types.Info) -> UserPlanGQLModel:
        result = await UserPlanGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the User-Plan data""")
    async def update(self, info: strawberryA.types.Info, data: UserPlanUpdateGQLModel) -> "UserPlanEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateUserPlan(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UserPlanEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

################################################################################################################

#facilityPlan GQL
from gql_plannedlessons.GraphResolvers import resolveFacilityPlanById
from gql_plannedlessons.GraphResolvers import resolveUpdateFacilityPlan
@strawberryA.federation.type(keys=["id"],description="""Intermediate Facility and Plan""")
class FacilityPlanGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveFacilityPlanById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Planned Lesson""")
    async def plannedLesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result

    @strawberryA.field(description="""Facility""")
    async def facility(self, info: strawberryA.types.Info) -> Union[FacilityGQLModel,None]:
        result = await resolveFacilityById(AsyncSessionFromInfo(info), self.facility_id)
        return result

    @strawberryA.field(description="""Returns the facility-plan editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['FacilityPlanEditorGQLModel', None]:
        return self

#Facility-Plan update GQL 
@strawberryA.input
class FacilityPlanUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    facility_id: Optional[strawberryA.ID] = None

#Facility-Plan Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable Facility-Plan""")
class FacilityPlanEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await FacilityPlanGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def facilityPlan(self, info: strawberryA.types.Info) -> FacilityPlanGQLModel:
        result = await FacilityPlanGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the Facility-Plan data""")
    async def update(self, info: strawberryA.types.Info, data: FacilityPlanUpdateGQLModel) -> "FacilityPlanEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateFacilityPlan(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = FacilityPlanEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

################################################################################################################

#groupPlan GQL
from gql_plannedlessons.GraphResolvers import resolveGroupPlanById
from gql_plannedlessons.GraphResolvers import resolveUpdateGroupPlan
@strawberryA.federation.type(keys=["id"],description="""Intermediate Group and Plan""")
class GroupPlanGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveGroupPlanById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id


    @strawberryA.field(description="""Planned Lesson""")
    async def plannedLesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(AsyncSessionFromInfo(info), self.plannedlesson_id)
        return result

    @strawberryA.field(description="""Group""")
    async def group(self, info: strawberryA.types.Info) -> Union[GroupGQLModel,None]:
        result = await resolveGroupById(AsyncSessionFromInfo(info), self.group_id)
        return result

    @strawberryA.field(description="""Returns the Group-plan editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['GroupPlanEditorGQLModel', None]:
        return self

#Group-Plan update GQL 
@strawberryA.input
class GroupPlanUpdateGQLModel:
    lastchange: datetime.datetime  # razitko
    group_id: Optional[strawberryA.ID] = None

#Group-Plan Edit GQL   
@strawberryA.federation.type( keys=["id"], description="""Entity representing an editable Group-Plan""")
class GroupPlanEditorGQLModel:

    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await GroupPlanGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def groupPlan(self, info: strawberryA.types.Info) -> GroupPlanGQLModel:
        result = await GroupPlanGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the Group-Plan data""")
    async def update(self, info: strawberryA.types.Info, data: GroupPlanUpdateGQLModel) -> "GroupPlanEditorGQLModel":
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateGroupPlan(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = GroupPlanEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
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
from gql_plannedlessons.GraphResolvers import resolveUserPlanAll,resolveGroupPlanAll,resolveFacilityPlanAll
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

    #group-plan
    @strawberryA.field(description="""Finds a group-plan by id""")
    async def group_plan_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[GroupPlanGQLModel,None]:
        result = await resolveGroupPlanById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all GroupPlans""")
    async def group_plan_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[GroupPlanGQLModel]:
        result = await resolveGroupPlanAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #user-plan
    @strawberryA.field(description="""Finds a UserPlan by id""")
    async def user_plan_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserPlanGQLModel,None]:
        result = await resolveUserPlanById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all UserPlans""")
    async def user_plan_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UserPlanGQLModel]:
        result = await resolveUserPlanAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    #facility-plan
    @strawberryA.field(description="""Finds a FacilityPlan by id""")
    async def facility_plan_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[FacilityPlanGQLModel,None]:
        result = await resolveFacilityPlanById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all FacilityPlans""")
    async def facility_plan_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[FacilityPlanGQLModel]:
        result = await resolveFacilityPlanAll(AsyncSessionFromInfo(info), skip, limit)
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
        result = await resolveUnavailableFacilityById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds all unavailable facilities""")
    async def unavailable_facility_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[UnavailableFacilityGQLModel]:
        result = await resolveUnavailableFacilityAll(AsyncSessionFromInfo(info), skip, limit)
        return result

#call method in DBfeed


    @strawberryA.field(description="""""")
    async def load_demo_data(self,info: strawberryA.types.Info) -> str:
        asyncSessionMaker = info.context['asyncSessionMaker']
        result = await predefineAllDataStructures(asyncSessionMaker)
        return 'ok'
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))