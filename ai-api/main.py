import sys
import os
import time
from dotenv import load_dotenv
load_dotenv()

import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL")
temperature = float(os.getenv("TEMPERATURE"))

import custom_tools

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.agents import load_tools
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun

from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain.schema import output_parser

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    temperature=temperature,
    model_name=model
)
# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

tools = load_tools(["llm-math","wikipedia"], llm=llm)
tools += [custom_tools.DuckDuckGoSearchTool()]

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)


from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_memory import ChatMessageHistory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper

message_history = RedisChatMessageHistory(
    url="redis://redis:6379/0", ttl=600, session_id="my-session"
)

memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history
)

llm_chain = LLMChain(llm=OpenAI(temperature=temperature), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)

####################
# API Section
####################

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from elevenlabs import set_api_key, voices, generate, stream, play, UnauthenticatedRateLimitError
import os

class Message(BaseModel):
    content: str

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://razor-desktop:8080",
    "https://cloud.alethotech.com",
    "http://localhost:8080",  # Be sure to include the port your frontend is running on
    # # you can add more origins here if needed
    # "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/message/")
async def create_message(message: Message):
    try:
        response = agent_chain.run(input=message.content)
    except output_parser.OutputParserException as e:
        print(f"An OutputParserException occurred: {e}")
        response = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        response = None
        raise HTTPException(status_code=500, detail="An unexpected error occurred")    

    if response == None: response = "There was an error."
    return {"message": response}

set_api_key(os.getenv("ELEVENLABS_KEY"))

@app.get("/text_to_speech/")
async def text_to_speech(text: str):
    # Convert the text to speech using the ElevenLabs SDK
    audio_stream = generate(
        text=text,
        voice="Bella",
        stream=True
    )

    # Create a StreamingResponse object to stream the audio data
    return StreamingResponse(
        audio_stream,
        media_type='audio/mpeg',
    )