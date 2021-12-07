from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    db_file="C:/Users/Administrator/Desktop/qq_go/gm.db"
    class Config:
        extra = "ignore"
