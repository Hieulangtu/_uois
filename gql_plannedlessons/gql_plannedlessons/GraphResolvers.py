
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import delete
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

async def resolveUsersForPlannedLesson_(session, id):
    statement = select(UserModel).join(UserPlanModel)
    statement = statement.filter(UserPlanModel.plannedlesson_id == id)
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolveGroupsForPlannedLesson_(session, id):
    statement = select(GroupModel).join(GroupPlanModel)
    statement = statement.filter(GroupPlanModel.plannedlesson_id == id)
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolveFacilitiesForPlannedLesson_(session, id):
    statement = select(FacilityModel).join(FacilityPlanModel)
    statement = statement.filter(FacilityPlanModel.plannedlesson_id == id)
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolveDeletePlannedLesson(session, id) :
    statement = delete(PlannedLessonModel).where(PlannedLessonModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

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

async def resolveDeleteUserPlan(session, id) :
    statement = delete(UserPlanModel).where(UserPlanModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

#groupPlan resolver
resolveGroupPlanById = createEntityByIdGetter(GroupPlanModel)
resolveGroupPlanAll = createEntityGetter(GroupPlanModel)
resolveUpdateGroupPlan = createUpdateResolver(GroupPlanModel)
resolveInsertGroupPlan = createInsertResolver(GroupPlanModel)

async def resolveDeleteGroupPlan(session, id) :
    statement = delete(GroupPlanModel).where(GroupPlanModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

#facilityPlan resolver
resolveFacilityPlanById = createEntityByIdGetter(FacilityPlanModel)
resolveFacilityPlanAll = createEntityGetter(FacilityPlanModel)
resolveUpdateFacilityPlan = createUpdateResolver(FacilityPlanModel)
resolveInsertFacilityPlan = createInsertResolver(FacilityPlanModel)

async def resolveDeleteFacilityPlan(session, id) :
    statement = delete(FacilityPlanModel).where(FacilityPlanModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

# Unavailable resolver

#unavailable Plan lesson resolver
resolveUnavailablePLById = createEntityByIdGetter(UnavailablePLModel)
resolveUnavailablePLAll = createEntityGetter(UnavailablePLModel)
resolveUpdateUnavailablePL = createUpdateResolver(UnavailablePLModel)
resolveInsertUnavailablePL = createInsertResolver(UnavailablePLModel)

async def resolveDeleteUnavailablePlannedlesson(session, id) :
    statement = delete(UnavailablePLModel).where(UnavailablePLModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

#unavailable User resolver
resolveUnavailableUserById = createEntityByIdGetter(UnavailableUserModel)
resolveUnavailableUserAll = createEntityGetter(UnavailableUserModel)
resolveUpdateUnavailableUser = createUpdateResolver(UnavailableUserModel)
resolveInsertUnavailableUser = createInsertResolver(UnavailableUserModel)

async def resolveDeleteUnavailableUser(session, id) :
    statement = delete(UnavailableUserModel).where(UnavailableUserModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"

#unavailable Facility resolver
resolveUnavailableFacilityById = createEntityByIdGetter(UnavailableFacilityModel)
resolveUnavailableFacilityAll = createEntityGetter(UnavailableFacilityModel)
resolveUpdateUnavailableFacility = createUpdateResolver(UnavailableFacilityModel)
resolveInsertUnavailableFacility = createInsertResolver(UnavailableFacilityModel)

async def resolveDeleteUnavailableFacility(session, id) :
    statement = delete(UnavailableFacilityModel).where(UnavailableFacilityModel.id == id)
    result = await session.execute(statement)
    await session.commit()
    return "ok"



# async def resolvePlannedLessonsForEvent_(session, id):
#     statement = select(PlannedLessonModel).join(EventPlanModel)
#     statement = statement.filter(EventPlan.user_id == id)
    
#     response = await session.execute(statement)
#     result = response.scalars()
#     return result
