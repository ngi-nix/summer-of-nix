import logging
import os
import re
import urllib.parse
from base64 import b64encode
from dataclasses import dataclass
from typing import Any, Callable, Optional

from githubkit import GitHub, TokenAuthStrategy
from githubkit.utils import UNSET
from githubkit.versions import RestVersionSwitcher
from githubkit.versions.v2022_11_28.models import (
    BranchWithProtection,
    ContentDirectoryItems,
    ContentFile,
    Issue,
    PullRequestSimple,
    ShortBranch,
)
from githubkit.versions.v2022_11_28.types import (
    ReposOwnerRepoContentsPathPutBodyPropCommitterType,
)


@dataclass
class GitClient:
    def __init__(self, owner, repo) -> None:
        self.logger = logging.getLogger(__name__)

        self.gh: GitHub[TokenAuthStrategy] = GitHub(os.environ["GH_TOKEN"])
        self.api: RestVersionSwitcher = self.gh.rest

        self.owner: str = owner
        self.repo: str = repo

        self.committer = ReposOwnerRepoContentsPathPutBodyPropCommitterType(
            name="ngi-nix-bot",
            email="168762487+ngi-nix-bot@users.noreply.github.com",
        )
        self.author = self.committer

        self.issues = self.get_issues()
        self.branches = self.get_branches()
        self.pulls = self.get_pulls()
        self.projects = self.get_projects()
        self.base_branch = self.get_branch("main")

    def issue_is_pr(self, issue: Issue):
        """Determines if an issue item is a PR"""
        return hasattr(issue, "pull_request") and issue.pull_request is not UNSET

    # https://yanyongyu.github.io/githubkit/usage/rest-api/#rest-api-pagination
    def get_paginated_items(self, fetch_function: Callable, key: str, *args, **kwargs):
        """Fetches all items from a paginated API and returns them as a list."""
        paginator = self.gh.paginate(
            fetch_function, owner=self.owner, repo=self.repo, *args, **kwargs
        )

        items = {}
        for item in paginator:
            if fetch_function.__name__ == "list_for_repo":
                if self.issue_is_pr(item):
                    continue
            items[getattr(item, key)] = item

        return items

    def get_issues(self) -> dict[str, Issue]:
        return self.get_paginated_items(
            self.api.issues.list_for_repo, "title", state="all"
        )

    def get_branches(self) -> dict[str, ShortBranch]:
        return self.get_paginated_items(self.gh.rest.repos.list_branches, "name")

    def get_pulls(self) -> dict[str, PullRequestSimple]:
        return self.get_paginated_items(self.api.pulls.list, "title")

    def get_projects(self):
        return self.get_path_contents("projects")

    def get_path_contents(self, path):
        return self.api.repos.get_content(self.owner, self.repo, path=path).parsed_data

    def get_branch(self, branch) -> BranchWithProtection:
        return self.api.repos.get_branch(
            self.owner, self.repo, branch=branch
        ).parsed_data

    def create_branch(self, branch_name):
        branch = self.clean_branch_name(branch_name)
        ref = self.api.git.create_ref(
            self.owner,
            self.repo,
            ref=f"refs/heads/{branch}",
            sha=self.base_branch.commit.sha,
        ).parsed_data
        self.logger.info(f"Branch {branch} created.")
        return ref

    def delete_branch(self, branch_name):
        branch = self.clean_branch_name(branch_name)
        self.api.git.delete_ref(self.owner, self.repo, ref=f"heads/{branch}")
        self.logger.debug(f"Deleted branch: {branch}")

    def create_pr(self, title, head_branch, body=""):
        try:
            response = self.api.pulls.create(
                self.owner,
                self.repo,
                title=title,
                body=body,
                head=self.clean_branch_name(head_branch),
                base="main",
            )
            self.logger.info(f"Created PR for {title}: {response.parsed_data.html_url}")
            self.add_label(response.parsed_data.number, ["automated"])
        except Exception as e:
            self.logger.debug(e)

    def add_project(self, name, template_dir, message="", branch=""):
        message = f"Init {name}" if message == "" else message
        branch_name = f"projects/{name}" if branch == "" else branch

        if not os.path.isdir(template_dir):
            self.logger.debug(
                f"The provided template for {name} is not a directory: '{template_dir}'"
            )
            return

        template_files = []

        # Recursively get the file contents to commit
        for root, _, files in os.walk(template_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, template_dir)
                path = f"projects/{name}/{relative_path}"
                path = urllib.parse.quote(path)

                if self.get_file_sha(path) is not None:
                    self.logger.debug(f"Template: '{path}' already exists.")
                    continue

                # The GitHub API expects the file contents to be in Base64
                with open(file_path, "r") as f:
                    file_content = f.read().encode("utf-8")
                file_content = b64encode(file_content).decode("utf-8")

                # Append the file change to the list
                template_files.append(
                    {
                        "path": path,
                        "content": file_content,
                        "sha": None,  # No SHA since we're creating new files
                    }
                )

        # Commit all the files
        for change in template_files:
            try:
                self.api.repos.create_or_update_file_contents(
                    owner=self.owner,
                    repo=self.repo,
                    path=change["path"],
                    message=message,
                    content=change["content"],
                    branch=self.clean_branch_name(branch_name),
                    committer=self.committer,
                    author=self.author,
                    sha=change["sha"],
                )
            except Exception as e:
                self.logger.debug(e)

    def create_issue(self, title, body="") -> Issue:
        issue = self.api.issues.create(
            self.owner, self.repo, title=title, body=body
        ).parsed_data

        self.add_label(issue.number, ["automated"])
        return issue

    def get_sub_issues(self, issue_number) -> list[Issue]:
        return self.api.issues.list_sub_issues(
            self.owner, self.repo, issue_number
        ).parsed_data

    def link_sub_issue(self, issue_number, sub_issue_id):
        """Add sub-issue to a parent issue"""
        self.api.issues.add_sub_issue(
            self.owner,
            self.repo,
            issue_number=issue_number,
            sub_issue_id=sub_issue_id,
        ).parsed_data

    def sub_issue_summary(self, issue_number):
        return self.api.issues.get(
            self.owner, self.repo, issue_number=issue_number
        ).parsed_data.sub_issues_summary

    def add_label(self, issue_number: int, labels: list[str]):
        return self.api.issues.add_labels(
            self.owner, self.repo, issue_number, data=labels
        )

    def clean_branch_name(self, name: str) -> str:
        cleaned_name = name.strip().replace(" ", "-").lower()
        cleaned_name = re.sub(r"[^a-z0-9._/-]", "", cleaned_name)
        return cleaned_name

    def exists(self, issues: dict[str, Any], title) -> Any | None:
        if title in issues:
            return issues[title]
        return None

    def project_exists(self, name: str):
        for item in self.projects:
            if isinstance(item, ContentDirectoryItems):
                return item.path == name
            else:
                return name in item
        return False

    def branch_exists(self, name):
        return self.exists(self.branches, self.clean_branch_name(name))

    def pr_exists(self, title: str):
        return self.exists(self.pulls, title)

    def issue_exists(self, title):
        return self.exists(self.issues, title)

    def get_file_sha(self, path: str) -> Optional[str]:
        try:
            response = self.api.repos.get_content(self.owner, self.repo, path)

            # If the file exists and is not a directory, get the file hash
            if response.status_code == 200 and not isinstance(
                response.parsed_data, list
            ):
                return response.parsed_data.sha
        except Exception as e:
            self.logger.debug(e)
        return None
