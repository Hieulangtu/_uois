from doctest import master
from functools import cache
from gql_plannedlessons.DBDefinitions import BaseModel

import random
import itertools
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
def types1():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {'id': '282e67ec-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeA'},
        {'id': '282e6e86-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeB'},
        {'id': '282e7002-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeC'},
    ]
    return data

@cache
def types2():
    # krome id a name, lze mit i dalsi prvky, napriklad cizi klice...
    data = [
        {'id': '4b883614-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeX'},
        {'id': '4b8838a8-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeY'},
        {'id': '4b883a38-6d9e-11ed-a1eb-0242ac120002', 'name': 'typeZ'},
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
      putPredefinedStructuresIntoTable(asyncSessionMaker, Types1Model, types1), # prvni
      putPredefinedStructuresIntoTable(asyncSessionMaker, Types1Model, types2)  # druha ...
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