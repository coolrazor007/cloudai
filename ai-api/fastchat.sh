#!/bin/bash

# Default to the environment variables
MODEL=${AI_MODEL}
NAME=${AI_NAME}

# Parse command-line parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model) MODEL="$2"; shift ;;
        --name) NAME="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "Model to load: $MODEL"
echo "Name for model: $NAME"

# Launch three processes in the background
python3 -m fastchat.serve.controller --host=0.0.0.0 &
pids+=($!)
#sleep 10 && python3 -m fastchat.serve.model_worker --model-path $AI_MODEL --host=0.0.0.0 &
sleep 10 && python3 -m fastchat.serve.model_worker --model-path "${MODEL}" --model-names "${NAME}" --num-gpus 2 --max-gpu-memory 9GiB --host=0.0.0.0 &
pids+=($!)
sleep 60 && python3 -m fastchat.serve.gradio_web_server --host=0.0.0.0 --port 7860 &
pids+=($!)
sleep 5 && python3 -m fastchat.serve.openai_api_server --host=0.0.0.0 --port 8000 &
pids+=($!)


# Trap the TERM signal and kill the background processes
trap 'kill ${pids[@]}' TERM

# Wait for any child processes to complete
wait