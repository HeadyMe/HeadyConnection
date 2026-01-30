# HeadySystems Inc. 
Official "Heady" Ecosystem Repo

## Overview

This repository contains the HeadyConnection project, which includes:

- **execute_build.py**: A utility script to clone GitHub repositories, extract packaged archives, and run build scripts
- **heady_demo_kit**: Demo project containing stub implementations for various Heady modules
- **HeadySystems**: Fleet and project configurations

## Components

### Build Utility (`execute_build.py`)

A Python script that automates the setup and build process for Heady projects.

**Usage:**
```bash
python3 execute_build.py \
    --repo-url https://github.com/HeadyConnection/Heady.git \
    --zip-file /path/to/HeadySystems_package_v1_0_0.zip \
    --build-script Heady_Golden_Master_Builder_v_1_0_0.py \
    --work-dir /tmp/heady_build \
    --output-dir /tmp/heady_package
```

### Demo Kit

The `heady_demo_kit` directory contains demonstration modules including:
- heady_society
- heady_finance  
- heady_hardware
- heady_security
- heady_foundation
- And more...

## Requirements

- Python 3.x
- Git (for clone operations)

## License

See LICENSE file for details.
