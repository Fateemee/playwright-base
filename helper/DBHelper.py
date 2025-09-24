import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

class DBHelper:
    def __init__(self, key):
        self.pool = None
        self.key = key.upper()  # multi، ssl، reseller
        self.host = os.getenv(f"DB_HOST_{self.key}")
        self.port = int(os.getenv(f"DB_PORT_{self.key}", 3306))
        self.user = os.getenv(f"DB_USER_{self.key}")
        self.password = os.getenv(f"DB_PASSWORD_{self.key}")
        self.db = os.getenv(f"DB_NAME_{self.key}")

        if not all([self.host, self.user, self.password, self.db]):
            raise ValueError(f"Database configuration for key '{key}' is incomplete!")

    async def connect(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                autocommit=True
            )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def fetch_one(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchone()

    async def fetch_all(self, query, *args):
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()
