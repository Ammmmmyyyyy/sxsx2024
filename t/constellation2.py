import httpx
import json
from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import time
from langchain_core.pydantic_v1 import BaseModel,Field
from fuzzywuzzy import fuzz
import re
def get_ali_api(str):
    host = 'https://ali-star-lucky.showapi.com'
    path = '/star'
    appcode = '6685c9f6da73471dba8f2e0e6dc0f27c'
    
    # 动态构建查询字符串
    querys = str
    url = f'{host}{path}?{querys}'

    headers = {
        'Authorization': f'APPCODE {appcode}'
    }

    response = httpx.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        json_content = response.json()
        formatted_json = json.dumps(json_content, ensure_ascii=False, indent=4)
        return formatted_json
    else:
        return f"请求失败，状态码: {response.status_code}"

#print(get_ali_api())
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())
#client  = ZhipuAI()
store = {}
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]



tagging_prompt = ChatPromptTemplate.from_messages(
    [("system",'''请提供一段具体的文本内容以便我从中抽取信息。
仅提取“Classification”函数中提到的属性。
'''),
    ("user",'''{input}''')
    ]
)
from typing import Optional
class Classification(BaseModel):
    constellation: str = Field(..., enum=["baiyang", "jinniu", "shuangzi" ,"juxie", "shizi", "chunv" ,"tiancheng", "tianxie", "sheshou" ,"mojie", "shuiping", "shuangyu" ,])
    needMonth:  Optional[int] = Field(
  
        description="是否需要对本月进行预测",
        enum=[0,1],
        default=0
    )
    needWeek: Optional[int] = Field(
      
        description="是否需要对本周进行预测",
        enum=[0,1],
        default=0
    )
    needYear: Optional[int] = Field(
      
        description="是否需要对本年进行预测",
        enum=[0,1],
        default=0
    )
    needTomorrow: Optional[int] = Field(
      
        description="是否需要对明天进行预测",
        enum=[0,1],
        default=0
    )

    
llm = ChatOpenAI(
    base_url="https://open.bigmodel.cn/api/paas/v4",
    api_key=os.environ["ZHIPUAI_API_KEY"],
    model="glm-4",
).with_structured_output(Classification)
    
tagging_chain = tagging_prompt | llm
def process_input(question):
    greeting_pattern = re.compile(r"^(开始|运势|测试|你好|嗨|早上好|晚上好)$")
    horoscope_pattern = re.compile(r"(明天|本周|本月|本年)")
    if greeting_pattern.match(question):
        return "我是一个星座运势测试助手。请告诉我你的星座以及你想分析明天、本周、本月、本年中哪些时间段的运势。"
    elif horoscope_pattern.search(question):
        # 构造查询字符串
        output=tagging_chain.invoke({"input": question}).dict()
        formatted_string = f"needMonth={output['needMonth']}&star={output['constellation']}&needWeek={output['needWeek']}&needTomorrow={output['needTomorrow']}&needYear={output['needYear']}"
        return get_ali_api(formatted_string)
    else:
        return question
#print(tagging_chain.invoke({"input": "我想要知道金牛座本周和本年的运势，不要回答明天。"}).dict())

llm2 = ChatOpenAI(
    base_url="http://api.baichuan-ai.com/v1",
    api_key=os.environ["BAICHUAN_API_KEY"],
    model="Baichuan4",
)

prompt_template = ChatPromptTemplate.from_messages(
    [("system",'''你是一个运势测试助手,如果你收到的输入是关于运势的分析，你的回答要满足以下条件：
1.你的回答应该以“根据星座运势”作为开头。并且你的回答应该包含输入的所有内容。你回答的内容要尽可能的多，并且要根据预测的时间（比如明天、本周、本月、本年）分段作答。
答案请按
“
<<<明天>>>
<<<本周>>>
<<<本月>>>
<<<本年>>>
”的格式输出。
2.若你获得的输入不包含上述某一个或几个时间，则不答。
3.你的回答不要包括“get_ali_api(str)”这样的文字。
4.并且你的回答应该以“感谢您的查询，以上是我对您的运势分析”作为结尾。
5.你的回答不要从记忆中提取，只能且必须从输入中提取。

如果你收到的输入是“我是一个星座运势测试助手。请告诉我你的星座以及你想分析明天、本周、本月、本年中哪些时间段的运势。”请原封不动地输出。
'''),
    MessagesPlaceholder(variable_name="history"),
    ("user",'''{question}''')
    ]
)

chat_chain = prompt_template | llm2
chain = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

config = {
    "configurable":{
        "session_id":time.time(),
    }
}
def answer_with_ali(question):
    ali_api_result = process_input(question)
        # 再将结果传递给模型
    response = chain.invoke({"question":ali_api_result},config=config)
    return response.content
#print(answer_with_ali("我是金牛座，我要对明天和本周的运势进行预测。")) 
