import logging
import os

from github import Auth, Github, InputGitAuthor
from github.PullRequest import PullRequest


class GH:
    def __init__(self, repo) -> None:
        self.gh = Github(auth=Auth.Token(os.environ["GH_TOKEN"]))
        self.repo = self.gh.get_user().get_repo(repo)
        self.logger = logging.getLogger(__name__)

        self.branches = self.repo.get_git_refs()
        self.milestones = self.repo.get_milestones()
        self.open_pulls = self.repo.get_pulls(state="open")
        self.projects = self.repo.get_contents("projects")

        self.author = InputGitAuthor(
            "github-actions[bot]", "github-actions[bot]@users.noreply.github.com"
        )
        self.committer = InputGitAuthor(
            "ngi-nix-bot", "168762487+ngi-nix-bot@users.noreply.github.com"
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_branch(self, branch_name):
        base_branch = self.repo.get_branch("main")
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha
        )
        self.logger.info(f"Branch {branch_name} created.")

    def create_pr(self, title, head_branch, body=""):
        pr = self.repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base="main",
        )
        self.logger.info(f"PR created for {title}: {pr.html_url}")
        return pr

    def add_project(self, name, filename, message="", branch=""):
        msg = f"Init {name}" if message == "" else message
        branch_name = f"projects/{name}" if branch == "" else branch
        file_contents = open(filename).read()
        self.repo.create_file(
            f"projects/{name}",
            msg,
            file_contents,
            branch=branch_name,
            committer=self.committer,
            author=self.author,
        )

    def create_milestone(
        self, title, pull_requests: list[PullRequest] = [], desctiption=""
    ):
        milestone = self.repo.create_milestone(title, description=desctiption)
        # TODO: can this be improved? perhaps an an issue is directly created?
        for pr in pull_requests:
            issue = self.repo.get_issue(pr.number)
            issue.edit(milestone=milestone)
        self.logger.info(f"Milestone created for {title}: {milestone.url}")

    def exists(self, collection, attribute, value):
        for item in collection:
            if getattr(item, attribute) == value:
                return True
        return False

    def project_exists(self, name):
        return self.exists(self.projects, "path", f"projects/{name}")

    def branch_exists(self, name):
        return self.exists(self.branches, "ref", f"refs/heads/{name}")

    def pr_exists(self, title):
        return self.exists(self.open_pulls, "title", title)

    def milestone_exists(self, name):
        return self.exists(self.milestones, "title", name)

    def close(self):
        self.gh.close()
