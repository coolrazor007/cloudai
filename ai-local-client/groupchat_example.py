from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import autogen
from autogen.retrieve_utils import TEXT_FORMATS
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

config_list_gpt = [
        {
            "model": "6ae1e4ae2cfbaf107c705ed722ec243b4f88014d",
            "api_base": "http://host.docker.internal:8000/v1",
            "api_type": "open_ai",
            "api_key": "NULL", # just a placeholder
        }
    ]
#/root/.cache/huggingface/hub/models--TheBloke--Mistral-7B-Instruct-v0.1-GPTQ/snapshots/6ae1e4ae2cfbaf107c705ed722ec243b4f88014d/

gpt_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list_gpt,
    "request_timeout": 600,
}
user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
   code_execution_config=False,
)

DocumentationAssistant = RetrieveAssistantAgent(
    name="DocumentationAssistant", 
    system_message="You are a helpful documentation library assistant.",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list_gpt,
    },
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "code",
        "docs_path": "./coding/documentation",
        "chunk_token_size": 2000,
        "model": config_list_gpt,
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "embedding_model": "all-mpnet-base-v2",
    },
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt_config,
    system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
''',
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code."""
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
''',
    llm_config=gpt_config,
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False, # set to True or image name like "python:3"
    },
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt_config,
)

# reset the assistant. Always reset the assistant before starting a new conversation.
#assistant.reset()

groupchat = autogen.GroupChat(agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt_config)




user_proxy.initiate_chat(
    manager,
    message="""
Goal: Create a basic Python function that uses the ElevenLabs Python module to speak text.
Critical Parts: 
Must use the latest ElevenLabs Python module
Use the already existing ELEVENLABS_KEY environment variable to provide the API key
Code Snippets:
    import os
    from elevenlabs import set_api_key, voices, generate, stream, play, UnauthenticatedRateLimitError
    set_api_key(os.getenv("ELEVENLABS_KEY"))


""",
)