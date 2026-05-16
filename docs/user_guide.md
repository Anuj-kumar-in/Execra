# Execra User Guide

## What is Execra?

Execra is an AI assistant that watches your screen or camera feed and helps you complete tasks step by step in real time. 

Instead of searching for tutorials or debugging mistakes later, Execra tries to guide you while you work.

It can help with:
- Coding tasks
- Software navigation
- Form filling 
- Real world tasks using a webcam
- Error prevention and guidance

Execra works in different modes:
- Passive Mode -> Automatic guidance
- Active Mode -> Ask questions manually
- Mixed Mode -> Both together

## System Requirements

Before installing Execra, make sure your system meets these requirements

### Windows
- Windows 10 or newer 
- Python 3.10 or newer
- Node.js 18 or newer
- Webcam (optional but recommended)
- Internet connection

### Linux
- Ubuntu 22.04 or newer
- Python 3.10 or newer
- Node.js 18 or newer
- Webcam (optional but recommended)
- Internet connection

### Additional Tools
- FFmpeg installed

## Windows Installation

### Step 1: Install Python

Download and install python from :[Python](https://www.python.org/downloads/)

Make sure "Add Python to PATH" is checked during installation.

### Step 2: Install Node.js

Download and install Node.js from :[Node.js](https://nodejs.org//)

### Step 3: Clone  This Git Repo

Open command Prompt and run:

```bash 
git clone https://github.com/sahoo-tech/execra.git
cd Execra
```
### Step 4: Create Virtual Enviornment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Install Frontend Package

```bash
cd frontend
npm install
cd ..
```

### Step 7: Configure Enviornment Variable

```bash
copy .env.example .env
```

### Step 8: Download AI Models

```bash
python scripts/download_models.py
```

### Step 9: Start Execra

```bash
    python main.py
```
## Linux Installation

### Step 1: Clone  This Git Repo

Open command Prompt and run:

```bash 
git clone https://github.com/sahoo-tech/execra.git
cd Execra
```
### Step 2: Create Virtual Enviornment

```bash
python3 -m venv .venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Frontend Package

```bash
cd frontend
npm install
cd ..
```

### Step 5: Configure Environment Variable

```bash
cp .env.example .env
```

### Step 6: Download AI Models

```bash
python scripts/download_models.py
```

### Step 7: Start Execra

```bash
    python main.py
```
## Starting Execra

After launching Execra:

1. Choose a working domain:
    - Digital Domain -> Coding and software tasks
    - Physical Domain -> Camera based real-world tasks

2. Select a mode :
    - Passive Mode -> Automatic guidance
    - Active Mode -> Ask questions manually
    - Mixed Mode -> Both together

3. Allow screen  or  camera permissions if prompted.


## Understanding the overlay UI

### Main Overlay Panel

> Screenshot placeholder

The overlay panel displays:
- Current task guidance
- Warnings and alerts
- suggested next steps
- Confidence score

### Confidence Indicator

> Screenshot placeholder

This shows how confident Execra is about it's suggestion.

### Mode Indicator

> Screenshot placeholder

Shows whether Execra is running in:
- Passive Mode
- Active Mode
- Mixed Mode


## Using Active Mode

In Active Mode, you can ask questions directly while working.

Example questions:
- "Why is this code failing?"
- "what should i do next?"
- "how do i fix this error?"

Execra remembers your current context, so you do not need to repeat everything.

## Undoing an Action

Execra keeps tracks of recent actions using it's action logging system.

if an undo feature is available in your current workflow, use the undo option provided in the overlay or application controls.

## Privacy Mode 

Privacy Mode helps limit sensitive information exposure while using Execra.

when enabled:
- Certain screen or camera information may be hidden or restricted
- sensitive tasks can be performed more safely

Check the application settings to enable Privacy Mode.

## FAQ

### Is my screen data sent to the cloud?

Execra may use AI services depending on your configuration and selected models.

Review the '.env' configuration and project settings to understand which external services are enabled before using sensitive data.
