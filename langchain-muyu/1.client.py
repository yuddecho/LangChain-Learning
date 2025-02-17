from zhipuai import ZhipuAI

client = ZhipuAI(api_key="9a523c8b1e8145bcb9755a876611b372.mEg9L0BVnBsAHytk11")  # 请填写您自己的API Key
response = client.chat.completions.create(
  model="glm-4-0520",  # 填写需要调用的模型编码
  messages=[
      {"role": "user", "content": "你好！你叫什么名字"},
  ],
  stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)