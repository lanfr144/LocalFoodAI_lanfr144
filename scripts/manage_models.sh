#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:manage_models.sh:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Load LLM_MODEL from .env
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    LLM_MODEL=$(grep '^[ \t]*LLM_MODEL[ \t]*=' "$ENV_FILE" | sed 's/^.*=//' | tr -d '\r\n ')
elif [ -f "../.env" ]; then
    ENV_FILE="../.env"
    LLM_MODEL=$(grep '^[ \t]*LLM_MODEL[ \t]*=' "$ENV_FILE" | sed 's/^.*=//' | tr -d '\r\n ')
fi

if [ -z "$LLM_MODEL" ]; then
    echo "LLM_MODEL not found in .env, defaulting to llama3.2:3b"
    LLM_MODEL="llama3.2:3b"
fi

# Detect Ollama container dynamically
OLLAMA_CONTAINER=$(docker ps --format '{{.Names}}' | grep "ollama" | head -n 1)
if [ -z "$OLLAMA_CONTAINER" ]; then
    echo "No running Ollama container found. Defaulting to localfoodai_lanfr144-ollama-1"
    OLLAMA_CONTAINER="localfoodai_lanfr144-ollama-1"
fi

echo "Active Ollama container: $OLLAMA_CONTAINER"
echo "Target LLM Model from .env: $LLM_MODEL"

echo "Pulling model ($LLM_MODEL)..."
docker exec "$OLLAMA_CONTAINER" ollama pull "$LLM_MODEL"

echo "Cleaning up unused models from container..."
# List all running models, skip header, extract names, and remove those not matching target LLM_MODEL
docker exec "$OLLAMA_CONTAINER" ollama list | tail -n +2 | awk '{print $1}' | while read -r model; do
    if [ ! -z "$model" ] && [ "$model" != "$LLM_MODEL" ] && [ "$model" != "${LLM_MODEL}:latest" ] && [ "${model}:latest" != "$LLM_MODEL" ]; then
        echo "Removing unused model: $model"
        docker exec "$OLLAMA_CONTAINER" ollama rm "$model"
    fi
done

echo "Currently installed models inside container:"
docker exec "$OLLAMA_CONTAINER" ollama list

echo "Model management complete!"