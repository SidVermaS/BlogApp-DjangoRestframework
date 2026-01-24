```sh
    chmod +x ./entrypoint.sh && docker compose -f docker-compose-local.yaml up
```

```sh
    docker compose -f docker-compose-local.yaml up -d && docker compose -f docker-compose-local.yaml exec backend /app/entrypoint.sh both_migrate
```

```sh
    docker stop $(docker ps -aq)
    docker rm $(docker ps -aq)
    docker rmi $(docker images -aq)
    docker volume rm $(docker volume ls -q)
    docker network rm $(docker network ls -q)
```