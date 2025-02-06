import requests
import os

service_name = os.getenv("SERVICE_NAME", "default_service")
service_port = os.getenv("SERVICE_PORT", "5000")
service_host = os.getenv("SERVICE_HOST", service_name)  
consul_url = os.getenv("CONSUL_URL", "http://localhost:8500")

service_data = {
    "Name": service_name,
    "Address": service_host,  
    "Port": int(service_port),
    "Check": {
        "HTTP": f"http://{service_host}:{service_port}/health", 
        "Interval": "10s",
        "Timeout": "5s"
    }
}

response = requests.put(f"{consul_url}/v1/agent/service/register", json=service_data)
if response.status_code == 200:
    print(f"Service {service_name} registered successfully!")
else:
    print(f"Failed to register service {service_name}: {response.text}")
