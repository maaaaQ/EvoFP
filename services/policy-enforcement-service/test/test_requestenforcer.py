import os
import unittest

import jwt
from starlette.requests import Request
from starlette.datastructures import Headers
from src.policies.requestenforcer import RequestEnforcer, Service, EnforceResult

TEST_POLICIES_CONFIG = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_policies.yaml"
)
TEST_JWT_SECRET = "572e6200-1a7a-4f61-9ac1-0f2c8220d8b8"

USER_SERVICE = Service(
    name="user-service",
    entrypoint="http://user-service:5000/",
    inject_token_in_swagger=True,
)

TASKS_SERVICE = Service(
    name="tasks-service",
    entrypoint="http://tasks-service:5000/",
    inject_token_in_swagger=True,
)

COMMENT_SERVICE = Service(
    name="comment-service",
    entrypoint="http://comment-service:5000/",
    inject_token_in_swagger=True,
)


def build_request(
    method: str = "GET",
    server: str = "www.example.com",
    path: str = "/",
    headers: dict = None,
    body: str = None,
) -> Request:
    """
    Build mock-request based on Starlette Request
    """
    if headers is None:
        headers = {}
    request = Request(
        {
            "type": "http",
            "path_params": {"path_name": path[1:]},
            "path": path,
            "headers": Headers(headers).raw,
            "http_version": "1.1",
            "method": method,
            "scheme": "https",
            "client": ("127.0.0.1", 8080),
            "server": (server, 443),
        }
    )
    if body:

        async def request_body():
            return body

        request.body = request_body
    return request


class RequestEnforceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.policy_checker: RequestEnforcer = RequestEnforcer(
            TEST_POLICIES_CONFIG, TEST_JWT_SECRET
        )

    def test_tasks_get_allow(self):
        request = self._prepare_request(1, "GET", "/tasks")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, TASKS_SERVICE.entrypoint.unicode_string())

    def test_tasks_create_allow(self):
        request = self._prepare_request(2, "POST", "/tasks")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, TASKS_SERVICE.entrypoint.unicode_string())

    def test_tasks_delete_denied(self):
        request = self._prepare_request(2, "DELETE", "/tasks")
        result = self.policy_checker.enforce(request)
        self._assert_access_denied(result)

    def test_comments_get_allow(self):
        request = self._prepare_request(1, "GET", "/comments")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, COMMENT_SERVICE.entrypoint.unicode_string())

    def test_comments_create_allow(self):
        request = self._prepare_request(2, "POST", "/comments")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, COMMENT_SERVICE.entrypoint.unicode_string())

    def test_comments_delete_denied(self):
        request = self._prepare_request(2, "DELETE", "/comments")
        result = self.policy_checker.enforce(request)
        self._assert_access_denied(result)

    def test_groups_create_allow(self):
        request = self._prepare_request(1, "POST", "/groups")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, USER_SERVICE.entrypoint.unicode_string())

    def test_groups_get_allow(self):
        request = self._prepare_request(1, "GET", "/groups")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, USER_SERVICE.entrypoint.unicode_string())

    def test_groups_get_denied(self):
        request = self._prepare_request(2, "GET", "/groups")
        result = self.policy_checker.enforce(request)
        self._assert_access_denied(result)

    def test_groups_delete_denied(self):
        request = self._prepare_request(2, "DELETE", "/groups")
        result = self.policy_checker.enforce(request)
        self._assert_access_denied(result)

    def test_users_info_allow(self):
        request = self._prepare_request(2, "GET", "/users/me")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, USER_SERVICE.entrypoint.unicode_string())

    def test_users_delete_denied(self):
        request = self._prepare_request(2, "DELETE", "/users/554")
        result = self.policy_checker.enforce(request)
        self._assert_access_denied(result)

    def test_users_delete_allow(self):
        request = self._prepare_request(1, "DELETE", "/users/15")
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, USER_SERVICE.entrypoint.unicode_string())

    def test_auth_allow(self):
        request = self._prepare_request(1, "POST", "/auth/auth", make_headers=False)
        result = self.policy_checker.enforce(request)
        self._assert_access_allow(result, USER_SERVICE.entrypoint.unicode_string())

    def test_services_list(self):
        expected_services = [USER_SERVICE, TASKS_SERVICE, COMMENT_SERVICE]

        def sort_list(target):
            return sorted(target, key=lambda i: i.name)

        self.assertListEqual(
            sort_list(self.policy_checker.services), sort_list(expected_services)
        )

    def _make_headers(self, group: int) -> dict:
        token = jwt.encode(
            {"group_id": group, "aud": ["fastapi-users:auth"]},
            key=TEST_JWT_SECRET,
        )
        return {"authorization": f"Bearer {token}"}

    def _prepare_request(
        self, group: int, method: str, path: str, make_headers: bool = True
    ) -> Request:
        headers = self._make_headers(group) if make_headers else {}
        return build_request(method=method, path=path, headers=headers)

    def _assert_access_allow(self, result: EnforceResult, entrypoint: str):
        self.assertTrue(result.access_allowed)
        self.assertEqual(result.redirect_service, entrypoint)

    def _assert_access_denied(self, result: EnforceResult):
        self.assertFalse(result.access_allowed)
        self.assertIsNone(result.redirect_service)
