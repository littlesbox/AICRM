import os

class Config:
    LOG_FILE = "logfile/app.log"
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    MAX_BYTES = 1024 * 1024 * 10
    BACKUP_COUNT = 3
    LLM_TYPE = "deepseek"
    MEMORY_DB_PATH = "data/memory.db"
    SQL_AGENT_DB_PATH = "data/app.db"