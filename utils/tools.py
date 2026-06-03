from langchain.tools import tool, ToolRuntime
from .models import Context
from .logger import  LoggerManager
from .rag_law import rag_law_query
from .tavily_search import tavily_search as tavily_search_func

logger = LoggerManager.get_logger()

from .sql_agent import query_sql_agent

def get_tools():
    @tool("rag_law", description="利用法律条文知识库检索法条。")
    def rag_law(query: str) -> str:
        """
        根据用户查询检索相关法律条文。

        Args:
            query: 用户关于法律条文的问题

        Returns:
            检索到的法律条文内容
        """
        return rag_law_query(query)

    @tool("tavily_search", description="根据用户想要获取最新资讯的问题进行网络检索。")
    def tavily_search(query: str) -> str:
        """
        根据用户查询使用 Tavily 进行网络检索，返回最新的相关信息。

        Args:
            query: 用户关于最新资讯的问题

        Returns:
            格式化后的网络搜索结果
        """
        return tavily_search_func(query)

    @tool("sql_agent", description="使用自然语言查询数据库，执行复杂的SQL操作。")
    def sql_agent(query: str) -> str:
        """
        根据用户自然语言问题查询数据库，返回查询结果。

        Args:
            query: 用户关于数据库查询的问题

        Returns:
            SQL 查询结果或错误信息
        """
        return query_sql_agent(query)

    tools = [rag_law, tavily_search, sql_agent]

    logger.info(f"获取并提供的工具列表: {tools}")

    return tools

