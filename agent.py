import os
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.sqlite import SqliteSaver
from pyexpat.errors import messages
from utils.config import Config
from utils import get_llm
from utils import get_tools
from utils.models import Context, ResponseFormat
from utils.logger import LoggerManager
from utils.memory_sqlite import get_sqlite_saver

SYSTEM_PROMPT = '''你是一个AI助理，同时也可以处理数据库查询。

你可以使用三个工具：
rag_law：用于获取《中华人民共和国反家庭暴力法》的内容。
tavily_search：用于通过网络检索获取一些最新的资讯。
sql_agent：用于使用自然语言查询数据库，执行复杂的SQL操作。

如果从问题中判断出回答用户需要依据《中华人民共和国反家庭暴力法》来进行回答，则使用 rag_law。
如果从问题中判断出用户是想要一些最新消息，比如今天是几月几号，这样具有时效性的内容，使用 tavily_search 来获取。
如果用户的问题涉及数据库查询，例如，有多少个岗位，多少个候选人，使用 sql_agent 工具
'''

logger = LoggerManager.get_logger()

llm_chat = get_llm()

tools = get_tools()

checkpointer = get_sqlite_saver()

agent = create_agent(
    model=llm_chat,
    system_prompt=SYSTEM_PROMPT,
    tools=tools,
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

def run_conversation(thread_id='1', user_id='1'):
    config = {"configurable":{"thread_id":thread_id}}
    print(f'开始对话，线程ID：{thread_id}, 用户ID：{user_id}')
    print("输入 exit 结束对话：")
    while(True):
        user_input = input("用户：").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue
        response = agent.invoke(
        {"messages":[{"role":"user", "content":user_input}]},
            config=config,
            context=Context(user_id=user_id)
        )
        structured = response.get("structured_response")
        if structured:
            print(f"Agent回复：{structured.answer}")
            if structured.tool_used:
                print(f"使用的工具：{structured.tool_used}")
            if structured.law_references:
                print(f"引用内容：{structured.law_references}")
            if structured.search_results:
                print(f"搜索结果：{structured.search_results}")
            if structured.sql_results:
                print(f"查询结果：{structured.sql_results}")
            if structured.confidence is not None:
                print(f"置信度：{structured.confidence}")
        else:
            print(f"Agent回复：{response}")

        logger.info(f"对话记录：用户：{user_input}, Agent: {structured}")

if __name__ == "__main__":
    run_conversation()