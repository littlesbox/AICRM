import os
import dotenv
from zai import ZhipuAiClient

from .llms import get_llm

dotenv.load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")
#
# client = ZhipuAiClient(api_key=API_KEY)
# response = client.embeddings.create(
#     model="embedding-3", #填写需要调用的模型编码
#     input=[
#         "美食非常美味，服务员也很友好。"
#     ],
#     dimensions=1024
# )
# print(response)

from langchain_community.embeddings import ZhipuAIEmbeddings

text = "LangChain is the framework for building context-aware reasoning applications"


embeddings = ZhipuAIEmbeddings(
    model="embedding-3",
    api_key=API_KEY,
    # With the `embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    dimensions=1024
)

single_vector = embeddings.embed_query(text)
print(str(single_vector)[:100])  # Show the first 100 characters of the vector