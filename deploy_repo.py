"""
DocuMorph GitHub Repository Creation & Deployment Script
Creates the remote repository, sets topics & description, pushes code, and configures GitHub Pages.
"""

import subprocess
import urllib.request
import urllib.error
import json
import sys
import os

def get_git_token():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate('url=https://github.com\n')
    for line in out.splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1].strip()
    return None

def api_request(url, method='GET', data=None, token=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'DocuMorph-Deployer'
    }
    payload = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        return {'error': e.code, 'message': err_body}

def main():
    token = get_git_token()
    if not token:
        print("Error: Could not retrieve GitHub token from git credentials.")
        sys.exit(1)

    repo_name = "documorph-converter"
    username = "preyal2"
    
    print(f"1. Checking if repository '{username}/{repo_name}' exists...")
    repo_info = api_request(f"https://api.github.com/repos/{username}/{repo_name}", token=token)
    
    if 'error' in repo_info and repo_info['error'] == 404:
        print(f"Creating repository '{repo_name}' on GitHub...")
        create_payload = {
            "name": repo_name,
            "description": "🚀 High-performance bidirectional Word (.docx) ⇄ PDF document converter and microservice with multi-tier fallback engines, glassmorphic UI, and 100% privacy-first processing.",
            "homepage": f"https://{username}.github.io/{repo_name}/",
            "private": False,
            "has_issues": True,
            "has_wiki": False,
            "auto_init": False
        }
        res = api_request("https://api.github.com/user/repos", method='POST', data=create_payload, token=token)
        if 'error' in res:
            print("Failed to create repository:", res['message'])
            sys.exit(1)
        print("Repository created successfully!")
    else:
        print("Repository already exists. Updating metadata...")
        update_payload = {
            "description": "🚀 High-performance bidirectional Word (.docx) ⇄ PDF document converter and microservice with multi-tier fallback engines, glassmorphic UI, and 100% privacy-first processing.",
            "homepage": f"https://{username}.github.io/{repo_name}/"
        }
        api_request(f"https://api.github.com/repos/{username}/{repo_name}", method='PATCH', data=update_payload, token=token)

    # Set Topics
    print("Setting repository topics...")
    topics_payload = {
        "names": [
            "word-to-pdf",
            "pdf-to-word",
            "docx-converter",
            "pdf-converter",
            "fastapi",
            "document-processing",
            "python",
            "glassmorphism",
            "privacy-first"
        ]
    }
    api_request(f"https://api.github.com/repos/{username}/{repo_name}/topics", method='PUT', data=topics_payload, token=token)

    # Git Operations
    print("2. Initializing local git repository and staging files...")
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.name", "Preyal"], check=True)
    subprocess.run(["git", "config", "user.email", "deepmodipre@gmail.com"], check=True)
    subprocess.run(["git", "checkout", "-B", "main"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    
    commit_res = subprocess.run(["git", "commit", "-m", "feat: Initial release of DocuMorph Word ⇄ PDF Converter with full documentation and web UI"])
    
    # Configure Remote with token in URL for frictionless authenticated push
    authenticated_remote = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    public_remote = f"https://github.com/{username}/{repo_name}.git"

    subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", authenticated_remote], check=True)

    print(f"3. Pushing codebase to GitHub (main branch)...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], capture_output=True, text=True)
    if push_res.returncode != 0:
        print("Git push error:", push_res.stderr)
        sys.exit(1)
    print("Code pushed successfully!")

    # Reset remote URL to clean public HTTPS URL (remove token from config)
    subprocess.run(["git", "remote", "set-url", "origin", public_remote], check=True)

    # Enable GitHub Pages via Actions workflow
    print("4. Configuring GitHub Pages deployment...")
    pages_payload = {
        "build_type": "workflow"
    }
    pages_res = api_request(f"https://api.github.com/repos/{username}/{repo_name}/pages", method='POST', data=pages_payload, token=token)
    if 'error' in pages_res and pages_res['error'] != 409: # 409 means already enabled
        print("Pages configuration response:", pages_res.get('message'))
    else:
        print("GitHub Pages configured to deploy via GitHub Actions!")

    print("=" * 60)
    print(f"🎉 SUCCESS! Repository is live at:")
    print(f"🔗 https://github.com/{username}/{repo_name}")
    print(f"🌐 GitHub Pages: https://{username}.github.io/{repo_name}/")
    print("=" * 60)

if __name__ == '__main__':
    main()
