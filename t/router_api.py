from fastapi import APIRouter
from starlette.responses import StreamingResponse
from pydantic import BaseModel
import test as test_chain
import constellation as con_chain
import tarot as tarot_chain
import constellation2 as con2_chain
import json
from langchain_core.messages import AIMessageChunk

class Item(BaseModel):
    question: str
    config: str
    
class Item_input(BaseModel):
    input: str
    config: str
    

router = APIRouter()

@router.get("/api/chathello")
async def chathello():
    return {"message": "Hello, World!"}

async def generate_response(p_chain , question):
    # chat_chain.config["configurable"]["session_id"] = time.time()
    print(test_chain.config)
    async for message_chunk in p_chain.chain.astream(
        {"question":question},
        config=p_chain.config
    ):
        # 确保将AIMessageChunk对象转换为字符串
        if isinstance(message_chunk, AIMessageChunk):
            message_str = str(message_chunk.content)
        elif isinstance(message_chunk, str):
            message_str = message_chunk
        else:
            message_str = str(message_chunk)
        
        # 将字符串编码为字节流
        yield message_str.encode('utf-8')
        
async def generate_response_input(p_chain , question):
    # chat_chain.config["configurable"]["session_id"] = time.time()
    complete_response = ""
    async for message_chunk in p_chain.chain.astream(
        {"input":question},
        config=p_chain.config
    ):
        # 确保将AIMessageChunk对象转换为字符串
        if isinstance(message_chunk, AIMessageChunk):
            message_str = str(message_chunk.content)
        elif isinstance(message_chunk, str):
            message_str = message_chunk
        else:
            message_str = str(message_chunk)
        
        # 将字符串编码为字节流
        yield message_str.encode('utf-8')
    
@router.post("/api/test")
async def test(item:Item):
    print("传输的参数为：",item.question)
    return StreamingResponse(generate_response(test_chain,item.question ),media_type="text/event-stream")

@router.post("/api/constellation")
async def constellation(item:Item):
    print("传输的参数为：",item.question)
    return StreamingResponse(generate_response(con_chain,item.question ),media_type="text/event-stream")

@router.post("/api/constellation2")
async def constellation2(item:Item):
    print("传输的参数为：",item.question)
    output=con2_chain.process_input(item.question)
    return StreamingResponse(generate_response(con2_chain,output),media_type="text/event-stream")

@router.post("/api/tarot")
async def tarot(item:Item_input):
    print("传输的参数为：",item.input)
    return StreamingResponse(generate_response_input(tarot_chain,item.input ),media_type="text/event-stream")