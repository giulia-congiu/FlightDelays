from database.DB_connect import DBConnect
from model.airport import Airport
from model.arco import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapAreoporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.ID, t.IATA_CODE, count(*) as N
                FROM (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                from airports a, flights f
                where a.ID = f.ORIGIN_AIRPORT_ID 
                or a.ID = f.DESTINATION_AIRPORT_ID 
                GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                GROUP BY t.ID, t.IATA_CODE
                having N >= %s
                order by N asc"""

        cursor.execute(query, (n,))

        for row in cursor:
            #uso la mappa per recuperare l'areoporto data la chiave
            #aggiungo alla lista di risultati un sottoinsieme di areoporti, quelli con n> di quello specificato
            result.append(idMapAreoporti[row["ID"]])

        cursor.close()
        conn.close()
        return result

    '''attenzione che nella query in cui prendo gli archi, perchè avrò righe ripetute tra destra e sx
    provo sia la versione in cui complico python che quello dove complico a query'''


    @staticmethod
    def getAllEdges1(idMapAreoporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*)
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AORIGIN_AIRPORT_IDIRPORT_ID , f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            #leggo due id map di areoporti e posso creare una tupla con due aereoporti con la mappa
            #result.append((idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["peso"]]))
            #creo una lista di oggetti tipo tratta
            result.append(Tratta(idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["peso"]]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges2(idMapAreoporti):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce(t1.n,0)+ coalesce(t2.n, 0) as peso
                    from (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID) t1
                    left join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID
                    and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null
                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["ORIGIN_AIRPORT_ID"]], idMapAreoporti[row["peso"]]))

        cursor.close()
        conn.close()
        return result