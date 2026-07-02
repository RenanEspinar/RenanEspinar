import os
import requests

USERNAME = "RenanEspinar"
README_PATH = "README.md"

EXCLUDED_REPOS = {
    "RenanEspinar",
}

TOPICS_PRIORITY = [
    "control",
    "robotics",
    "biomedical",
    "matlab",
    "python",
    "arduino",
    "iot",
    "alexa",
    "home-assistant",
    "3d-printing",
]

def get_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos"
    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": 100,
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    repos = response.json()

    repos = [
        repo for repo in repos
        if not repo["fork"]
        and repo["name"] not in EXCLUDED_REPOS
    ]

    return repos


def repo_card(repo):
    name = repo["name"]
    description = repo["description"] or "Engineering project repository."
    language = repo["language"] or "Engineering"
    url = repo["html_url"]
    stars = repo["stargazers_count"]
    updated = repo["updated_at"][:10]

    return f"""
<td width="50%" valign="top">

### [{name}]({url})

{description}

**Main stack:** `{language}`  
**Stars:** `{stars}`  
**Last update:** `{updated}`

</td>
"""


def build_projects_section(repos):
    repos = repos[:8]

    rows = []
    for i in range(0, len(repos), 2):
        left = repo_card(repos[i])
        right = repo_card(repos[i + 1]) if i + 1 < len(repos) else "<td width='50%'></td>"

        rows.append(f"""
<tr>
{left}
{right}
</tr>
""")

    return "<table>\n" + "\n".join(rows) + "\n</table>"


def update_readme(projects_markdown):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- PROJECTS:START -->"
    end = "<!-- PROJECTS:END -->"

    before = content.split(start)[0]
    after = content.split(end)[1]

    new_content = before + start + "\n" + projects_markdown + "\n" + end + after

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    repos = get_repositories()
    projects = build_projects_section(repos)
    update_readme(projects)
