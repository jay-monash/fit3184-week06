import os
import random
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)
    image_dir = "image_source" #change this to your local test image directory
    images = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    @task
    def detect_stress_test(self):
        if not self.images:
            return
        image_path = os.path.join(self.image_dir, random.choice(self.images))
        with open(image_path, "rb") as image_file:
            self.client.post("/detect", files={"file": image_file})