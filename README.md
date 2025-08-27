# Task Management Tool

A simple web-based task management application built with Flask and containerized with Docker.

## Description

This application allows users to create, view, complete, and delete tasks. It was built as a demonstration of a simple web application using Python's Flask framework. The entire application is designed to be run inside a Docker container.

## Tech Stack

- **Backend:** Python 3.9, Flask
- **WSGI Server:** Gunicorn
- **Containerization:** Docker

## How to Run

To run this application, you need to have Docker installed on your system.

1.  **Build the Docker image:**
    Open your terminal in the project root directory and run the following command to build the Docker image. You may need to use `sudo` depending on your Docker setup.

    ```bash
    docker build -t task-manager .
    ```

2.  **Run the Docker container:**
    Once the image is built, run the following command to start the application container.

    ```bash
    docker run -d -p 5000:5000 --name task-manager-app task-manager
    ```
    *   `-d` runs the container in detached mode.
    *   `-p 5000:5000` maps port 5000 of your machine to port 5000 of the container.
    *   `--name task-manager-app` gives a convenient name to the running container.

3.  **Access the application:**
    Open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000)

4.  **To stop and remove the container:**
    ```bash
    docker stop task-manager-app
    docker rm task-manager-app
    ```
