# cloudai

## Quickstart

```
pip install huggingface_hub[cli]
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GPTQ

docker build . --no-cache -t ai-api
docker run -it -v /home/$(whoami)/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ -v /home/$(whoami)/.cache/huggingface/token:/root/.cache/huggingface/token:ro -p 8000:8000 -p 7860:7860 --gpus all --name ai-api ai-api

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