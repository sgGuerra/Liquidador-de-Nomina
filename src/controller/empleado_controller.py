import sys
sys.path.append( "." )
sys.path.append( "src" )

import psycopg2
from model.calculo_nomina import Nomina
import SecretConfig


class EmpleadoController:
    pass




def Obtener_cursor():
    connection = psycopg2.connect(database=SecretConfig.PGDATABASE, user=SecretConfig.PGUSER, password=SecretConfig.PGPASSWORD, host=SecretConfig.PGHOST, port=SecretConfig.PGPORT)
        # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = connection.cursor()
    return cursor