import sqlalchemy as db
from sqlalchemy.orm import sessionmaker 
import models


engine = db.create_engine("sqlite:///data.db")
models.Base.metadata.create_all(engine)
conn = engine.connect()  

Session = sessionmaker(bind=engine)
session = Session()