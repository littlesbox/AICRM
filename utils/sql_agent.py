import os
from typing import Optional
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from utils.llms import get_llm
from utils.config import Config
from utils.logger import LoggerManager

logger = LoggerManager.get_logger()


_sql_agent_instance = None

def get_sql_agent():
    global _sql_agent_instance
    if _sql_agent_instance is None:
        conn_string = "mysql+pymysql://root:shine@localhost:3306/job_data?charset=utf8"
        logger.info(f"连接MySQL数据库：{conn_string}")
        db = SQLDatabase.from_uri(conn_string)


        llm_chat = get_llm(Config.LLM_TYPE)

        toolkit = SQLDatabaseToolkit(db=db, llm=llm_chat)

        agent = create_sql_agent(
            llm=llm_chat,
            toolkit=toolkit,
            agent_type="zero-shot-react-description",
            verbose=True,
            handle_parsing_errors=True,
        )
        _sql_agent_instance = agent
        logger.info("SQL Agent 初始化完成")
    return _sql_agent_instance


def query_sql_agent(question: str) -> str:
    """
    使用 SQL Agent 执行自然语言查询，返回结果字符串。

    Args:
         question: 自然语言查询，例如 "有多少个用户？" 或 “显示所有产品”

    Returns:
        Agent 执行后的回答字符串。
    """
    try:
        agent = get_sql_agent()
        logger.info(f"执行 SQL Agent 查询：{question}")
        result = agent.invoke({"input":question})
        output = result.get("output", str(result))
        logger.info(f"SQL Agent 查询完成")
        return output
    except Exception as e:
        error_msg = f"SQL Agent 查询时发生错误：{str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    answer = query_sql_agent("applications 表中有多少条记录")
    print(answer)