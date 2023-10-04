### cuda 12 not really supported yet by some dependencies
#FROM nvidia/cuda:12.2.0-devel-ubuntu22.04
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HUGGINGFACE_API_KEY $HUGGINGFACE_API_KEY

# Set work directory
WORKDIR /app

# Install packages
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev python3-venv git git-lfs build-essential clang g++ nano wget curl libssl-dev libffi-dev
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install dependencies
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
#RUN pip3 install git+https://github.com/huggingface/transformers.git@72958fcd3c98a7afdc61f953aa58c544ebda2f79
RUN pip3 install git+https://github.com/huggingface/transformers.git
#Needed for AutoGPTQ to run better
RUN pip3 install exllama gekko
RUN pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
RUN pip3 install git+https://github.com/lm-sys/FastChat.git
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

#RUN huggingface-cli login --token $HUGGINGFACE_API_KEY

# Run the command to start Uvicorn
CMD ["./fastchat.sh]
