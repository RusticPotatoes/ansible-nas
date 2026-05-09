ARG BASE=nvidia/cuda:12.3.0-runtime-ubuntu22.04
# ARG BASE_IMAGE=base
FROM ${BASE} AS base

# Set environment PATH for local installations
ENV PATH="/root/.local/bin:$PATH"
# Set non-interactive mode to prevent tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive
# Install system packages
RUN apt-get update && \
    apt-get install -y gcc g++ make wget git calibre ffmpeg libmecab-dev mecab mecab-ipadic-utf8 libsndfile1-dev libc-dev curl espeak-ng sox && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install Rust compiler
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# Copy the application
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Install UniDic (non-torch dependent)
RUN pip install --no-cache-dir unidic-lite unidic && \
    python3 -m unidic download && \
    mkdir -p /root/.local/share/unidic
ENV UNIDIC_DIR=/root/.local/share/unidic

# Expose the required port
EXPOSE 7860
# Start the Gradio app with the required flag
ENTRYPOINT ["python", "app.py", "--script_mode", "full_docker"]


#docker build --pull --build-arg BASE_IMAGE=athomasson2/ebook2audiobook:latest -t your-image-name .
#The --pull flag forces Docker to always try to pull the latest version of the image, even if it already exists locally.
#Without --pull, Docker will only use the local version if it exists, which might not be the latest.