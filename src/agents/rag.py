# from typing import TypedDict
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import (
    AIMessage, SystemMessage, ToolMessage, HumanMessage
)
from langchain.chat_models import init_chat_model
import random
import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_ID = os.getenv('OPENAI_VECTOR_STORE_ID')

openai_vector_store_ids = [
    VECTOR_STORE_ID
]

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids
}

llm = init_chat_model("openai:gpt-4o", temperature=0.5)
llm = llm.bind_tools([file_search_tool])


class State(MessagesState):
    customer_name: str
    my_age: int


def extractor(state: State):
    return {}


# la función principal de un nodo es actualizar el estado
def conversation(state: State):
    new_state: State = {}
    history = state["messages"]
    if not history:
        history = [HumanMessage(content="Hola, ¿cómo estás?")]
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(20, 30)
    ai_message = llm.invoke(history[-3:])

    if isinstance(ai_message.content, list):
        text = " ".join(
            block.get("text", "")
            for block in ai_message.content
            if isinstance(block, dict) and block.get("type") == "text"
        )
        ai_message = AIMessage(content=text)

    new_state["messages"] = [ai_message]
    print(new_state)
    return new_state


builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()
