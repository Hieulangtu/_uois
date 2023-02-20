
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_plannedlessons.DBDefinitions import BaseModel, PlannedLessonModel, UserPlanModel, GroupPlanModel, FacilityPlanModel
from gql_plannedlessons.DBDefinitions import UnavailablePLModel, UnavailableUserModel, UnavailableFacilityModel
from gql_plannedlessons.DBDefinitions import UserModel, GroupModel, EventModel, FacilityModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################



###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

#plannedlesson resolver
resolvePlannedLessonPage = createEntityGetter(PlannedLessonModel) #fuction. return a list
resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel) #single row . 
resolveUpdatePlannedLesson = createUpdateResolver(PlannedLessonModel)
resolveInsertPlannedLesson = createInsertResolver(PlannedLessonModel)

# resolveEventsForPlannedLesson = create1NGetter(EventModel,foreignKeyName='plannedlesson_id')

resolveUserLinksForPlannedLesson = create1NGetter(UserPlanModel,foreignKeyName='plannedlesson_id') 
resolveGroupLinksForPlannedLesson = create1NGetter(GroupPlanModel,foreignKeyName='plannedlesson_id')
resolveFacilityLinksForPlannedLesson = create1NGetter(FacilityPlanModel,foreignKeyName='plannedlesson_id')

resolveUnavailablePLsForPlannedLesson = create1NGetter(UnavailablePLModel,foreignKeyName='plannedlesson_id') 
# resolveUnavailablesForUser = create1NGetter(UnavailableUserModel,foreignKeyName='user_id') 
# resolveUnavailablesForFacility = create1NGetter(UnavailableFacilityModel,foreignKeyName='facility_id') 

# resolveUnavailableUsersForPlannedLesson = create1NGetter(UnavailableUserModel,foreignKeyName='plannedlesson_id') 
# resolveUnavailableFacilitiesForPlannedLesson = create1NGetter(UnavailableFacilityModel,foreignKeyName='plannedlesson_id') 
  

#user resolver
resolveUserById = createEntityByIdGetter(UserModel)
resolveUserAll = createEntityGetter(UserModel)
resolveUpdateUser = createUpdateResolver(UserModel)
resolveInsertUser = createInsertResolver(UserModel)

resolverPlanLinksForUser = create1NGetter(UserPlanModel,foreignKeyName='user_id')

async def resolvePlannedLessonsForUser_(session, id):
    statement = select(PlannedLessonModel).join(UserPlanModel)
    statement = statement.filter(UserPlanModel.user_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result

resolveUnavailablesForUser = create1NGetter(UnavailableUserModel,foreignKeyName='user_id') 

#group resolver
resolveGroupById = createEntityByIdGetter(GroupModel)
resolveGroupAll = createEntityGetter(GroupModel)

resolverPlanLinksForGroup = create1NGetter(GroupPlanModel,foreignKeyName='group_id')

async def resolvePlannedLessonsForGroup_(session, id):
    statement = select(PlannedLessonModel).join(GroupPlanModel)
    statement = statement.filter(GroupPlanModel.group_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result


#facility resolver
resolveFacilityById = createEntityByIdGetter(FacilityModel)
resolveFacilityAll = createEntityGetter(FacilityModel)

resolverPlanLinksForFacility = create1NGetter(FacilityPlanModel,foreignKeyName='facility_id')

async def resolvePlannedLessonsForFacility_(session, id):
    statement = select(PlannedLessonModel).join(FacilityPlanModel)
    statement = statement.filter(FacilityPlanModel.facility_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result

resolveUnavailablesForFacility = create1NGetter(UnavailableFacilityModel,foreignKeyName='facility_id') 

#event resolver
resolveEventById = createEntityByIdGetter(EventModel)
resolveEventAll = createEntityGetter(EventModel)

resolverPlansForEvent = create1NGetter(PlannedLessonModel,foreignKeyName='event_id')

# intermediate data resolver

#userPlan resolver
resolveUserPlanById = createEntityByIdGetter(UserPlanModel)
resolveUserPlanAll = createEntityGetter(UserPlanModel)
resolveUpdateUserPlan = createUpdateResolver(UserPlanModel)
resolveInsertUserPlan = createInsertResolver(UserPlanModel)

#groupPlan resolver
resolveGroupPlanById = createEntityByIdGetter(GroupPlanModel)
resolveGroupPlanAll = createEntityGetter(GroupPlanModel)
resolveUpdateGroupPlan = createUpdateResolver(GroupPlanModel)
resolveInsertGroupPlan = createInsertResolver(GroupPlanModel)

#facilityPlan resolver
resolveFacilityPlanById = createEntityByIdGetter(FacilityPlanModel)
resolveFacilityPlanAll = createEntityGetter(FacilityPlanModel)
resolveUpdateFacilityPlan = createUpdateResolver(FacilityPlanModel)
resolveInsertFacilityPlan = createInsertResolver(FacilityPlanModel)

# Unavailable resolver

#unavailable Plan lesson resolver
resolveUnavailablePLById = createEntityByIdGetter(UnavailablePLModel)
resolveUnavailablePLAll = createEntityGetter(UnavailablePLModel)
resolveUpdateUnavailablePL = createUpdateResolver(UnavailablePLModel)
resolveInsertUnavailablePL = createInsertResolver(UnavailablePLModel)

#unavailable User resolver
resolveUnavailableUserById = createEntityByIdGetter(UnavailableUserModel)
resolveUnavailableUserAll = createEntityGetter(UnavailableUserModel)
resolveUpdateUnavailableUser = createUpdateResolver(UnavailableUserModel)
resolveInsertUnavailableUser = createInsertResolver(UnavailableUserModel)

#unavailable Facility resolver
resolveUnavailableFacilityById = createEntityByIdGetter(UnavailableFacilityModel)
resolveUnavailableFacilityAll = createEntityGetter(UnavailableFacilityModel)
resolveUpdateUnavailableFacility = createUpdateResolver(UnavailableFacilityModel)
resolveInsertUnavailableFacility = createInsertResolver(UnavailableFacilityModel)



# async def resolvePlannedLessonsForEvent_(session, id):
#     statement = select(PlannedLessonModel).join(EventPlanModel)
#     statement = statement.filter(EventPlan.user_id == id)
    
#     response = await session.execute(statement)
#     result = response.scalars()
#     return result
