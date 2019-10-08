import psycopg2


class PostgreDB():
    def __init__(self, database_config):
        self.database_config = database_config

    def add_data(self, data):
        try:
            conn = psycopg2.connect(**self.database_config)
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO URL (SHORTEN, ORIGINAL) VALUES (%s, %s)', data)
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.commit()

    def create_table(self):
        try:
            conn = psycopg2.connect(**self.database_config)
            cur = conn.cursor()
            cur.execute(
                '''
                    CREATE TABLE URL(
                        ID SERIAL PRIMARY KEY     NOT NULL,
                        SHORTEN           TEXT    NOT NULL,
                        ORIGINAL          TEXT    NOT NULL);
                '''
            )
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.commit()
