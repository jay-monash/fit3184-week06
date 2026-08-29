from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    # Health check is hit more frequently (weight 3)
    @task(3)
    def view_health(self):
        self.client.get("/health")

    # Courses list (weight 2)
    @task(2)
    def view_courses(self):
        self.client.get("/courses")

    # API interaction is hit less frequently (weight 1)
    @task(1)
    def view_fit3184(self):
        self.client.get("/api/v2/fit3184") # or v1