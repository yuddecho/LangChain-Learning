# https://bigmodel.cn/dev/api/thirdparty-frame/langchain-sdk
# pip install -qU langchain langchain-openai
# pip install langchain langchainhub httpx_sse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

model = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="9a523c8b1e8145bcb9755a876611b372.mEg9L0BVnBsAHytk11",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)


# 定义提⽰模板
prompt = PromptTemplate(
    input_variables = ["question"],
    template = "你是⼀个乐于助⼈的智能⼩助理。擅⻓根据⽤⼾输⼊的问题给出⼀个简短的回答：: {question}"
)
# 构建Chains
chain = (
    prompt
    | model
    | StrOutputParser()
)

print(prompt.input_schema.model_json_schema())
print(chain.invoke({"question": "请问什么是LangChain？"}))