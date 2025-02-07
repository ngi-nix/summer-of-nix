import logging
import os
import textwrap
from dataclasses import dataclass
from typing import Any, Callable

from githubkit import GitHub, TokenAuthStrategy
from githubkit.exception import RequestFailed
from githubkit.utils import UNSET
from githubkit.versions import RestVersionSwitcher
from githubkit.versions.v2022_11_28.models import (
    Issue,
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

    def get_or_create_issue(self, title, body="") -> Issue:
        issue = self.get_issue(title)

        if issue is not None:
            self.logger.info(f"{title} already tracked with an issue.")
            return issue

        issue = self.api.issues.create(
            self.owner, self.repo, title=title, body=body
        ).parsed_data

        self.add_label(issue.number, ["automated"])

        return issue

    def get_sub_issues(self, issue_number):
        response = self.api.issues.list_sub_issues(
            self.owner, self.repo, issue_number
        ).parsed_data
        return {issue.id: issue for issue in response}

    def get_sub_issue_summary(self, issue: Issue):
        if (
            hasattr(issue, "sub_issues_summary")
            and issue.sub_issues_summary is not UNSET
        ):
            return issue.sub_issues_summary
        return None

    def link_sub_issue(self, issue: Issue, sub_issue: Issue):
        """Add sub-issue to a parent issue"""

        def msg(i: Issue):
            return f"'{i.title} (#{i.number})'"

        sub_issues = self.get_sub_issues(issue.number)
        if sub_issue.id in sub_issues:
            self.logger.info(
                f"Sub-issue '{msg(sub_issue)}' is already linked to parent '{msg(issue)}'."
            )
            return

        try:
            self.api.issues.add_sub_issue(
                self.owner,
                self.repo,
                issue_number=issue.number,
                sub_issue_id=sub_issue.id,
            ).parsed_data
        except RequestFailed as e:
            self.logger.warning(
                textwrap.dedent(
                    f"""
                        Failed to link sub-issue {msg(sub_issue)} to parent {msg(issue)}.
                        {e}
                        """
                )
            )

    def sub_issue_summary(self, issue_number):
        return self.api.issues.get(
            self.owner, self.repo, issue_number=issue_number
        ).parsed_data.sub_issues_summary

    def add_label(self, issue_number: int, labels: list[str]):
        return self.api.issues.add_labels(
            self.owner, self.repo, issue_number, data=labels
        )

    def getter(self, issues: dict[str, Any], title) -> Any | None:
        if title in issues:
            return issues[title]
        return None

    def get_issue(self, title):
        return self.getter(self.issues, title)
