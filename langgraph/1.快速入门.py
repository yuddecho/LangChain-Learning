"""
学习 LangGraph 的基础知识，您将在其中从头开始构建一个智能体
ref: https://github.langchain.ac.cn/langgraph/tutorials/introduction/

langsmith: https://smith.langchain.com/onboarding

在本综合快速入门中，我们将构建一个 LangGraph 支持聊天机器人，它可以

    通过搜索网络回答常见问题
    维护跨通话的对话状态
    将复杂查询路由到人工进行审核
    使用自定义状态来控制其行为
    倒带并探索替代的对话路径

"""
from typing import Annotated

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from os import getenv
from dotenv import load_dotenv

load_dotenv()


# 1 定义搜索工具
from langchain_community.tools.tavily_search import TavilySearchResults 
tool = TavilySearchResults(max_results=2) 
tools = [tool] 

# 2 定义状态图
class State(TypedDict):
    # 首先定义图的 State
    # State 包含图的模式以及 reducer 函数，这些函数指定如何将更新应用于状态。在我们的示例中
    messages: Annotated[list, add_messages]

graph = StateGraph()

