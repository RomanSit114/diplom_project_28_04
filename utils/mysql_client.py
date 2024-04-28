import sqlalchemy
engine = sqlalchemy.create_engine('mysql://root:12345@mysql/mydb')


def execute_query(query):
    result = engine.execute(query)
    return result
