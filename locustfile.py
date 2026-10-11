from locust import HttpUser, task, between
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@test.com"

class WebsiteUser(HttpUser):
    # Виртуальный пользователь ждет от 1 до 3 секунд между запросами
    wait_time = between(1, 3)

    @task(3)
    def get_users(self):
        # 3 части нагрузки идет на чтение списка пользователей
        self.client.get("/api/users")

    @task(1)
    def create_user(self):
        # 1 часть нагрузки идет на генерацию и создание нового пользователя
        payload = {
            "name": "user_" + ''.join(random.choices(string.ascii_lowercase, k=5)),
            "email": random_email()
        }
        self.client.post("/api/users", json=payload)
