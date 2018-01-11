from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime

def table_genarated(metadata):

    genarated =  Table('genarated', metadata,
        Column('id', Integer(), primary_key=True),
        Column('question', String(511)),
        Column('answer', String(511))
    )

    return genarated

def table_submitted(metadata):

    submitted = Table('submitted', metadata,
        Column('id', Integer(), primary_key=True),
        Column('month', Integer()),
        Column('datetime', DateTime()),
        Column('question', String(511)),
        Column('answer', String(511))
    )

    return submitted

if __name__ == '__main__':
    engine = create_engine('sqlite:///data.db', echo=True)
    metadata = MetaData()

    table_genarated(metadata)
    table_submitted(metadata)

    metadata.create_all(engine)
