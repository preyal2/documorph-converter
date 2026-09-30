import subprocess
import urllib.request
import json
import sys

def get_token():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate('url=https://github.com\n')
    for line in out.splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1].strip()
    return None

token = get_token()
if not token:
    print("No token found")
    sys.exit(1)

# Update repo description
url = "https://api.github.com/repos/preyal2/documorph-converter"
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'DocuMorph-Deployer'
}

data = {
    "description": "🚀 High-performance bidirectional Word (.docx) ⇄ PDF document converter with multi-tier fallback engines, glassmorphic UI, and 100% privacy-first local processing. Developed by Preyal Modi.",
    "homepage": "https://preyal2.github.io/documorph-converter/"
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='PATCH')
try:
    with urllib.request.urlopen(req) as resp:
        print("GitHub repository description updated successfully!")
except Exception as e:
    print("API Error:", e)

# Commit and Push git changes
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat: Add developer attribution 'Developed by Preyal Modi' and enhance project description"], check=True)
push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if push_res.returncode == 0:
    print("Git push to GitHub main succeeded!")
else:
    print("Git push output:", push_res.stderr or push_res.stdout)
