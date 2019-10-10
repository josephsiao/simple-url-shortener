import psycopg2


class PostgreDB():
    """Interact with PostgreSQL database."""
    def __init__(self, database_config):
        self.database_config = database_config

    def add_data(self, data):
        """Add a data to database."""
        try:
            conn = psycopg2.connect(**self.database_config)
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO URL (SHORTEN, ORIGINAL) VALUES (%s, %s)', data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def check_data_exist(self, shorten=None, original=None):
        """Check data if already in database or not."""
        try:
            conn = psycopg2.connect(**self.database_config)
            cur = conn.cursor()
            if shorten:
                cur.execute('SELECT * FROM URL WHERE SHORTEN = %s',
                            (shorten,))
            else:
                cur.execute('SELECT * FROM URL WHERE ORIGINAL = %s',
                            (original,))
            result = cur.fetchone()
            if result and original:
                return result[1]
            elif result and shorten:
                return result[2]
            else:
                return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def create_table(self):
        """Create table in database."""
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
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
