# https://openrouter.ai/docs/community/frameworks

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

from os import getenv
from dotenv import load_dotenv

load_dotenv()

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = ChatOpenAI(
  openai_api_key=getenv("OPENROUTER_API_KEY"),
  openai_api_base=getenv("OPENROUTER_BASE_URL"),
  model_name=getenv("MODEL_NAME")
)

llm_chain = prompt | llm | StrOutputParser()

# question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

print(llm_chain.invoke({"question": "请问什么是OpenRouter"}))
