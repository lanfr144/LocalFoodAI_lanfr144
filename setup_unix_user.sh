#!/bin/bash
# create unix service user for Food AI
USERNAME="food_ai"
PASSWORD="BTSai123"
# Check if user exists
if id -u $USERNAME >/dev/null 2>&1; then
  echo "User $USERNAME already exists"
else
  sudo net user $USERNAME $PASSWORD /add
  # Add to docker-users group (Docker Desktop group on Windows)
  sudo net localgroup docker-users $USERNAME /add
  echo "User $USERNAME created and added to docker-users group"
fi
