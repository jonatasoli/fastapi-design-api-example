from locust import HttpUser, TaskSet, task
from order.schemas.schemas_order import orderModelBase

HEADERS = {"Content-Type": "application/json"}


class orderModelTask(TaskSet):
    @task
    def post(self):
        _data = ()
        self.client.post("/orders", data=_data.dict(), headers=HEADERS)


class stressTest(HttpUser):
    tasks = [orderModelTask]
    host = "http://localhost:8888"
    min_wait = 5000
    max_wait = 10000
