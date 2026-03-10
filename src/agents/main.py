import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# TOOL para el mockup
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


gemini_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_tokens=500,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        # convert_system_message_to_human=True
    )


agent = create_agent(
    model=gemini_model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
    # api_key=api_key
)

# # Run the agent
# agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
# )
