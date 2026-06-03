import os
from typing import Optional
from tavily import  TavilyClient
from utils.logger import LoggerManager
import os
import dotenv
dotenv.load_dotenv()

logger = LoggerManager.get_logger()

TAVILY_API_KEY = os.environ.get("TAILY_API_KEY")

if not TAVILY_API_KEY:
    logger.warning("TAILY_API_KEY 环境变量未设置，tavily搜索可能无法正常工作。")

_client: Optional[TavilyClient] = None

def get_tavily_client() -> TavilyClient:
    global _client
    if _client is None:
        if not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY 环境变量未设置，请先设置该变量以使用tavily搜索。")
        _client = TavilyClient(api_key=TAVILY_API_KEY)
        logger.info("Tavily 客户端初始化成功")
    return _client

def tavily_search(query: str, max_results: int=5) -> str:
    try:
        client = get_tavily_client()
        logger.info(f"执行tavily搜索：{query}")
        response = client.search(query=query, max_results=max_results)

        results = response.get("results", [])
        if not results:
            return "未找到相关结果"

        formatted = []
        for i, res in enumerate(results, 1):
            title = res.get("title", "无标题")
            url = res.get("url", "")
            content = res.get("content", "").strip()
            if len(content) > 300:
                content = content[:300] + "..."
            formatted.append(f"{i}. {title}\n  链接：{url}\n   摘要：{content}")

        result_text = "\n\n".join(formatted)
        logger.info(f"tavily 搜索完成，共找到{len(results)}条结果：")
        return result_text

    except Exception as e:
        error_msg = f"tavily 搜索时发生错误：{str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == '__main__':
    res = tavily_search("今天是几月几号")
    print(res)