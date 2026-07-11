#!/usr/bin/env python3
import os
import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
    return result.returncode

def main():
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in repo_name:
        repo_name = repo_name.split("/")[-1]
    
    if not repo_name:
        repo_name = os.path.basename(os.getcwd())

    github_token = os.environ.get("GITHUB_TOKEN")
    gitlab_token = os.environ.get("GITLAB_TOKEN")
    codeberg_token = os.environ.get("CODEBERG_TOKEN")

    failures = 0

    if github_token:
        url = f"https://oauth2:{github_token}@github.com/portugalfuturista/{repo_name}.git"
        print("Pushing to GitHub...")
        if run_cmd(f"git push --mirror {url}") != 0:
            failures += 1

    if gitlab_token:
        url = f"https://oauth2:{gitlab_token}@gitlab.com/portugalfuturista/{repo_name}.git"
        print("Pushing to GitLab...")
        if run_cmd(f"git push --mirror {url}") != 0:
            failures += 1

    if codeberg_token:
        url = f"https://{codeberg_token}@codeberg.org/portugalfuturista/{repo_name}.git"
        print("Pushing to Codeberg...")
        if run_cmd(f"git push --mirror {url}") != 0:
            failures += 1

    if failures > 0:
        print(f"Completed with {failures} failures.")
        sys.exit(1)
    else:
        print("Mirroring completed successfully.")

if __name__ == "__main__":
    main()
