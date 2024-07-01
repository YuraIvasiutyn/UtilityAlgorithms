import psycopg2
from typing import List, Dict, Any, Optional
from psycopg2.extras import DictCursor
from dataclasses import dataclass


@dataclass
class DBConfig:
    user: str
    password: str
    host: str
    port: str
    database: str


class DB:
    def __init__(self, config: DBConfig):
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.port = config.port
        self.database = config.database
        self._connection_string = (
            f"dbname='{self.database}' host='{self.host}' port='{self.port}' "
            f"user='{self.user}' password = '{self.password}'"
        )
        self.connection = None

    def execute_many(
        self, query: str, values: List[Dict[str, Any]], batch_size: int = 1000
    ) -> None:

        if not values:
            return None

        chunks = list_splitter(values, batch_size)

        with psycopg2.connect(self._connection_string) as conn:
            cursor = conn.cursor()
            for lp, chunk in enumerate(chunks):
                try:
                    cursor.executemany(query, chunk)
                except Exception as e:
                    raise

    def fetch_all(self, query: str, values: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            with psycopg2.connect(self._connection_string) as conn:
                cursor = conn.cursor(cursor_factory=DictCursor)
                cursor.execute(query, values)
                records = cursor.fetchall()
                return records
        except Exception as e:
            raise

    def fetch_val(self, query: str, values: Dict[str, Any]) -> Optional[Any]:
        try:
            with psycopg2.connect(self._connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                records = cursor.fetchone()
                if records:
                    return records[0]
                else:
                    return None
        except Exception as e:
            raise

    def fetch_one(self, query: str, values: Dict[str, Any]) -> Optional[Any]:
        try:
            with psycopg2.connect(self._connection_string) as conn:
                cursor = conn.cursor(cursor_factory=DictCursor)
                cursor.execute(query, values)
                records = cursor.fetchone()
                return records
        except Exception as e:
            raise


def list_splitter(list_to_split: List[Any], chunk_size: int) -> List[List[Any]]:
    list_of_chunks = []
    start_chunk = 0
    end_chunk = start_chunk + chunk_size
    while end_chunk <= len(list_to_split) + chunk_size:
        chunk_ls = list_to_split[start_chunk: end_chunk]
        if end_chunk > len(list_to_split) and not chunk_ls:
            break
        list_of_chunks.append(chunk_ls)
        start_chunk = start_chunk + chunk_size
        end_chunk = end_chunk + chunk_size
    return list_of_chunks
