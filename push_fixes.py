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
    print("Error: Could not retrieve GitHub token.")
    sys.exit(1)

# 1. Update GitHub repository description
url = "https://api.github.com/repos/preyal2/documorph-converter"
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'DocuMorph-Deployer'
}

data = {
    "description": "📄 DocuMorph – High-fidelity bidirectional Word (.docx) ⇄ PDF converter with multi-tier layout preservation engines, sleek glassmorphic white UI, zero data leakage, and automated REST API. Developed by Preyal Modi.",
    "homepage": "https://preyal2.github.io/documorph-converter/"
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='PATCH')
try:
    with urllib.request.urlopen(req) as resp:
        print("GitHub repository description updated successfully!")
except Exception as e:
    print("API Error updating description:", e)

# 2. Stage, commit, and push git updates
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "fix: resolve document opening errors with verified Base64 samples and multi-tier fallbacks, update repository description"], check=True)
push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if push_res.returncode == 0:
    print("Git push to GitHub main succeeded!")
else:
    print("Git push output:", push_res.stderr or push_res.stdout)
