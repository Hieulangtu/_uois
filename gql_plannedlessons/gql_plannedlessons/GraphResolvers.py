
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

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

resolvePlannedLessonPage = createEntityGetter(PlannedLessonModel) #fuction. return a list
resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel) #single row . 

# intermediate data resolver
resolveUserLinksForPlannedLesson = create1NGetter(UserPlan,foreignKeyName='plannedlesson_id') #
resolveGroupLinksForPlannedLesson = create1NGetter(GroupPlan,foreignKeyName='plannedlesson_id')
resolveFacilityLinksForPlannedLesson = create1NGetter(EventPlan,foreignKeyName='plannedlesson_id')
resolveEventLinksForPlannedLesson = create1NGetter(FacilityPlan,foreignKeyName='plannedlesson_id')

#unavailable Plan lesson resolver
resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
resolverUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

#unavailable User resolver
resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
resolverUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

#unavailable Facility resolver
resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
resolverUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)