import logging
import os
from base64 import b64encode
from dataclasses import dataclass
from typing import Callable, List, Optional, TypeVar

from githubkit import GitHub, TokenAuthStrategy
from githubkit.versions import RestVersionSwitcher
from githubkit.versions.latest.models import (
    Issue,
    PullRequestSimple,
    ShortBranch,
)
from githubkit.versions.v2022_11_28.types import (
    ReposOwnerRepoContentsPathPutBodyPropCommitterType,
)

T = TypeVar("T")


def fetch_paginated_items(fetch_function: Callable, *args, **kwargs) -> List[T]:
    """Fetches all items from a paginated API and returns them as a list."""
    return [item for item in fetch_function(*args, **kwargs)]


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

        # https://yanyongyu.github.io/githubkit/usage/rest-api/#rest-api-pagination
        self.issues: list[Issue] = fetch_paginated_items(
            self.gh.paginate,
            self.api.issues.list_for_repo,
            owner=self.owner,
            repo=self.repo,
        )
        self.branches: list[ShortBranch] = fetch_paginated_items(
            self.gh.paginate,
            self.gh.rest.repos.list_branches,
            owner=self.owner,
            repo=self.repo,
        )
        self.pulls_open: list[PullRequestSimple] = fetch_paginated_items(
            self.gh.paginate,
            self.api.pulls.list,
            owner=self.owner,
            repo=self.repo,
            state="open",
        )

        self.projects = self.api.repos.get_content(
            self.owner, self.repo, path="projects"
        ).parsed_data

    def create_branch(self, branch_name):
        base_branch = self.api.repos.get_branch(
            self.owner, self.repo, branch="main"
        ).parsed_data
        ref = self.api.git.create_ref(
            self.owner,
            self.repo,
            ref=f"refs/heads/{branch_name}",
            sha=base_branch.commit.sha,
        ).parsed_data
        self.logger.info(f"Branch {branch_name} created.")
        return ref

    def delete_branch(self, branch_name):
        self.api.git.delete_ref(self.owner, self.repo, ref=f"heads/{branch_name}")
        self.logger.debug(f"Deleted branch: {branch_name}")

    def create_pr(self, title, head_branch, body=""):
        try:
            response = self.api.pulls.create(
                self.owner,
                self.repo,
                title=title,
                body=body,
                head=head_branch,
                base="main",
            )
            self.logger.info(f"Created PR for {title}: {response.parsed_data.html_url}")
        except Exception as e:
            self.logger.debug(e)

    def update_project(self, name, filename, msg="", branch=""):
        msg = f"Init {name}" if msg == "" else msg
        branch_name = f"projects/{name}" if branch == "" else branch
        path = f"projects/{name}"
        file_sha = self.get_file_sha(path)

        self.add_project(name, filename, message=msg, branch=branch_name, sha=file_sha)

    def add_project(self, name, filename, message="", branch="", sha=None):
        message = f"Init {name}" if message == "" else message
        branch_name = f"projects/{name}" if branch == "" else branch
        path = f"projects/{name}"

        if self.get_file_sha(path) is not None and sha is None:
            self.logger.debug(f"The template for '{name}' already exists in '{path}'")
            return

        # The GitHub API expects the file contents to be in Base64
        file_content = open(filename, "r").read().encode("utf-8")
        file_content = b64encode(file_content).decode("utf-8")

        try:
            self.api.repos.create_or_update_file_contents(
                owner=self.owner,
                repo=self.repo,
                path=path,
                message=message,
                content=file_content,
                branch=branch_name,
                committer=self.committer,
                author=self.author,
                sha=sha,
            )
        except Exception as e:
            self.logger.debug(e)

    def create_issue(self, title, body="") -> Issue:
        return self.api.issues.create(
            self.owner, self.repo, title=title, body=body
        ).parsed_data

    def get_sub_issues(self, issue_number) -> list[Issue]:
        return self.api.issues.list_sub_issues(
            self.owner, self.repo, issue_number
        ).parsed_data

    def add_sub_issue(self, issue_number, sub_issue_number):
        """Add sub-issue to a parent issue"""
        sub_issue: Issue = self.api.issues.get(
            self.owner, self.repo, sub_issue_number
        ).parsed_data

        return self.api.issues.add_sub_issue(
            self.owner, self.repo, issue_number=issue_number, sub_issue_id=sub_issue.id
        )

    def sub_issue_summary(self, issue_number):
        return self.api.issues.get(
            self.owner, self.repo, issue_number=issue_number
        ).parsed_data.sub_issues_summary

    def exists(self, collection, attribute, value: str):
        for item in collection:
            if str(getattr(item, attribute)).lower() == value.lower():
                return True

        return False

    def project_exists(self, name: str):
        return self.exists(self.projects, "path", f"projects/{name}")

    def branch_exists(self, name):
        return self.exists(self.branches, "name", name)

    def pr_exists(self, title: str):
        for item in self.pulls_open:
            item: PullRequestSimple
            if item.title == title:
                return True
        return False

    def issue_exists(self, title):
        return self.exists(self.pulls_open, "title", title)

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
