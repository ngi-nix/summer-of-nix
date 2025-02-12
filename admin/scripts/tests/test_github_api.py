import json
from pathlib import Path
from typing import Any, Callable, Type, Union

import httpx
import pytest
from common.ghkit import GitClient
from githubkit import GitHub
from githubkit.response import Response
from githubkit.typing import UnsetType, URLTypes
from githubkit.utils import UNSET
from githubkit.versions.v2022_11_28.models import Issue


def load_fake_response(filename: str) -> Any:
    return json.loads((Path(__file__).parent / filename).read_text())


fake_issues_response = load_fake_response("fake_responses/issues.json")


def mock_items(api_method: Callable, key: str, *args, **kwargs) -> Any:
    response: list[Any] = api_method("owner", "repo", *args, **kwargs).parsed_data
    return {getattr(item, key): item for item in response}


def mock_issues(self) -> dict[str, Issue]:
    return mock_items(self.api.issues.list_for_repo, "title")


def unique_issues(issues: dict[str, Issue], title: str):
    """Checks that the issue does not exist multiple times"""
    issue_number = []

    for i in issues.values():
        if i.title == title:
            issue_number.append(i.number)

    if len(issue_number) > 1:
        return False
    return True


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
        m.setenv("GH_TOKEN", "xxxx")

        mock_methods = {
            "get_issues": mock_issues,
        }

        for method_name, mock_method in mock_methods.items():
            m.setattr(GitClient, method_name, mock_method)

        gh = GitClient("owner", "repo")

        issues: dict[str, Issue] = gh.get_issues()
        issue = gh.get_issue("#Seppo!")

        assert issue is not None

        # Only one issue exists for the project
        assert unique_issues(issues, issue.title)

        # The original issue is picked and not the duplicate
        assert issue.number == 575
