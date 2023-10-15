import random
from locust import HttpUser, TaskSet, task, between

class Usuario (HttpUser):
    tiempo_espera = between(1, 5)

    @task
    def prueba_request_xml(self):
        self.client.get('/meal_ingredients')
    @task
    def prueba_request_xml(self):
        self.client.get('/meal_ingredients/1&json')
    @task
    def prueba_request_json(self):
        self.client.get('/meal_ingredients/1&xml')