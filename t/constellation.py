from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import time

from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())

store = {}
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

llm = ChatOpenAI(
    base_url="http://api.baichuan-ai.com/v1",
    api_key=os.environ["BAICHUAN_API_KEY"],
    model="Baichuan4",
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",'''你是一个有关于mbti的大模型。
                    如果我想测试mbti，实际上你不需要给我一个简化的过程帮助我自我评估，你只需要简单介绍一下mbti，并引导我去官方网站检测。
                    你的回答不要使用markdown格式。'''),
        MessagesPlaceholder(variable_name="history"),
        ("user", '''{question}''')
    ]
)

chat_chain = prompt_template | llm

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

# 示例使用
""" question = "你能给我解释一下mbti吗？"  
response = chain.invoke({"question":question},config=config)
print(response) """