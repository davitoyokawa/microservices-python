# Distributed System with Flask, Django, and RabbitMQ

## 📌 Description
  This project is a distributed system based on microservices that interact asynchronously using RabbitMQ. It consists of two main services:

- **Client (Flask)**: Allows users to like and rate products.
- **Admin (Django)**: Manages products and processes rating and like messages.

The system is scalable and utilizes Docker, NGINX, and Consul for load balancing and service discovery.

## 🚀 Technologies Used
- **Python (Flask & Django)**
- **RabbitMQ** (messaging broker)
- **Docker & Docker Compose**
- **NGINX** (reverse proxy and load balancing)
- **Consul** (service discovery)
- **MySQL & SQLite** (databases)
- **Postman** (API testing)

## 📌 Main Endpoints
### Client Service (Flask)
- `POST /api/products/<id>/like` → Like a product
- `POST /api/products/<id>/rate` → Rate a product
- `GET /api/products` → List products

### Admin Service (Django)
- `GET /products/` → List all products
- `POST /products/` → Create a new product
- `PUT /products/<id>/` → Update a product
- `DELETE /products/<id>/` → Delete a product
