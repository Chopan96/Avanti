from avanti.tests.performance.test_locust import HttpUser, task, between
import os
class MyUser(HttpUser):
    host = os.getenv("LOCUST_HOST", "http://127.0.0.1:8000")  # Cambia esto al host de tu app

    @task
    def my_task(self):
        self.client.get("/")

class DjangoLoadTest(HttpUser):
    wait_time = between(1, 5)  # Tiempo de espera entre solicitudes (en segundos)

    @task(2)
    def index_page(self):
        # Prueba la página de inicio
        self.client.get("/")

    @task(1)
    def login_page(self):
        # Simula una solicitud a la página de inicio de sesión
        self.client.get("/login/")

    @task(3)
    def stress_post(self):
        # Simula el envío de un formulario (si aplica)
        self.client.post("/some-endpoint/", data={"key": "value"})

    def on_start(self):
        # Si tu aplicación requiere autenticación, inicia sesión aquí
        self.client.post("/login/", data={"username": "testuser", "password": "password123"})