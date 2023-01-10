
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_empty.DBDefinitions import BaseModel, PlannedLessonModel, UserPlan, GroupPlan, EventPlan, FacilityPlan

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

# ...

resolveUserLinksForPlannedLesson = create1NGetter(UserPlan,foreignKeyName='plannedlesson_id') #
resolveGroupLinksForPlannedLesson = create1NGetter(GroupPlan,foreignKeyName='plannedlesson_id')
resolveFacilityLinksForPlannedLesson = create1NGetter(EventPlan,foreignKeyName='plannedlesson_id')
resolveEventLinksForPlannedLesson = create1NGetter(FacilityPlan,foreignKeyName='plannedlesson_id')
