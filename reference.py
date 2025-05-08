import os
import warnings

from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import Chroma


from api_key import doubao_api_key, deepseek_api_key

deepseek_base_url = "https://api.deepseek.com"

class DataCleaner():
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一名数据集清理专家，请对用户输入的数据进行数据清理，尽可能保留有用知识，最后格式为普通段落型，不得使用特殊排版符号，不得输出提示信息等多余信息。
        """
    def clear(self, input):
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        return response.choices[0].message.content


class Embeddings():
    def __init__(self):
        self.client = OpenAI(api_key=doubao_api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")

    def embed_query(self, input):
        embeddings = self.client.embeddings.create(
            model="doubao-embedding-large-text-240915",
            input=input,
            encoding_format="float"
        )
        return embeddings.data[0].embedding
    
    def embed_documents(self, inputs):
        return [self.embed_query(input) for input in inputs]


class Embedder():
    def __init__(self):
        self.db_path = "./ref/chroma_db"
        if os.path.isdir(self.db_path):
            self.load()
        else:
            self.build()

    def load(self):
        self.embeddings = Embeddings()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") # LangChainDeprecationWarning: The class `Chroma` was deprecated in LangChain 0.2.9 and will be removed in 1.0.
            self.vectorstore = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)

    def build(self):
        # Load
        loader = TextLoader("./ref/data", encoding='utf-8')
        documents = loader.load()
        # Split
        text_splitter = RecursiveCharacterTextSplitter (chunk_size=200, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        # Embed
        self.embeddings = Embeddings()
        self.vectorstore = Chroma.from_documents(chunks, self.embeddings, persist_directory=self.db_path)
        self.vectorstore.persist()


class Retriever():
    def __init__(self):
        embed_agent = Embedder()
        vectorstore = embed_agent.vectorstore
        self.retriever = vectorstore.as_retriever()
    
    def retrieve(self, input, log=None):
        related_docs = self.retriever.invoke(input)
        context = "\n".join([doc.page_content for doc in related_docs])
        if log is not None:
            with open(log, "a", encoding='utf-8') as f:
                print(f"对输入检索增强结果：\n{context}\n", file=f)
        return context


if __name__ == "__main__":
    # clean_agent = DataCleaner()
    # with open("./ref/tmp", "r", encoding='utf-8') as f:
    #     data = f.read()
    # cleaned_data = clean_agent.clear(data)
    # with open("./ref/data", "a", encoding='utf-8') as f:
    #     print(cleaned_data, file=f)

    input = """
    学长您好，学生会这学期拟举行一个大模型相关的比赛，目前的想法是调参赛（给定数据集和基本的代码，让选手调参）。想请问你们Linux社是否能接下出题的任务[可怜][可怜][可怜]

    北京大学信息科学技术学院举办"AI与大模型"主题活动，旨在搭建产学研深度对话平台，通过前沿技术分享、应用场景探讨与跨学科思维碰撞，推动大模型技术的创新突破与落地实践。

    活动聚焦三大核心目标：
    一是系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；
    二是构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；
    三是激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展。

    工作安排：4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送
    """

    rag_agent = Retriever()
    context = rag_agent.retrieve(input)
    print(context)