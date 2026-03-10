import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain_classic.chains import LLMChain, SimpleSequentialChain
from langchain_classic.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.deepseek.com/v1")  # DeepSeek 的基础 URL
llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)

# location 链
# llm = OpenAI(temperature=1)
template = """你的工作是查询，{topic}，列举5个, 越近时间的加权越大.

YOUR RESPONSE:
"""

prompt_template = PromptTemplate(input_variables=["topic"], template=template)
diplomatic_events_chain = LLMChain(llm=llm, prompt=prompt_template)

# meal 链
template = """根据事件，分析其对A股的影响，并输出利空、利多各5只股票，并相应的对股票影响程度打分，100分为最大影响值.
% diplomatic_events
{diplomatic_events}

YOUR RESPONSE:
"""
prompt_template = PromptTemplate(input_variables=["diplomatic_events"], template=template)
stock_chain = LLMChain(llm=llm, prompt=prompt_template)

topic = "中国2026年3月份到4月份有什么重大的外交事件"
diplomatic_events = diplomatic_events_chain.invoke({"topic": topic})
stock_analysis = stock_chain.invoke({"diplomatic_events": diplomatic_events})

output_dir = Path(__file__).resolve().parents[1] / "gen" / "StockAnalysis"
output_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
output_path = output_dir / f"{timestamp}.md"

output_path.write_text(
    "\n".join(
        [
            "# 外交事件",
            diplomatic_events,
            "",
            "# A股影响分析",
            stock_analysis,
            "",
        ]
    ),
    encoding="utf-8",
)

print(output_path)