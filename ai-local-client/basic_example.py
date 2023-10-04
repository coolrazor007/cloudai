from autogen import oai

# create a text completion request
response = oai.Completion.create(
    config_list=[
        {
            "model": "6ae1e4ae2cfbaf107c705ed722ec243b4f88014d",
            "api_base": "http://host.docker.internal:8000/v1",
            "api_type": "open_ai",
            "api_key": "NULL", # just a placeholder
        }
    ],
    prompt="Hi",
)
print(response)

# create a chat completion request
response = oai.ChatCompletion.create(
    config_list=[
        {
            "model": "6ae1e4ae2cfbaf107c705ed722ec243b4f88014d",
            "api_base": "http://host.docker.internal:8000/v1",
            "api_type": "open_ai",
            "api_key": "NULL",
        }
    ],
    messages=[{"role": "user", "content": "Hi"}]
)
print(response)