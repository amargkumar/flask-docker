# Dockerized Flask App

A Flask web app running inside a Docker container, adapted from the archived Runnable.com tutorial to work using Python 2 on Ubuntu 18.04. The page is a small dashboard that shows details about the container it's running in (container ID, OS, Python and Flask versions, uptime, visits), plus a JSON endpoint at `/api/info`.

![Screenshot of the running app](screenshot.png)

## Running
```bash
docker build -t flask-tutorial:latest .
docker run -d -p 5000:5000 flask-tutorial
```
Then open http://localhost:5000.
