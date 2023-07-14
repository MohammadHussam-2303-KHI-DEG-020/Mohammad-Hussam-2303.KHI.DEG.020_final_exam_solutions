# Docker task

In the `app.py` file you're given an implementation of an app. It exposes an endpoint allowing users to get the maximum and minimum tempereture predicted for next few days for a given location – latitude and longitude.

The app uses Redis as a cache. Cache key are coordinates truncated to two decimal points (so `24.8608,67.0104` and `24.8612,67.0197` will result with the same key `24.86:67.01`). Each entry in the cache expires after 24h.

Your task is to:
* write `Dockerfile` to run the app in a container,
* write `docker-compose.yml` to run the app together with Redis.

Requirements:
* You **can't** (and don't need to) edit `app.py` file.
* You **can** create any other files you find useful.
* Last line of your `Dockerfile` should be `CMD ["python", "app.py"]`.
* The app should be accessible on port `8001` on host computer (so one should be able to access it eg. via web browser `0.0.0.0:8001/weather/24.8608/67.0104` -- these are the coordinates for Karachi).
* The app should use port `3000` inside of the container.
* In the submission include the whole working solution – after downloading your solution we should be able to run it with `docker compose up`, without making any edits or fixes.

Hints:
* You can use [`redis:alpine`](https://hub.docker.com/_/redis) image to run Redis.
* Note that the app wants to access Redis on port `6380` which is not a default one. You need to find out how to change the port Redis uses (there's a flag for that).
* Creating `requirements.txt` file is useful for managing required packages.