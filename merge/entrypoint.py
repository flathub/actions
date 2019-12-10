#!/usr/bin/env python3

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

import github
import pygit2
import requests
import yaml


def set_protected_branch(token, owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection"
    json = {
        "required_status_checks": None,
        "enforce_admins": None,
        "required_pull_request_reviews": None,
        "restrictions": None,
    }
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.loki-preview+json",
    }

    r = requests.put(url, json=json, headers=headers)

    return r.status_code


def detect_appid(dirname):
    files = []
    ret = None

    for ext in ("yml", "yaml", "json"):
        files.extend(glob.glob(f"{dirname}/*.{ext}"))

    for filename in files:
        if os.path.isfile(filename):
            ext = filename.split('.')[-1]

            with open(filename) as f:
                if ext in ("yml", "yaml"):
                    manifest = yaml.safe_load(f)
                else:
                    result = subprocess.run(['flatpak-builder', '--show-manifest', filename], stdout=subprocess.PIPE)
                    if result.returncode == 0:
                        manifest = json.loads(result.stdout.decode('utf-8'))
                    else:
                        break

            if manifest:
                if "app-id" in manifest:
                    ret = (os.path.basename(filename), manifest["app-id"])
                elif 'id' in manifest:
                    ret = (os.path.basename(filename), manifest["id"])

    return ret


def main():
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("GITHUB_TOKEN environment variable is not set")
        sys.exit(1)

    github_event_path = os.environ.get('GITHUB_EVENT_PATH')
    with open(github_event_path) as f:
        github_event = json.load(f)

    if github_event['action'] != "created":
        print("this is not a new comment event")
        sys.exit(0)

    if 'pull_request' not in github_event['issue']:
        print("the issue is not a pull request")
        sys.exit(0)

    command_re = re.search("^/merge.*", github_event['comment']['body'], re.M)
    if not command_re:
        print("comment doesn't contain '/merge' command")
        sys.exit(0)
    else:
        command = command_re.group()

    gh = github.Github(github_token)
    org = gh.get_organization("flathub")

    admins = org.get_team_by_slug('admins')
    reviewers = org.get_team_by_slug('reviewers')
    comment_author = gh.get_user(github_event['comment']['user']['login'])

    if not admins.has_in_members(comment_author) and not reviewers.has_in_members(comment_author):
        print(f"{comment_author} is not a reviewer")
        sys.exit(1)

    flathub = org.get_repo("flathub")
    pr_id = int(github_event['issue']['number'])
    pr = flathub.get_pull(pr_id)
    pr_author = pr.user.login
    branch = pr.head.label.split(":")[1]
    fork_url = pr.head.repo.clone_url

    tmpdir = tempfile.TemporaryDirectory()
    print(f"cloning {fork_url} (branch: {branch})")
    clone = pygit2.clone_repository(fork_url, tmpdir.name, checkout_branch=branch)
    clone.update_submodules(init=True)

    manifest_file, appid = detect_appid(tmpdir.name)
    print(f"detected {appid} as appid from {manifest_file}")

    if os.path.splitext(manifest_file)[0] != appid:
        print("manifest filename does not match appid")
        os.exit(1)

    print("creating new repo on flathub")
    repo = org.create_repo(appid)

    print("adding flathub remote")
    clone.remotes.create("flathub", f"https://x-access-token:{github_token}@github.com/flathub/{appid}")
    
    try: 
        remote_branch = command.split()[0].split(":")[1]
    except IndexError:
        remote_branch = "master"
    
    print("pushing changes to the new repo on flathub\n")
    git_push = f"cd {tmpdir.name} && git push flathub {branch}:{remote_branch}"
    subprocess.run(git_push, shell=True, check=True)
    repo.remove_from_collaborators('flathubbot')

    print("\nsetting protected branches")
    set_protected_branch(github_token, "flathub", appid, "master")
    set_protected_branch(github_token, "flathub", appid, "beta")
    set_protected_branch(github_token, "flathub", appid, "branch/*")

    print(f"adding {pr_author} to collaborators")
    repo.add_to_collaborators(pr_author, permission="push")

    collaborators = {user.replace('@', '') for user in command.split()[1:]}
    for user in collaborators:
        print(f"adding {user} to collaborators")
        repo.add_to_collaborators(user, permission="push")

    close_comment = (
        f"A repository for this has been created: {repo.html_url}", "\n",
        "You will receive an invitation to be a collaborator which will grant you write access to the repository above. The invite can be also viewed [here](f{repo.html_url}/invitations).", "\n",
        "If you have never maintained an application before, common questions are answered in [the app maintenance guide](https://github.com/flathub/flathub/wiki/App-Maintenance).", "\n",
        "Thanks!"
    )

    print("closing the pull request")
    pr.create_issue_comment("\n".join(close_comment))
    pr.edit(state="closed")


if __name__ == "__main__":
    main()
