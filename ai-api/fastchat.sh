#!/bin/bash

# Launch three processes in the background
python3 -m fastchat.serve.controller --host=0.0.0.0 &
pids+=($!)
sleep 10 && python3 -m fastchat.serve.model_worker --model-path /root/.cache/huggingface/hub/models--TheBloke--Mistral-7B-Instruct-v0.1-GPTQ/snapshots/6ae1e4ae2cfbaf107c705ed722ec243b4f88014d/ --host=0.0.0.0 &
#sleep 10 && python3 -m fastchat.serve.model_worker --model-path /root/.cache/huggingface/hub/models--TheBloke--Mistral-7B-Instruct-v0.1-GPTQ/snapshots/6ae1e4ae2cfbaf107c705ed722ec243b4f88014d/ --num-gpus 2 --max-gpu-memory 9GiB --host=0.0.0.0 &
pids+=($!)
sleep 30 && python3 -m fastchat.serve.gradio_web_server --host=0.0.0.0 --port 7860 &
pids+=($!)
sleep 2 && python -m fastchat.serve.openai_api_server --host=0.0.0.0 --port 8000 &
pids+=($!)


# Trap the TERM signal and kill the background processes
trap 'kill ${pids[@]}' TERM

# Wait for any child processes to complete
wait