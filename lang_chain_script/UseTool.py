import os
from dotenv import load_dotenv
from langchain_classic.agents import initialize_agent, Tool, AgentType
from langchain_classic.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_classic import LLMMathChain

load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")  # DeepSeek 的基础 URL
llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

# 初始化搜索链和计算链
def search_tool(query: str) -> str:
    return "Search tool not configured. Provide SERPAPI_API_KEY to enable."

llm_math_chain = LLMMathChain(llm=llm, verbose=True)

# 创建一个功能列表，指明这个 agent 里面都有哪些可用工具，agent 执行过程可以看必知概念里的 Agent 那张图
tools = [
    Tool(
        name="Search",
        func=search_tool,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]

# 初始化 agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 执行 agent
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")
