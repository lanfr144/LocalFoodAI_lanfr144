---
description: Hardware limits pre-flight check before builds
---

# Agent Skill: Hardware Limits Pre-Flight Check

As an autonomous agent, you MUST execute this "pre-flight check" workflow **BEFORE** attempting any heavy or resource-intensive operations such as:
- `npm install`
- `docker build`
- `make`
- Heavy PyPI package compilations (e.g., `pip install` requiring local gcc compilation)

## Step 1: Resource Verification
Execute the necessary commands on the active environment to assess system resources:
- RAM Check: `free -m`
- Disk Check: `df -h`
- CPU/Load Check: `uptime`

Define the threshold for a safe build environment. For example:
- **RAM**: > 2048 MB available.
- **Disk**: > 5.0 GB available on root/workspace partition.
- **Load**: Average safely below the CPU core threshold.

## Step 2: Evaluation & Protocol Action

Evaluate the gathered resource parameters to determine the STATUS.

### ❌ Failure Protocol
If **STATUS: FAIL** is determined (resources fall below safe operational thresholds):
1. **ABORT** the planned build action immediately.
2. **ANALYSIS**: Identify memory-hogging processes by executing:
   ```bash
   top -b -n1 | head -n 20
   ```
3. **PROPOSAL**: Output the analysis and proactively ask the user if they want to:
   - Clear caches (e.g., `docker system prune`, `npm cache clean --force`, or `apt clean`).
   - Increase swap space before retrying.
   - Terminate specific high-usage processes.
4. **DO NOT** attempt to "force" the build. Stop execution and wait for the user's explicit response.

### ✅ Success Protocol
If **STATUS: PASS** is determined (resources are healthy):
1. Note the current timestamp and a brief summary of the resource levels to the conversation log.
2. Proceed safely with executing the planned build/install action.
