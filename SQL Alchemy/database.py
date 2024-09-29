from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

#My engine
engine =  create_engine("sqlite:///store.db", echo=True)

#Create all tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#Make session
def get_session():
    return Session()