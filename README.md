# cloudai

## Quickstart

```
pip install -U huggingface_hub
pip install -U huggingface_hub[cli]
#using an environment variable for the huggingface token
huggingface-cli login --token $HUGGINGFACE_TOKEN
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GPTQ

cd ai-api
docker build . --no-cache -t ai-api
docker run -it -v /home/$(whoami)/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ -p 8000:8000 -p 7860:7860 --gpus all --name ai-api ai-api

```

## AutoGen code for local
```
config_list = [
        {
            "model": "6ae1e4ae2cfbaf107c705ed722ec243b4f88014d",
            "api_base": "http://host.docker.internal:8000/v1",
            "api_type": "open_ai",
            "api_key": "NULL", # just a placeholder
        }
    ]

gpt_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "request_timeout": 600,
}
```
## Models

Use Huggingface-cli/Huggingface-hub to download the models locally first (you do not want the models INSIDE the container).  This way you mount them.
Because of this you will need to edit the "fastchat.sh" with the correct path.

## ai-api (WIP - because I broke it)

Quick commands:

```
docker compose build --no-cache 
docker compose up -d 
docker container logs -f ai-api 
docker compose down

```

## Docker

### ai-api
```
docker build . --no-cache -t cuda

docker run -it --env-file .env -v $(pwd):/app2/ -v /home/$(whoami)/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ -v /home/$(whoami)/.cache/huggingface/token:/root/.cache/huggingface/token:ro -p 8000:8000 -p 7860:7860 --gpus all --name cuda cuda /bin/bash
```
### ai-local-client
```
docker build . --no-cache -t cuda2

docker run -it --env-file .env -v $(pwd):/app2/ --gpus all --name cuda2 cuda /bin/bash
```