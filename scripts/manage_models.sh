#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:manage_models.sh:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

echo "Pulling the new efficient billion-parameter model (llama3.2-vision:11b)..."
docker exec food-ollama-1 ollama pull llama3.2-vision:11b

echo "Cleaning up unused models to free up disk space..."
docker exec food-ollama-1 ollama rm qwen2.5:7b
docker exec food-ollama-1 ollama rm llama3.2:3b

echo "Currently installed models:"
docker exec food-ollama-1 ollama list

echo "Model management complete!"
