
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_plannedlessons.DBDefinitions import BaseModel, PlannedLessonModel, UserPlan, GroupPlan, EventPlan, FacilityPlan
from gql_plannedlessons.DBDefinitions import UnavailabilityPL, UnavailabilityUser, UnavailabilityFacility
from gql_plannedlessons.DBDefinitions import UserModel, GroupModel, Event, Facility

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


resolveUserLinksForPlannedLesson = create1NGetter(UserPlan,foreignKeyName='plannedlesson_id') 
resolveGroupLinksForPlannedLesson = create1NGetter(GroupPlan,foreignKeyName='plannedlesson_id')
resolveFacilityLinksForPlannedLesson = create1NGetter(EventPlan,foreignKeyName='plannedlesson_id')
resolveEventLinksForPlannedLesson = create1NGetter(FacilityPlan,foreignKeyName='plannedlesson_id')

# intermediate data resolver
async def resolvePlannedLessonsForUser_(session, id):
    statement = select(PlannedLessonModel).join(UserPlan)
    statement = statement.filter(UserPlan.user_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolvePlannedLessonsForGroup_(session, id):
    statement = select(PlannedLessonModel).join(GroupPlan)
    statement = statement.filter(GroupPlan.user_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolvePlannedLessonsForFacility_(session, id):
    statement = select(PlannedLessonModel).join(FacilityPlan)
    statement = statement.filter(FacilityPlan.user_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolvePlannedLessonsForEvent_(session, id):
    statement = select(PlannedLessonModel).join(EventPlan)
    statement = statement.filter(EventPlan.user_id == id)
    
    response = await session.execute(statement)
    result = response.scalars()
    return result


#unavailable Plan lesson resolver
resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
resolveUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

#unavailable User resolver
resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
resolveUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

#unavailable Facility resolver
resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
resolveUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)