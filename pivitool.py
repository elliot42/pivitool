import requests
import yaml
import os

default_pivotal_context = {
    'api_base': 'https://www.pivotaltracker.com/services/v5',
}

default_config_path = os.path.expanduser("~/.pivitool.yml")

def config(path):
    with open(path, 'r') as f:
        config_string_content = f.read()
        return yaml.load(config_string_content)

default_config = config(default_config_path)

def backlog(pivotal_context, config, project_id):
    headers = {
        'X-TrackerToken': config['api_token'],
    }

    params = {
        'filter': 'state:unstarted,started,finished,delivered',
    }

    uri = "".join([
        pivotal_context['api_base'],
        '/projects',
        '/',
        str(project_id),
        '/stories',
        ])

    return requests.get(uri,params=params,headers=headers).json()

def story_pretty(story):
    if story['story_type'] == 'release':
        estimate = ' '
    elif 'estimate' in story:
        estimate = ''.join(["(", str(story['estimate']), ") "])
    else:
        estimate = ''.join(["(", story['story_type'], ") "])

    output = ''.join([estimate, story['name']])
    if story['story_type'] == 'release':
        output = ''.join(["=== ", output, " ==="])
    return output

def backlog_pretty(backlog_items):
    return [story_pretty(story) for story in backlog_items]

class Pivitool:
    def __init__(self, config=default_config, pivotal_context=default_pivotal_context):
        self.config = config
        self.pivotal_context = pivotal_context

    def backlog(self, project_id):
        return backlog(self.pivotal_context, self.config, project_id)

    def backlog_pretty(self, project_id):
        return backlog_pretty(self.backlog(project_id))

    def backlog_pprint(self, project_id):
        print("=== BACKLOG ===")
        for story in self.backlog_pretty(project_id):
            print(story)

