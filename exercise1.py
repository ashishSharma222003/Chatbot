import requests
from github import Github
from xml.etree import ElementTree as ET


def authenticate_github(client_id, client_secret):
    g = Github(client_id, client_secret)
    return g


def get_repository_list(github_instance):
    repositories = github_instance.get_user().get_repos()
    return repositories


def get_pom_xml_dependencies(repo):
    url = f"https://raw.githubusercontent.com/{repo.full_name}/master/pom.xml"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    dependencies = []
    for dependency in root.findall('.//{http://maven.apache.org/POM/4.0.0}dependency'):
        group_id = dependency.find('{http://maven.apache.org/POM/4.0.0}groupId').text
        artifact_id = dependency.find('{http://maven.apache.org/POM/4.0.0}artifactId').text
        version = dependency.find('{http://maven.apache.org/POM/4.0.0}version').text
        dependencies.append(f"{group_id}: Version {version}")

    return dependencies


# Replace with your own client_id and client_secret
client_id = 'your_client_id'
client_secret = 'your_client_secret'
github = authenticate_github(client_id, client_secret)

repos = get_repository_list(github)

for repo in repos:
    if repo.name == "shopizer":
        dependencies = get_pom_xml_dependencies(repo)
        print(f"Dependencies for repository '{repo.name}':")
        for dependency in dependencies:
            print(dependency)