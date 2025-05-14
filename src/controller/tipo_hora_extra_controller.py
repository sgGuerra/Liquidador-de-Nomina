import sys
sys.path.append(".")
sys.path.append("src")

import psycopg2
import SecretConfig

class TipoHoraExtraController:
    @staticmethod
    def ActualizarTiposHoraExtra():
        """Actualiza los tipos de hora extra en la base de datos"""
        connection = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT
        )
        cursor = connection.cursor()
        try:
            # Primero borramos los registros existentes
            cursor.execute("DELETE FROM tipos_horas_extra")
            
            # Insertamos los nuevos valores
            cursor.execute("""
                INSERT INTO tipos_horas_extra(tipo_hora_id, nombre_tipo_hora)
                VALUES ('he01','Diurnas'),
                       ('he02','Nocturnas'),
                       ('he03','Festivas');
            """)
            
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
