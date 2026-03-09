import os
import json
import requests
from pathlib import Path

# Load token from .env.example if present, otherwise expect GITHUB_TOKEN env var
env_path = Path(__file__).parent / '.env.example'
token = None
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('GITHUB_TOKEN='):
                token = line.split('=', 1)[1]
                break
if not token:
    token = os.getenv('GITHUB_TOKEN')

if not token:
    raise RuntimeError('GitHub token not found. Set GITHUB_TOKEN in environment or .env.example')

repo_owner = 'Orcadebug'
repo_name = 'Agent_orch'
new_description = 'Visual PR Activity Tracker – credits: code‑graph‑rag, graphrag‑workbench'

url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json'
}
payload = {'description': new_description}

response = requests.patch(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    print('Repository description updated successfully.')
else:
    print(f'Failed to update description: {response.status_code}\n{response.text}')
