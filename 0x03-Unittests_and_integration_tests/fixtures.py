# fixtures.py
org_payload = {
    "login": "google",
    "id": 1342004,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {
        "id": 123,
        "name": "repo1",
        "license": {"key": "apache-2.0"}
    },
    {
        "id": 456,
        "name": "repo2",
        "license": {"key": "mit"}
    }
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]