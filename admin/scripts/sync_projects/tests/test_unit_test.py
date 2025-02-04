import json
from pathlib import Path
from typing import Any, Callable, List, Type, Union

import httpx
import pytest
from githubkit import GitHub
from githubkit.response import Response
from githubkit.typing import UnsetType, URLTypes
from githubkit.utils import UNSET
from githubkit.versions.v2022_11_28.models import Issue, ShortBranch
from pydantic import BaseModel

from ...lib.ghkit import GitClient
from ...lib.utils import load_credentials


class ItemsList(BaseModel):
    items: List[Any]


def load_fake_response(filename: str) -> Any:
    return json.loads((Path(__file__).parent / filename).read_text())


fake_issues_response = load_fake_response("fake_responses/issues.json")
fake_branches_response = load_fake_response("fake_responses/branches.json")
fake_pulls_response = load_fake_response("fake_responses/pulls.json")
fake_branch_main = load_fake_response("fake_responses/main.json")


def mock_items(api_method: Callable, *args, **kwargs) -> Any:
    response = api_method("owner", "repo", *args, **kwargs).parsed_data
    return ItemsList(items=response)


def mock_issues(self) -> ItemsList:
    return mock_items(self.api.issues.list_for_repo)


def mock_branches(self) -> ItemsList:
    return mock_items(self.api.repos.list_branches)


def mock_pulls(self) -> ItemsList:
    return mock_items(self.api.pulls.list)


def mock_projects(self):
    return ""


def remove_prs_from_issues(self):
    pass


def mock_request(
    g: GitHub,
    method: str,
    url: URLTypes,
    *,
    response_model: Union[Type[Any], UnsetType] = UNSET,
    **kwargs: Any,
) -> Response[Any]:
    if method != "GET":
        raise RuntimeError(f"Unexpected request: {method} {url}")

    response_map = {
        "/repos/owner/repo/issues": fake_issues_response,
        "/repos/owner/repo/branches": fake_branches_response,
        "/repos/owner/repo/pulls": fake_pulls_response,
        "/repos/owner/repo/contents/projects": "{}",
        "/repos/owner/repo/branches/main": fake_branch_main,
    }

    if url in response_map:
        return Response(
            httpx.Response(status_code=200, json=response_map[url]),
            Any if response_model is UNSET else response_model,
        )

    raise RuntimeError(f"Unexpected request: {method} {url}")


def test_sync_mock():
    with pytest.MonkeyPatch.context() as m:
        m.setattr(GitHub, "request", mock_request)

        mock_methods = {
            "get_issues": mock_issues,
            "get_branches": mock_branches,
            "get_pulls": mock_pulls,
            "get_projects": mock_projects,
            "remove_prs_from_issues": remove_prs_from_issues,
        }

        for method_name, mock_method in mock_methods.items():
            m.setattr(GitClient, method_name, mock_method)

        load_credentials("./.env")

        gh = GitClient("owner", "repo")

        issues: list[Issue] = gh.get_issues()
        assert isinstance(issues, ItemsList)

        branches: list[ShortBranch] = gh.get_branches()
        assert isinstance(branches, ItemsList)
