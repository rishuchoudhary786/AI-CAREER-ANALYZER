from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import pymysql
import os

pymysql.install_as_MySQLdb()
load_dotenv()

host     = os.getenv("TIDB_HOST")
port     = os.getenv("TIDB_PORT")
user     = os.getenv("TIDB_USER")
password = os.getenv("TIDB_PASSWORD")
db       = os.getenv("TIDB_DB")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ssl_verify_cert": False,
            "ssl_verify_identity": False
        }
    }
)

sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()