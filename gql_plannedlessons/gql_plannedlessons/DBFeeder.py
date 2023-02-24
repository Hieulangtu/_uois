from doctest import master
from functools import cache
from gql_plannedlessons.DBDefinitions import BaseModel,PlannedLessonModel
from gql_plannedlessons.DBDefinitions import UserPlanModel, GroupPlanModel,FacilityPlanModel
from gql_plannedlessons.DBDefinitions import UnavailablePLModel, UnavailableFacilityModel, UnavailableUserModel

import random
import itertools
import datetime
from functools import cache


from sqlalchemy.future import select

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sva systemova data
#
###########################################################################################################################

@cache
def determinePlans():
    data = [
        {'id': 'a6b68fca-7874-419f-8366-007d6348c365','name':'matematika'},
        {'id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb','name':'informatika'},
        {'id': '7ec909c7-8479-4381-af99-fcc254fdd0ec','name':'data analyza'}
    ]
    return data

@cache
def determineUnavailablePlans():
    data = [
        {'id': '3c4ea8df-ef85-411f-9b31-1466e24b783a','plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365','reason':'Státní svátek', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': 'aff5f481-8316-431d-a8ab-7964010855be','plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365','reason':'sportovní den', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': 'bad2b1bd-f46c-4853-824b-286c8a559d39','plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365','reason':'oslavný den', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': 'd60f27be-94d0-4054-9b30-b21f94cce233','plannedlesson_id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb','reason':'Státní svátek', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '6470d145-2d70-4314-ab77-c56906c390e1','plannedlesson_id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb','reason':'oslavný den', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def determineUnavailableUsers():
    data = [
        {'id': 'aef959ec-88b9-4d34-ac18-a204944d8fbd','reason':'na dovolené', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '878a749a-0e56-4520-ad32-3a0df939a32a','reason':'osobní důvody', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': 'fec7906c-2941-4ffc-8bc2-9fc96d9cb971','reason':'osobní důvody', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '1f29aee7-7131-417d-98ee-77db9aab7c34','reason':'osobní důvody', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '2c375f31-7593-4cf3-b742-a1ccc5a7bb90','reason':'mít svatbu', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def determineUnavailableFacilities():
    data = [
        {'id': '66d42be1-4c1f-4db0-94b0-8623dffe2e01','reason':'v rekonstrukci', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '71bdc937-9aed-4f09-a6fa-b64ed95140ab','reason':'v rekonstrukci', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': 'ffeced99-598e-4701-8e65-1ee1b63d6ffd','reason':'v rekonstrukci', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '306848ac-b50d-48cc-8b1f-7a992cd6546f','reason':'Prezidentská přijímací místnost', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
        {'id': '57da7bcb-22d0-4e3a-b1e0-65951030a02f','reason':'nemá vody', 'startDate': datetime.datetime.now(), 'endDate':datetime.datetime.today(), "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def determineUserPlans():
    data = [
        {'id': '270a95eb-6cee-4941-9f09-23b8f6667fa6', 'plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365', "lastchange":datetime.datetime.now()},
        {'id': '8f716bc8-21d0-4924-ab00-79ac67692d29', 'plannedlesson_id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb', "lastchange":datetime.datetime.now()},
        {'id': '81bd5329-5777-45cd-b1d7-be66cffe91e1', 'plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365', "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def determineGroupPlans():
    data = [
        {'id': '5a732669-4e00-4393-b4cf-9f2da7b2b31c', 'plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365', "lastchange":datetime.datetime.now()},
        {'id': '264fbd79-4e61-46c3-98b0-5d0a9a8b44ec', 'plannedlesson_id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb', "lastchange":datetime.datetime.now()},
        {'id': 'd9774e66-7d23-472c-9c80-cf0f22d72321', 'plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365', "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def determineFacilityPlans():
    data = [
        {'id': '20ebf579-cf87-4b58-a39f-a13dbccd52bb', 'plannedlesson_id': 'a6b68fca-7874-419f-8366-007d6348c365', "lastchange":datetime.datetime.now()},
        {'id': 'ab602e68-dbd5-4082-8840-c7ca7a22b1ce', 'plannedlesson_id': '7ec909c7-8479-4381-af99-fcc254fdd0ec', "lastchange":datetime.datetime.now()},
        {'id': '1e5e526c-3f64-4d98-bb15-5b16c1f1bcd2', 'plannedlesson_id': 'cd45cbb8-de6d-4ea2-82ee-6294010b00cb', "lastchange":datetime.datetime.now()},
    ]
    return data

@cache
def d():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {'id': '282e67ec-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeA'},
        {'id': '282e6e86-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeB'},
        {'id': '282e7002-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeC'},
    ]
    return data
###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

import asyncio
async def predefineAllDataStructures(asyncSessionMaker):
    
    await asyncio.gather(
      putPredefinedStructuresIntoTable(asyncSessionMaker, PlannedLessonModel, determinePlans), # prvni
      putPredefinedStructuresIntoTable(asyncSessionMaker, UnavailablePLModel, determineUnavailablePlans),  # druha ...
      putPredefinedStructuresIntoTable(asyncSessionMaker, UnavailableUserModel, determineUnavailableUsers),
      putPredefinedStructuresIntoTable(asyncSessionMaker, UnavailableFacilityModel, determineUnavailableFacilities),
      putPredefinedStructuresIntoTable(asyncSessionMaker, UserPlanModel, determineUserPlans),
      putPredefinedStructuresIntoTable(asyncSessionMaker, GroupPlanModel, determineGroupPlans),
      putPredefinedStructuresIntoTable(asyncSessionMaker, FacilityPlanModel, determineFacilityPlans)
    )
    
    
    return

# async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
#     """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
#        DBModel zprostredkovava tabulku, je to sqlalchemy model
#        structureFunction() dava data, ktera maji byt ulozena
#     """
#     # ocekavane typy 
#     externalIdTypes = structureFunction()
    
#     #dotaz do databaze
#     stmt = select(DBModel)
#     async with asyncSessionMaker() as session:
#         dbSet = await session.execute(stmt)
#         dbRows = list(dbSet.scalars())
    
#     #extrakce dat z vysledku dotazu
#     #vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
#     dbRowsDicts = [
#         {'name': row.name, 'id': f'{row.id}'} for row in dbRows
#         ]

#     print(structureFunction, 'external id types found in database')
#     print(dbRowsDicts)

#     # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
#     idsInDatabase = [row['id'] for row in dbRowsDicts]

#     # zjistime, ktera id nejsou v databazi
#     unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))
#     print(structureFunction, 'external id types not found in database')
#     print(unsavedRows)

#     # pro vsechna neulozena id vytvorime entity
#     rowsToAdd = [DBModel(**row) for row in unsavedRows]
#     print(rowsToAdd)
#     print(len(rowsToAdd))

#     # a vytvorene entity jednou operaci vlozime do databaze
#     async with asyncSessionMaker() as session:
#         async with session.begin():
#             session.add_all(rowsToAdd)
#         await session.commit()

#     # jeste jednou se dotazeme do databaze
#     stmt = select(DBModel)
#     async with asyncSessionMaker() as session:
#         dbSet = await session.execute(stmt)
#         dbRows = dbSet.scalars()
    
#     #extrakce dat z vysledku dotazu
#     dbRowsDicts = [
#         {'name': row.name, 'id': f'{row.id}'} for row in dbRows
#         ]

#     print(structureFunction, 'found in database')
#     print(dbRowsDicts)

#     # znovu id, ktera jsou uz ulozena
#     idsInDatabase = [row['id'] for row in dbRowsDicts]

#     # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
#     unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))

#     # ted by melo byt pole prazdne
#     print(structureFunction, 'not found in database')
#     print(unsavedRows)
#     if not(len(unsavedRows) == 0):
#         print('SOMETHING is REALLY WRONG')

#     print(structureFunction, 'Defined in database')
#     # nyni vsechny entity mame v pameti a v databazi synchronizovane
#     print(structureFunction())
#     pass

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci zaznamu v databazi
       DBModel zprostredkovava tabulku,
       structureFunction() dava data, ktera maji byt ulozena, predpoklada se list of dicts, pricemz dict obsahuje elementarni datove typy
    """

    tableName = DBModel.__tablename__
    # column names
    cols = [col.name for col in DBModel.metadata.tables[tableName].columns]

    def mapToCols(item):
        """z item vybere jen atributy, ktere jsou v DBModel, zbytek je ignorovan"""
        result = {}
        for col in cols:
            value = item.get(col, None)
            if value is None:
                continue
            result[col] = value
        return result

    # ocekavane typy 
    externalIdTypes = structureFunction()
    
    #dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extrakce dat z vysledku dotazu
    #vezmeme si jen atribut id, id je typu uuid, tak jej zkovertujeme na string
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    async def saveChunk(rows):
        # pro vsechna neulozena id vytvorime entity
        # omezime se jen na atributy, ktere jsou definovane v modelu
        mappedUnsavedRows = list(map(mapToCols, rows))
        rowsToAdd = [DBModel(**row) for row in mappedUnsavedRows]

        # a vytvorene entity jednou operaci vlozime do databaze
        async with asyncSessionMaker() as session:
            async with session.begin():
                session.add_all(rowsToAdd)
            await session.commit()

    if len(unsavedRows) > 0:
        # je co ukladat
        if '_chunk' in unsavedRows[0]:
            # existuje informace o rozfazovani ukladani do tabulky
            nextPhase =  [*unsavedRows]
            while len(nextPhase) > 0:
                #zjistime nejmensi cislo poradi ukladani 
                chunkNumber = min(map(lambda item: item['_chunk'], nextPhase))
                #filtrujeme radky, ktere maji toto cislo
                toSave = list(filter(lambda item: item['_chunk'] == chunkNumber, nextPhase))
                #ostatni nechame na pozdeji
                nextPhase = list(filter(lambda item: item['_chunk'] != chunkNumber, nextPhase))
                #ulozime vybrane
                await saveChunk(toSave)
        else:
            # vsechny zaznamy mohou byt ulozeny soucasne
            await saveChunk(unsavedRows)


    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    idsInDatabase = [f'{row.id}' for row in dbRows]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not(f'{row["id"]}' in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    #print(structureFunction(), 'On the input')
    #print(dbRowsDicts, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    #print(structureFunction())
    pass