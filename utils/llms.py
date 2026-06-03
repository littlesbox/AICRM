from langchain_openai import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

MODEL_CONFIG = {
    "deepseek":{
        "base_url":"https://api.deepseek.com",
        "api_key":DEEPSEEK_API_KEY,
        "model_name":"deepseek-chat"
    }
}


DEFAULT_LLM_TYPE = "deepseek"
DEFAULT_TEMPERATURE = 0

class LLMInitialzationError(Exception):
    pass

def initialize_llm(llm_type:str = DEFAULT_LLM_TYPE) -> ChatOpenAI:
    try:
        if llm_type not in MODEL_CONFIG:
            raise ValueError(f"不支持的LLM类型：{llm_type}，可用的类型：{list(MODEL_CONFIG.keys())}")

        config = MODEL_CONFIG[llm_type]

        llm_chat = ChatOpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
            model=config["model_name"],
            temperature=DEFAULT_TEMPERATURE,
            timeout=30,
            max_retries=3
        )
        return llm_chat

    except ValueError as ve:
        raise LLMInitialzationError(f"LLM 配置错误：{str(ve)}")
    except Exception as e:
        raise LLMInitialzationError(f"初始化LLM失败：{str(e)}")

def get_llm(llm_type:str = DEFAULT_LLM_TYPE) -> ChatOpenAI:
    try:
        return initialize_llm(llm_type)
    except LLMInitialzationError as e:
        if llm_type != DEFAULT_LLM_TYPE:
            return initialize_llm(DEFAULT_LLM_TYPE)
        raise e

if __name__ == "__main__":
    llm = get_llm(llm_type=DEFAULT_LLM_TYPE)
    res = llm.invoke([
        {"role": "user", "content": "今天是几月几号"}
    ])
    print(res.content)