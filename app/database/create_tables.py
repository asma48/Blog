
from app.database.cofig import engine, Base
import app.models

Base.metadata.create_all(bind=engine)


