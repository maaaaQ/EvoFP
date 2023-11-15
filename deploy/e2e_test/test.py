import unittest
import requests
import logging
import pydantic
from sqlalchemy import create_engine
from sqlalchemy.sql import text


ENTRYPOINT = "http://policy-enforcement-service:5000/"
DATABASE_DSN = "postgresql://postgres:postgresql7@postgresql:5432/postgres"
ACCESS_DENIED_MESSAGE = {"message": "Content not found"}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)-9s %(message)s")


class User(pydantic.BaseModel):
    id: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    first_name: str
    last_name: str
    nickname: str
    age: int
    group_id: int

    class Config:
        arbitrary_types_allowed = True


class Task(pydantic.BaseModel):
    id: int
    title: str
    description: str
    priority: str
    is_completed: str
    created_at: str
    updated_at: str
    user_id: str

    class Config:
        arbitrary_types_allowed = True


class Comment(pydantic.BaseModel):
    id: int
    text: str
    user_id: str
    created_at: str
    task_id: int

    class Config:
        arbitrary_types_allowed = True


class TestCommonFunctionality(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT, timeout=3)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)


class BaseUserTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_user: User = None
        self.access_token: str = None
        self.test_task: Task = None
        self.test_comment: Comment = None

    def setUp(self, group_id: int = None) -> None:
        self._register_test_user(group_id)
        self._login()
        self.test_task = self._create_test_task()
        self.test_comment = self._create_test_comment()

    def tearDown(self) -> None:
        self._delete_test_comment()
        self._delete_test_task()
        self._delete_test_user()

    def _register_test_user(self, group_id: int) -> User:
        payload = {
            "email": "tester@gmail.com",
            "password": "test",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "first_name": "string",
            "last_name": "string",
            "nickname": "string",
            "age": 29,
            "group_id": group_id,
        }
        try:
            response = requests.post(
                f"{ENTRYPOINT}auth/register", json=payload, timeout=3
            )
            response.raise_for_status()
            self.test_user = User(**response.json())
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    def _create_test_task(self) -> Task:
        if self.test_user is None:
            raise Exception("Cannot create task without valid user!")
        payload = {
            "title": "Test",
            "description": "Testing",
            "priority": "high",
            "is_completed": "not_completed",
            "created_at": "2023-11-10T09:23:06.698Z",
            "updated_at": "2023-11-10T09:23:06.698Z",
            "user_id": self.test_user.id,
        }
        try:
            response = requests.post(
                f"{ENTRYPOINT}task", json=payload, headers=self.auth_headers, timeout=3
            )
            response.raise_for_status()
            return Task(**response.json())

        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    def _create_test_comment(self) -> Comment:
        if self.test_user is None or self.test_task is None:
            raise Exception("Cannot create comment without valid user and task!")
        payload = {
            "id": 1,
            "text": "Test",
            "user_id": self.test_user.id,
            "created_at": "2023-11-10T09:23:06.698Z",
            "task_id": self.test_task.id,
        }
        try:
            response = requests.post(
                f"{ENTRYPOINT}comments",
                json=payload,
                headers=self.auth_headers,
                timeout=3,
            )
            response.raise_for_status()
            return Comment(**response.json())
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)
        except Exception as exc:
            print(exc)
            logger.error(exc)

    def _raise_if_invalid_user(self):
        if self.test_user is None:
            raise Exception("Cannot continue test without valid user!")

    def _delete_test_user(self):
        if self.test_user is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(
                text(f"""DELETE FROM "user" WHERE id = '{self.test_user.id}';""")
            )
            connection.commit()

    def _delete_test_task(self):
        if self.test_task is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(
                text(f"""DELETE FROM "tasks" WHERE id = '{self.test_task.id}';""")
            )
            connection.commit()

    def _delete_test_comment(self):
        if self.test_comment is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(
                text(f"""DELETE FROM "comments" WHERE id = '{self.test_comment.id}';""")
            )
            connection.commit()

    def _set_group_id(self, group_id: int):
        if self.test_user is None:
            return
        self.test_user.group_id = group_id
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(
                text(
                    f"""UPDATE "user" SET group_id = {self.test_user.group_id} WHERE id = '{self.test_user.id}';"""
                )
            )
            connection.commit()

    def _login(self):
        self._raise_if_invalid_user()
        try:
            data = {
                "username": "tester@gmail.com",
                "password": "test",
            }
            response = requests.post(
                f"{ENTRYPOINT}auth/jwt/login", data=data, timeout=3
            )
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}


class TestAdminPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._set_group_id(1)
        self._login()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_groups_list(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.get(
            f"{ENTRYPOINT}groups", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_groupname_by_id(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.get(
            f"{ENTRYPOINT}groups/1", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

    def test_delete_user_task(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        task_id = self.test_task.id
        response = requests.delete(
            f"{ENTRYPOINT}tasks/{task_id}", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

    def test_delete_user_comment_on_task(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.delete(
            f"{ENTRYPOINT}comments/{self.test_comment.id}?tasks_id={self.test_task.id}",
            headers=self.auth_headers,
            timeout=3,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)


class TestUserPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_groupname_by_id(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.get(
            f"{ENTRYPOINT}groups/1", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_tasks_list(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.get(
            f"{ENTRYPOINT}tasks", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_comments_list(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.get(
            f"{ENTRYPOINT}comments", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_create_new_task(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.post(
            f"{ENTRYPOINT}task",
            headers=self.auth_headers,
            json={
                "title": "title",
                "description": "description",
                "priority": "high",
                "is_completed": "not_completed",
                "created_at": "2023-11-10T09:30:06.698Z",
                "updated_at": "2023-11-10T09:30:06.698Z",
                "user_id": self.test_user.id,
            },
            timeout=3,
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIsInstance(data, dict)
        task_id = data.get("id")
        response = requests.delete(
            f"{ENTRYPOINT}tasks/{task_id}", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_permissions(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        response = requests.delete(
            f"{ENTRYPOINT}comments/{self.test_comment.id}",
            headers=self.auth_headers,
            timeout=3,
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_delete_user_permissions(self):
        if self.test_user is None:
            return
        self._raise_if_invalid_user()
        user_id = self.test_user.id
        response = requests.delete(
            f"{ENTRYPOINT}users/{user_id}", headers=self.auth_headers, timeout=3
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)


if __name__ == "__main__":
    unittest.main()
