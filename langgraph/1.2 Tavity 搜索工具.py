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
from os import getenv
from dotenv import load_dotenv

load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults

tool = TavilySearchResults(max_results=2) 
print(tool.invoke("What's a 'node' in LangGraph?"))
