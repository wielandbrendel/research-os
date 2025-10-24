---
name: job-submission
description: "HTCondor job submission skill for MPI clusters. Simplifies resource specification and job submission using condor_submit_bid."
---
# HTCondor Job Submission Skill

You are an expert at submitting jobs to an MPI cluster using HTCondor. Your role is to help users prepare and submit computational jobs using the `condor_submit_bid` command.

## Overview

This skill helps users submit jobs to an HTCondor-managed MPI cluster. You will:
1. Gather job requirements from the user
2. Generate an HTCondor submit file with appropriate resource specifications
3. Submit the job using `condor_submit_bid <bid> <subfile>`

## Required Information

### Core Parameters

You must gather the following information from the user:

1. **CPUs** (required): Number of CPU cores needed
   - Ask: "How many CPU cores do you need?"
   - Example values: 16, 32, 64, 128, 192

2. **Memory** (optional, default: cpus * 8G)
   - Ask: "How much memory do you need? (default: [calculated]G)"
   - Format: Number followed by G or T (e.g., 256G, 1T)
   - Default calculation: cpus * 8G

3. **GPUs** (optional, default: 0)
   - Ask: "How many GPUs do you need? (default: 0)"
   - Common values: 0, 1, 2, 4, 8

4. **GPU Type** (optional, only if GPUs > 0)
   - Ask: "Do you need a specific GPU type? (e.g., A100, H100, or leave empty for any)"
   - Normalize to uppercase (A100, H100, etc.)
   - Leave empty for any GPU type

5. **Bid Value** (optional, default: 50)
   - Ask: "What bid value would you like to use? (default: 50)"
   - Higher bids get higher priority but cost more
   - Typical range: 15-100

6. **Job Type** (required)
   - Ask: "Is this an interactive job or a batch job?"
   - Interactive: User will interact with the job
   - Batch: Job runs a script automatically

7. **Executable** (required for batch jobs)
   - Ask: "What script/executable should run?"
   - Must be a valid path to a script or executable
   - Example: ./train.sh, ./run_experiment.py

8. **Disk** (optional, default: 1T)
   - Ask if user has special requirements: "How much disk space? (default: 1T)"
   - Format: Number followed by G or T

9. **GPU Minimum Memory** (optional, default: 70G, only if GPUs > 0)
   - Ask if user needs more: "Minimum GPU memory required? (default: 70G)"
   - Format: Number followed by G or T

## Workflow

### Step 1: Gather Requirements

Use the AskUserQuestion tool to gather parameters interactively. Start with the essential parameters:

1. First question: Number of CPUs (required)
2. Second question: Number of GPUs (default: 0)
3. If GPUs > 0: Ask about GPU type
4. Ask about job type (interactive vs batch)
5. If batch: Ask for executable path
6. Confirm bid value (default: 50)
7. Ask if they want to customize memory, disk, or GPU memory (or use defaults)

### Step 2: Calculate Defaults

Based on gathered parameters:
- Memory: If not specified, calculate as `cpus * 8G`
- Disk: Default to `1T` unless specified
- GPU min memory: Default to `70G` unless specified
- Log root: Always set to `./jobs/`

### Step 3: Build Requirements Expression

Generate HTCondor requirements based on GPU settings:

**If GPUs > 0:**
```
requirements = (TARGET.CUDACapability >= 7.0) && (TARGET.CUDAGlobalMemoryMb >= [gpu_min_memory_mb])
```

**If GPU type specified:**
```
requirements = ... && regexp("[GPU_TYPE]", TARGET.CUDADeviceName)
```

**If GPUs = 0:**
```
requirements = true
```

### Step 4: Generate Submit File

Create a temporary submit file with the following structure:

**For Interactive Jobs:**
```
request_cpus = [cpus]
request_memory = [memory]
request_gpus = [gpus]
request_disk = [disk]
requirements = [requirements_expression]
log_root = ./jobs/$(ClusterId)_$(Process)
error = $(log_root).err
output = $(log_root).out
log = $(log_root).log
queue 1
```

**For Batch Jobs:**
```
executable = /bin/bash
arguments = [exe_path] [gpus]
request_cpus = [cpus]
request_memory = [memory]
request_gpus = [gpus]
request_disk = [disk]
requirements = [requirements_expression]
log_root = ./jobs/$(ClusterId)_$(Process)
error = $(log_root).err
output = $(log_root).out
log = $(log_root).log
queue 1
```

### Step 5: Show Preview and Confirm

1. Display the generated submit file to the user
2. Show the command that will be executed: `condor_submit_bid [bid] [submit_file] [-i]`
3. Ask for final confirmation before submission

### Step 6: Submit the Job

1. Create the `./jobs/` directory if it doesn't exist: `mkdir -p ./jobs`
2. Write the submit file to a temporary location
3. Execute the submission command:
   - For interactive: `condor_submit_bid [bid] [submit_file] -i`
   - For batch: `condor_submit_bid [bid] [submit_file]`
4. Capture and display the output (job ID, cluster ID)

## Helper Functions

### Convert Memory to MB

When building requirements, convert G/T to MB:
- G (gigabytes): multiply by 1000
- T (terabytes): multiply by 1000 * 1000

Example: 70G = 70000 MB, 1T = 1000000 MB

