import os
import pathlib
import re
import sys
import requests
from requests.auth import HTTPBasicAuth
from git import Repo


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def args_to_string(args) -> str:
    result = ''
    for arg in args:
        if ' ' in arg:
            result += '"' + arg + '" '
        else:
            result += arg + ' '
    return result


def fetch_issue(issue_key):
    token_file = open(str(pathlib.Path.home()) + '/.jiratoken')
    token = token_file.readline()
    token_file.close()
    response = requests.get('https://freenet-group.atlassian.net/rest/api/3/issue/' + issue_key,
                            auth=HTTPBasicAuth(*token.split(':', maxsplit=2)))
    if response.status_code != 200:
        eprint('Failed to fetch issue {}: {} {}'.format(issue_key, response.status_code, response.text))
        exit(1)
    issue = response.json()
    return issue


def create_branch(args: list) -> bool:
    if len(args) != 1 or re.fullmatch('^(\\w+-)?\\d+$', args[0]) is None:
        eprint('Usage: git create_branch $issue')
        eprint('issue can be the specific issue key (e.g. SPOC-123567) or'
               ' just a number (e.g. 123) which is then interpreted as a GRAON issue')
        exit(1)

    if re.fullmatch('^\\d+$', args[0]) is not None:
        issue_key = 'GRAON-' + args[0]
    else:
        issue_key = args[0]

    summary: str = fetch_issue(issue_key)['fields']['summary']
    summary = summary.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    summary = re.sub('[^_\\w]+', '-', summary)
    while summary[0] == '-':
        summary = summary[1:]
    while summary[-1] == '-':
        summary = summary[0:-1]

    print('switch -c feature/' + issue_key + '-' + summary)
    return True


def commit(args) -> bool:
    # Don't generate message when message is already specified, or if we are amending
    if '--am' in args or '--amend' in args or '-F' in args or '-m' in args:
        return False

    # Fetch issue by branch name
    working_directory = os.getcwd()
    repo = Repo(working_directory, search_parent_directories=True)
    if repo.head.is_detached:
        return False

    branch = repo.active_branch.name
    issue_keys = re.findall('\\b([A-Z]+-\\d+\\b)', branch)
    if len(issue_keys) != 1:
        return False

    # Fetch issue via api
    issue = fetch_issue(issue_keys[0])
    if not issue:
        return False

    # Translate issue key and summary to commit message
    commit_message = issue['key'] + ' ' + issue['fields']['summary']
    print('commit -m "' + commit_message)
    print()
    print()
    print('" --edit ' + args_to_string(args))
    return True


overrides = dict()
overrides['create-branch'] = create_branch
overrides['commit'] = commit

command = sys.argv[1]
if command in overrides:
    # Call override function
    if overrides[command](sys.argv[2:]):
        exit(0)

# Call original function
print(args_to_string(sys.argv[1:]))
