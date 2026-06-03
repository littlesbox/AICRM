import os
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from .config import Config
from .logger import LoggerManager
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

logger = LoggerManager.get_logger()

def ensure_db_dir(db_path:str):
    dir_path = os.path.dirname(db_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"创建数据库目录：{dir_path}")

_sqlite_saver_instance = None

def get_sqlite_saver() -> SqliteSaver:
    global _sqlite_saver_instance
    if _sqlite_saver_instance is None:
        db_path = Config.MEMORY_DB_PATH
        ensure_db_dir(db_path)
        logger.info(f"初始化SQLiteSaver数据库路径：{db_path}")
        import sqlite3
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        serde = JsonPlusSerializer(
            allowed_msgpack_modules=[("utils.models", "ResponseFormat")]
        )
        _sqlite_saver_instance = SqliteSaver(conn, serde=serde)
    return _sqlite_saver_instance

def clear_memory():
    db_path = Config.MEMORY_DB_PATH
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.warning(f"已删除记忆数据库文件：{db_path}")
        global _sqlite_saver_instance
        _sqlite_saver_instance = None
    else:
        logger.info("记忆数据库文件不存在，无需清楚。")