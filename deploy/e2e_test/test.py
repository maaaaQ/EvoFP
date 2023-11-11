import unittest
import requests
import logging
import pydantic
from sqlalchemy import create_engine
from sqlalchemy.sql import text

ENTRYPOINT = "http://policy-enforcement-service:5000/"
DATABASE_DSN = "postgresql://postgres:postgresql7@postgresql:5432/postgres"
ACCESS_DENIED_MESSAGE = {"message": "Content not found"}
ADMIN_GROUP_ID = 1
USER_GROUP_ID = 2

# setup logging
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


class TestCommonFunctionality(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)


class BaseUserTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_user: User = None
        self.access_token: str = None

    def setUp(self, group_id: int) -> None:
        self._register_test_user(group_id)
        self._login()

    def tearDown(self) -> None:
        self._delete_test_user()

    def _register_test_user(self, group_id: int) -> User:
        payload = {
            "email": "test@mail.com",
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
            response = requests.post(f"{ENTRYPOINT}auth/register", json=payload)
            response.raise_for_status()
            self.test_user = User(**response.json())
        except requests.exceptions.HTTPError as exc:
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

    def _set_superuser(self, is_superuser: bool):
        if self.test_user is None:
            return
        self.test_user.is_superuser = is_superuser
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(
                text(
                    f"""UPDATE "user" SET is_superuser = {self.test_user.is_superuser} WHERE id = '{self.test_user.id}';"""
                )
            )
            connection.commit()

    def _set_groupsid(self, group_id: int):
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
                "username": "test@mail.com",
                "password": "test",
            }
            response = requests.post(f"{ENTRYPOINT}auth/jwt/login", data=data)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}


class TestAdminPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(ADMIN_GROUP_ID)
        self._set_superuser(True)
        self._set_groupsid(1)
        self._login()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(f"{ENTRYPOINT}groups", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


class TestUserPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(USER_GROUP_ID)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groupname_by_id(self):
        self._raise_if_invalid_user()
        response = requests.get(f"{ENTRYPOINT}groups/1", headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_tasks_list(self):
        self._raise_if_invalid_user()
        response = requests.get(f"{ENTRYPOINT}tasks", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_create_new_task(self):
        self._raise_if_invalid_user()
        response = requests.post(
            f"{ENTRYPOINT}task",
            headers=self.auth_headers,
            json={
                "title": "title",
                "description": "description",
                "priority": "low",
                "is_completed": "not_completed",
                "created_at": "2023-11-10T09:23:06.698Z",
                "updated_at": "2023-11-10T09:23:06.698Z",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIsInstance(data, dict)

    def test_delete_comment_permissions(self):
        self._raise_if_invalid_user()
        response = requests.delete(f"{ENTRYPOINT}comments/5", headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)


if __name__ == "__main__":
    unittest.main()
