from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import asyncio
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage
from langchain.chains import ConversationalRetrievalChain


from utils import get_vector_db
from prompt import ADVISOR_PROMPT


class ChatMessage(BaseModel):
    message: str

router = APIRouter(prefix='/chat', tags=['chat'])

#def get_retriever():
#    vector_db = get_vector_db()
#    return vector_db.as_retriever()

@router.post("/stream")
async def stream_chat(chat_message: ChatMessage, vector_db = Depends(get_vector_db)):
    callback = AsyncIteratorCallbackHandler()
    relevant_docs = vector_db.similarity_search(chat_message.message, k=5)
    
    # Prepare context from relevant documents
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = ADVISOR_PROMPT.format(relevant_docs=context, user_question=chat_message.message)
    
    model = ChatOpenAI(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        temperature=0.7,
        streaming = True,
        callbacks=[callback]
    )

    async def event_generator():
        async for chunk in model.astream([HumanMessage(content=prompt)]):
            yield f"{chunk.content}"
                
        
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")