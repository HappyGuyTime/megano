# MEGANO Marketplace
![image](./frontend/static/frontend/assets/img/logo.png)

MEGANO is a marketplace project built with Django and Django REST framework. 
It allows users to browse and purchase products across various categories.

## Installation

To run the project locally using Docker Compose, follow these steps:

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/HappyGuyTime/megano.git
    cd megano
    ```

2. Create a `.env` file in the project root directory with the required environment variables. Here's an example:

    ```plaintext
    SECRET_KEY=your-secret-key
    DEBUG=1
    ```

3. Build and start the Docker containers.

    ```bash
    docker-compose up -d --build
    ```

4. Apply migrations to set up the required tables.

    ```bash
    docker-compose exec megano python manage.py migrate
    ```

5. Add product data to the database if it's not available.

    ```bash
    docker-compose exec megano python manage.py create_data
    ```

6. The development server should now be running. Open your web browser and navigate to [http://localhost:8000/](http://localhost:8000/) to access the project.

## Dependencies

MEGANO project uses the following dependencies:

- Python
- Django
- Django REST framework
- Pillow
- Gunicorn
- Django-filter

## Development Tools

The project also includes several development tools for code formatting and linting:

- Black
- Flake8
- Isort

You can find the specific versions in the pyproject.toml file.

## Project Structure

The project follows the standard Django project structure. The main components include:

- `products`: Contains models, views, and serializers for products and categories.
- `profiles`: Manages user profiles and authentication.
- `orders`: Handles order creation, processing, and payment.
- `frontend`: The frontend application for MEGANO.
