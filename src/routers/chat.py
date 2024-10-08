from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from src.config import get_settings
from src.prompt import ADVISOR_PROMPT
from src.utils import get_vector_db


class ChatMessage(BaseModel):
    message: str


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/stream")
async def stream_chat(
    chat_message: ChatMessage,
    vector_db=Depends(get_vector_db),
    settings=Depends(get_settings),
):
    callback = AsyncIteratorCallbackHandler()
    relevant_docs = vector_db.similarity_search(chat_message.message, k=5)

    # Prepare context from relevant documents
    context = "\n".join([doc.page_content for doc in relevant_docs])

    prompt = ADVISOR_PROMPT.format(
        relevant_docs=context, user_question=chat_message.message
    )

    model = ChatOpenAI(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        temperature=0.7,
        streaming=True,
        callbacks=[callback],
        openai_api_key=settings.openai_api_key,
    )

    async def event_generator():
        async for chunk in model.astream([HumanMessage(content=prompt)]):
            yield f"{chunk.content}"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
