import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings  # 轻量占位 Embedding
from langchain_classic.chains import RetrievalQA

# 2. 加载本地文档 (以 PDF 为例)
from tempfile import tempdir

# 1. 配置 DeepSeek API
# .env 文件中配置:
# OPENAI_API_KEY=sk-**********************
# OPENAI_API_BASE=https://api.deepseek.com/v1
load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")  # DeepSeek 的基础 URL

loader = PyPDFLoader("/Users/zhaojialiang/AI/LangChainDoc/DiDi.pdf")
data = loader.load()

# 3. 文档切片 (Chunking)
# 设置 chunk_overlap 保证语义连续性
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(data)

# 4. 创建向量数据库 (Chroma)
embeddings = FakeEmbeddings(size=768)
vectorstore = Chroma.from_documents(chunks, embeddings)

llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

# 6. 构建检索器与问答链
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)

# 7. 提问
question = "这个文档是在描述什么，关键数据是什么？"
result = qa_chain.invoke({"query": question})
print(result)
