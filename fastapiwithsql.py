from typing import Annotated
from sqlmodel import SQLModel,Field,Session,select, create_engine
from fastapi import FastAPI, Depends,HTTPException, Query

class Hero(SQLModel,table=True):
    id : int |None = Field(default=None,primary_key=True)
    name : str = Field(index=True)
    age : int | None = Field(default=None, index=True)
    secret_name : str


sqlite_file_name = "test.db"
sqlitedb_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlitedb_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes")
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
@app.get("/heroes/{hero_id}")
def get_hero(hero_id: int, session: SessionDep)->Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted"}
    



