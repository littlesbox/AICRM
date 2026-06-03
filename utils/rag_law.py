import os
import dotenv
from pathlib import Path
from typing import List, Optional
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.llms import get_llm
from utils.logger import LoggerManager
from langchain_community.embeddings import ZhipuAIEmbeddings
from utils.llms import MODEL_CONFIG, DEFAULT_LLM_TYPE

dotenv.load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

logger = LoggerManager.get_logger()

LAW_DOC_PATH = Path(__file__).parent.parent / "data" / "中华人民共和国反家庭暴力法.txt"
CHROMA_PERSIST_DIR = Path(__file__).parent / "chroma_law"
COLLECTION_NAME = "anti_domestic_violence_law"

_vector_store: Optional[Chroma] = None

def get_embedding_model():
    embeddings = ZhipuAIEmbeddings(
        model="embedding-3",
        api_key=ZHIPU_API_KEY,
        # With the `embedding-3` class
        # of models, you can specify the size
        # of the embeddings you want returned.
        dimensions=1024
    )
    return embeddings

def load_and_split_documents() ->List[Document]:
    if not LAW_DOC_PATH.exists():
        raise FileNotFoundError(f"法律条文文件不存在：{LAW_DOC_PATH}")

    loader = TextLoader(str(LAW_DOC_PATH), encoding="utf-8")
    documents = loader.load()
    # print(documents)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=0,
        separators=["\n"]
    )
    splits = text_splitter.split_documents(documents)
    logger.info(f"法律条文加载完成，共{len(documents)}个原始文档，分割为{len(splits)}个块")
    return splits

def get_vector_store() -> Chroma:
    global _vector_store
    if _vector_store is not None:
        return _vector_store
    logger.info("正在初始化法律条文向量存储（Chroma）...")
    splits = load_and_split_documents()

    # 获取嵌入模型
    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embedding_model,
        persist_directory=str(CHROMA_PERSIST_DIR),
        collection_name=COLLECTION_NAME,
    )
    _vector_store = vector_store
    logger.info(f"法律条文向量存储初始化完成，持久化目录：{CHROMA_PERSIST_DIR}")
    return vector_store

def retrieve_law(query: str, k: int =3) -> List[Document]:
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query=query, k=k)
    return docs

def format_docs(docs: List[Document]) -> str:
    formatted = []
    for i, doc in enumerate(docs, 1):
        content = doc.page_content.strip()
        formatted.append(f"{i}. {content}")
    return "\n\n".join(formatted)

def rag_law_query(query: str) -> str:
    
    try:
        docs = retrieve_law(query=query, k=3)
        if not docs:
            return "未找到相关法律条文。"
        return format_docs(docs)
    except Exception as e:
        logger.error(f"法律条文检索失败：{e}")
        return f"法律条文检索时发生错误：{str(e)}"

if __name__ == "__main__":
    # embedding_model = get_embedding_model()
    # text = "LangChain is the framework for building context-aware reasoning applications"
    # single_vector = embedding_model.embed_query(text)
    # print(str(single_vector)[:100])
    print(rag_law_query("《中华人民共和国反家庭暴力法》第一条规定是什么"))

    # loader = TextLoader(str(LAW_DOC_PATH), encoding="utf-8")
    # documents = loader.load()
    # print(documents[0].page_content)
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=100,
    #     chunk_overlap=0,
    #     separators=["\n"]
    # )
    # splits = text_splitter.split_documents(documents)
    # for doc in splits:
    #     print("\n")
    #     print(len(doc.page_content))
    #     print(doc.page_content)
    #     print("\n")