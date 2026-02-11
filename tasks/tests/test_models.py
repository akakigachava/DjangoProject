from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from tasks.models import Task


User = get_user_model()


def auth_headers_for(user):
    access_token = RefreshToken.for_user(user).access_token
    return f"Bearer {access_token}"


class TaskAPITests(APITestCase):
    def setUp(self):

        self.user1 = User.objects.create_user(username="u1", password="pass12345")
        self.user2 = User.objects.create_user(username="u2", password="pass12345")


        Task.objects.create(owner=self.user1, title="u1 task", priority="LOW")
        Task.objects.create(owner=self.user2, title="u2 task", priority="HIGH")


        self.url = "/api/tasks/"

    def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=auth_headers_for(self.user1))

        dumptest={
            "title": "test task",
            "description": "test description",
            "priority": "HIGH",
            "is_done": False,
        }

        res=self.client.post(self.url, dumptest, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Task.objects.filter(title="test task", owner=self.user1).exists())

        task = Task.objects.get(title="test task", owner=self.user1)

        self.assertEqual(task.description, "test description")
        self.assertEqual(task.priority, "HIGH")
        self.assertEqual(task.is_done, False)

        self.assertFalse(Task.objects.filter(title="test task", owner=self.user2).exists())

    def test_list_returns_only_my_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION=auth_headers_for(self.user1))
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data["count"], 1)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["title"], "u1 task")

    def test_update_task_updates_fields(self):
        task = Task.objects.get(owner=self.user1, title="u1 task")
        detail_url = f"{self.url}{task.id}/"

        self.client.credentials(HTTP_AUTHORIZATION=auth_headers_for(self.user1))

        dumptest = {
            "title": "updated title",
            "description": "updated desc",
            "priority": "HIGH",
            "is_done": True,
        }

        res = self.client.patch(detail_url, dumptest, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        task.refresh_from_db()
        self.assertEqual(task.title, "updated title")
        self.assertEqual(task.description, "updated desc")
        self.assertEqual(task.priority, "HIGH")
        self.assertEqual(task.is_done, True)

    def test_delete_task_deletes_only_owner_task(self):
        task=Task.objects.get(owner=self.user1, title="u1 task")
        detail_url = f"{self.url}{task.id}/"

        self.client.credentials(HTTP_AUTHORIZATION=auth_headers_for(self.user1))
        res = self.client.delete(detail_url, format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(title="u1 task").exists())


    def test_user_doesnt_have_permission_to_other_users_tasks(self):
        task=Task.objects.get(owner=self.user1, title="u1 task")
        detail_url = f"{self.url}{task.id}/"

        self.client.credentials(HTTP_AUTHORIZATION=auth_headers_for(self.user2))
        resupdate = self.client.patch(detail_url, {"title": "hacked"}, format="json")
        self.assertIn(resupdate.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

        self.assertEqual(task.title, "u1 task")
        resdelete = self.client.delete(detail_url, format="json")

        self.assertIn(resdelete.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        self.assertTrue(Task.objects.filter(title="u1 task").exists())

