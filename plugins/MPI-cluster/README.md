# MPI-cluster Plugin

HTCondor job submission plugin for MPI clusters.

## Overview

This plugin provides a skill for submitting computational jobs to an MPI cluster managed by HTCondor. It simplifies the process of creating submit files and executing `condor_submit_bid` commands.

## Installation

The plugin is already available in the `plugins/MPI-cluster/` directory. To use it with Claude Code, ensure the plugin is loaded according to the Claude Code plugin documentation.

## Skill: job-submission

Submit jobs to the MPI cluster using HTCondor.

### Usage

Invoke the skill using the Skill tool in Claude Code:

```
/skill job-submission
```

or simply ask Claude to help you submit a job to the cluster.

### What It Does

The skill will guide you through:

1. **Gathering job requirements**
   - Number of CPUs (required)
   - Memory (default: cpus × 8G)
   - Number of GPUs (default: 0)
   - GPU type (optional, if GPUs > 0)
   - Job type (interactive or batch)
   - Executable path (for batch jobs)
   - Bid value (default: 50)

2. **Generating HTCondor submit file**
   - Configures resource requirements
   - Sets up GPU constraints if needed
   - Configures logging to `./jobs/` directory

3. **Submitting the job**
   - Creates jobs directory if needed
   - Executes `condor_submit_bid` with appropriate parameters
   - Reports job ID and status

### Examples

#### Example 1: Interactive GPU Session

```
User: "I need an interactive session with 64 cores and 4 H100 GPUs"

Claude will:
1. Confirm the parameters (CPUs: 64, GPUs: 4, Type: H100)
2. Calculate memory (512G = 64 × 8)
3. Generate submit file with GPU requirements
4. Submit: condor_submit_bid 50 <submit_file> -i
```

#### Example 2: Batch CPU Job

```
User: "Submit my training script with 32 cores"

Claude will:
1. Ask for the script path (e.g., ./train.sh)
2. Set CPUs: 32, Memory: 256G
3. Generate batch job submit file
4. Submit: condor_submit_bid 50 <submit_file>
```

#### Example 3: GPU Batch Job

```
User: "Run my experiment with 128 cores, 8 A100s, and 2TB memory"

Claude will:
1. Confirm parameters and ask for executable
2. Generate submit file with A100 GPU requirements
3. Submit with specified resources
```

### Spec String Format

You can also use spec strings in the format `cpus:gpu_type:gpus`:

- `16::` → 16 CPUs, 0 GPUs
- `16:a100` → 16 CPUs, A100 GPUs, 0 count (any available)
- `16::2` → 16 CPUs, 2 GPUs (any type)
- `64:h100:4` → 64 CPUs, 4 H100 GPUs

### Default Values

- **Memory**: cpus × 8G (e.g., 32 CPUs = 256G)
- **Disk**: 1T
- **GPU minimum memory**: 70G
- **Bid**: 50
- **Log directory**: ./jobs/

### Job Logs

All job logs are stored in `./jobs/` with the following naming:
- `<ClusterID>_<ProcessID>.err` - Standard error
- `<ClusterID>_<ProcessID>.out` - Standard output
- `<ClusterID>_<ProcessID>.log` - HTCondor log

## Requirements

- HTCondor must be installed and configured
- `condor_submit_bid` command must be available
- Write permissions in the working directory (for jobs/ folder)

## File Structure

```
plugins/MPI-cluster/
├── plugin.json              # Plugin configuration
├── README.md               # This file
└── skills/
    └── job-submission.md   # Skill definition
```

## Notes

1. **Bid values** affect job priority and cost. Higher bids get higher priority but cost more.
2. **GPU types** are normalized to uppercase (a100 → A100).
3. **Interactive jobs** use the `-i` flag with condor_submit_bid.
4. **Batch jobs** automatically pass the number of GPUs as an argument to the executable.

## Advanced Features

The underlying condor_job.sh script supports additional features:
- Restart threshold (restart job if running price exceeds threshold)
- Kill threshold (kill job if running price exceeds threshold)
- Infinite run mode (keep running executable until non-zero return)
- Custom log locations

These can be added to the skill if needed.

## Support

For issues or feature requests, please refer to the research-os repository documentation.