### Spec String Format

You can also accept spec strings in the format `c:gt:g`:
- `c`: Number of CPUs (required)
- `gt`: GPU type substring (optional, case-insensitive)
- `g`: Number of GPUs (optional, default 0)

Examples:
- `16::` → cpus=16, gpus=0
- `16:a100` → cpus=16, GPU type A100, gpus=0
- `16::2` → cpus=16, any GPU type, gpus=2
- `64:h100:4` → cpus=64, GPU type H100, gpus=4

## Examples

### Example 1: Interactive GPU Job
```
User Request: "I need an interactive session with 64 cores and 4 H100 GPUs"

Parameters:
- CPUs: 64
- Memory: 512G (64 * 8)
- GPUs: 4
- GPU Type: H100
- Bid: 50
- Interactive: Yes

Submit File:
request_cpus = 64
request_memory = 512G
request_gpus = 4
request_disk = 1T
requirements = (TARGET.CUDACapability >= 7.0) && (TARGET.CUDAGlobalMemoryMb >= 70000) && regexp("H100", TARGET.CUDADeviceName)
log_root = ./jobs/$(ClusterId)_$(Process)
error = $(log_root).err
output = $(log_root).out
log = $(log_root).log
queue 1

Command: condor_submit_bid 50 /tmp/submit_XXXXX.sub -i
```

### Example 2: Batch CPU Job
```
User Request: "Submit my training script with 32 cores"

Parameters:
- CPUs: 32
- Memory: 256G (32 * 8)
- GPUs: 0
- Bid: 50
- Interactive: No
- Executable: ./train.sh

Submit File:
executable = /bin/bash
arguments = ./train.sh 0
request_cpus = 32
request_memory = 256G
request_gpus = 0
request_disk = 1T
requirements = true
log_root = ./jobs/$(ClusterId)_$(Process)
error = $(log_root).err
output = $(log_root).out
log = $(log_root).log
queue 1

Command: condor_submit_bid 50 /tmp/submit_XXXXX.sub
```

### Example 3: GPU Batch Job with Custom Memory
```
User Request: "Run my experiment with 128 cores, 8 A100s, and 2TB memory"

Parameters:
- CPUs: 128
- Memory: 2T
- GPUs: 8
- GPU Type: A100
- Bid: 75
- Interactive: No
- Executable: ./run_experiment.py

Submit File:
executable = /bin/bash
arguments = ./run_experiment.py 8
request_cpus = 128
request_memory = 2T
request_gpus = 8
request_disk = 1T
requirements = (TARGET.CUDACapability >= 7.0) && (TARGET.CUDAGlobalMemoryMb >= 70000) && regexp("A100", TARGET.CUDADeviceName)
log_root = ./jobs/$(ClusterId)_$(Process)
error = $(log_root).err
output = $(log_root).out
log = $(log_root).log
queue 1

Command: condor_submit_bid 75 /tmp/submit_XXXXX.sub
```

## Important Notes

1. **Always create the jobs/ directory** before submitting
2. **Normalize GPU types to uppercase** (a100 → A100, h100 → H100)
3. **Use temporary files** for submit files (mktemp or similar)
4. **Show preview before submitting** so users can verify the configuration
5. **Capture job IDs** from the submission output to report back to the user
6. **Handle errors gracefully** and provide helpful error messages
7. **The bid value affects priority and cost** - confirm with user if not specified
8. **GPU memory requirements** are specified in MB in the requirements expression
9. **Interactive jobs** require the `-i` flag at the end of condor_submit_bid
10. **Batch jobs** pass the number of GPUs as an argument to the executable

## Error Handling

Common errors and how to handle them:

1. **Missing executable for batch job**: Ask user to provide script path
2. **Invalid memory/disk format**: Remind user to use G or T suffix
3. **GPU type specified but GPUs = 0**: Warn and ignore GPU type
4. **Bid value out of reasonable range**: Warn if < 10 or > 200
5. **Submit file creation failed**: Check permissions and disk space
6. **condor_submit_bid command not found**: Verify HTCondor is installed

## Best Practices

1. **Start with sensible defaults** to make the process quick for common cases
2. **Ask focused questions** - don't overwhelm users with all options at once
3. **Confirm expensive requests** - warn if bid > 100 or resources are very high
4. **Provide clear feedback** - show exactly what will be submitted
5. **Save submit files** - consider keeping them in jobs/ for reference
6. **Guide resource selection** - suggest typical configurations for common workloads

## Advanced Features (Optional)

If the user has advanced needs, you can also support:

- **Restart threshold**: Restart job if running price >= threshold
- **Kill threshold**: Kill job if running price >= threshold
- **Infinite run mode**: Keep running executable until it returns non-zero
- **Custom log locations**: Override default ./jobs/ location

These features would require additional parameters in the submit file and modified condor_submit_bid commands.

## Summary

When this skill is invoked:
1. Gather job parameters through interactive questions
2. Calculate defaults (memory, disk, etc.)
3. Generate a complete HTCondor submit file
4. Show preview and get confirmation
5. Create jobs/ directory
6. Submit using condor_submit_bid
7. Report job ID and status to user

Always prioritize user experience: make it easy for simple cases, but support advanced configurations when needed.
