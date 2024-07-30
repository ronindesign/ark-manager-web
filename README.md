# ark-manager-web
Web interface for ARK Server Tools (by FezVrasta)

## (Optional) Configure (.env)
Copy sample environment file
```bash
cp .env.example .env
```
Edit the .env file with your settings
```bash
vim .env
```

## Deploy - Docker (Build)
docker compose build

## Deploy - Docker (Attended)
docker compose up

## Deploy - Docker (Unattended/background)
docker compose up -d

## Develop - Flask (venv)
**Requirements:**
- Python 3.x
- Python Virtual Environment

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

Set the environment variables
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

Run the app
```bash
flask run
```

## Develop - Vue
Requirements:
- Node.js