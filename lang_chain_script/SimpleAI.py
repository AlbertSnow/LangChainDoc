import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")  # DeepSeek 的基础 URL
llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

result = llm.invoke("日韩估时暴跌，韩国触发熔断机制。这对A股会有什么影响吗？请列出最受影响导致 看好和看空 的各五家公司。")
print(result.content)