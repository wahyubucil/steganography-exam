# Learn Steganography for Exam Purpose

> Used Method: Binary Options

## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the App](#running-the-app)

## Prerequisites

- Python 3 (>= 3.9.0)
- Node.js (>= 14.15.0)
- Yarn (>= 1.22.5)

## Installation

1. Create Virtual Enviroment

```bash
python3 -m venv venv
```

2. Activate the environment

```bash
source venv/bin/activate
```

3. Install packages

```bash
pip3 install -r requirements.txt
```

## Running the App

- Start the app without development features

```bash
FLASK_APP=application.py flask run
```

- Development Mode

```bash
FLASK_APP=application.py FLASK_ENV=development flask run
```
