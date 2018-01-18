from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, DateTime

def table_person(metadata):

    person =  Table('person', metadata,
        Column('id', Integer(), primary_key=True),
        Column('question', String(511)),
        Column('good', String(511)),
        Column('fine', String(511)),
        Column('ok', String(511)),
        Column('wow', String(511))
    )

    return person

def table_trying_to_be_a_person(metadata):

    trying_to_be_a_person =  Table('trying_to_be_a_person', metadata,
        Column('id', Integer(), primary_key=True),
        Column('question', String(511)),
        Column('good', String(511)),
        Column('fine', String(511)),
        Column('ok', String(511)),
        Column('wow', String(511))
    )

    return trying_to_be_a_person

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

    table_submitted(metadata)
    table_person(metadata)
    table_trying_to_be_a_person(metadata)

    metadata.create_all(engine)
