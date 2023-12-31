import random
from locust import HttpUser, TaskSet, task, between

class Usuario (HttpUser):
    tiempo_espera = between(1, 5)

    @task
    def prueba_request_xml(self):
        self.client.get('/long_stop')
    @task
    def prueba_request_xml(self):
        self.client.get('/long_stop/1&json')
    @task
    def prueba_request_json(self):
        self.client.get('/long_stop/1&xml')