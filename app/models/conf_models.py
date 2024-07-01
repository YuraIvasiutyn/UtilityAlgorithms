from pydantic import BaseModel


class GeneralApiConf(BaseModel):
    host: str
    port: int


class DBConfig(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    password: str
    min_num_of_conns: int
    max_num_of_conns: int
