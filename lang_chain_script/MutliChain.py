import os
from dotenv import load_dotenv
from langchain_classic.chains import LLMChain, SimpleSequentialChain
from langchain_classic.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")  # DeepSeek 的基础 URL
llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

# location 链
# llm = OpenAI(temperature=1)
template = """你的工作是查询，{topic}有什么重大的外交事件，列举5个, 越近时间的加权越大.

YOUR RESPONSE:
"""

prompt_template = PromptTemplate(input_variables=["topic"], template=template)
diplomatic_events_chain = LLMChain(llm=llm, prompt=prompt_template)

# meal 链
template = """根据外交事件，分析其对A股的影响，并输出利空、利多各5只股票，并相应的对股票影响程度打分，100分为最大影响值.
% diplomatic_events
{diplomatic_events}

YOUR RESPONSE:
"""
prompt_template = PromptTemplate(input_variables=["diplomatic_events"], template=template)
stock_chain = LLMChain(llm=llm, prompt=prompt_template)

# 通过 SimpleSequentialChain 串联起来，第一个答案会被替换第二个中的 diplomatic_events，然后再进行询问
overall_chain = SimpleSequentialChain(chains=[diplomatic_events_chain, stock_chain], verbose=True)
result = overall_chain.run("中国未来1个月")
print(result)