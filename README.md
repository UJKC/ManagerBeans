# ManagerBeans
Office ai
5001 /ai

# Home
3000 /

# Postgres
5432

# Postgres Admin
8050 - (5432)

# Dashboard
3001 /dash

# docker
workflow

# nginx
80 ()

# authorization
5000 /auth

# Node JS
5003 /node

# Task
5002 /task

# React Flow
3002 /flow

# docker visualizer
8080 ()

# Chat Bot
3003 /chat

# temp
File storage or artifact storage



# Nginx
docker build -t nginx-balancer .
docker run -it --name nginx-container -p 81:80 --network my-network nginx-balancer

# Home
docker build -t webapp-home .
docker run -it --name webapp-home -p 3000:3000 --network my-network webapp-home

# Dashboard
docker build -t webapp-dash .
docker run -it --name webapp-dash -p 3001:3000 --network my-network webapp-dash

# Postgres
docker run --name webapp-postgres --network  my-network -e POSTGRES_HOST_AUTH_METHOD=trust -v postgresdatabase:/var/lib/postgresql/data -d postgres

##
\l
\c ujwal
SELECT table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
AND table_schema NOT IN ('pg_catalog', 'information_schema');


# postgres cli
docker exec -it webapp-postgres psql -U postgres

# Auth
docker build -t webapp-auth .
docker run -it --name webapp-auth -p 5000:5000 --network my-network webapp-auth


# Postgres Admin (application working)
docker run -d --name webapp-pgadmin --network my-network -p 5050:5050  thajeztah/pgadmin4

# Swarm visualizer
docker swarm init
docker run -it -d -p 8081:8080 --name vis -v /var/run/docker.sock:/var/run/docker.sock dockersamples/visualizer

$$ docker swarm join --token SWMTKN-1-5pefww4sftexv76139ucuvmt3l4nx7c2n9hl25wqqzl5vy9ebs-ddgmadny55ij4l258f56zh23f 192.168.65.3:2377
$$ current node (onld95abuc43tdomv6yy9mvpr) is now a manager.

docker network create -d overlay replication
docker network inspect replication
docker service create --name nginx-container -p 81:80 --network replication --replicas 1 nginx-balancer
docker service create --name webapp-home -p 3000:3000 --network replication --replicas 1 webapp-home
docker service create --name webapp-postgres --network replication -e POSTGRES_HOST_AUTH_METHOD=trust --replicas 1 --mount type=volume,source=postgresdatabase,target=/var/lib/postgresql/data postgres
docker service create -d --network replication -p 5000:5000 --name webapp-auth --replicas 1 webapp-auth

$$ docker service update --replicas 7 sleep-app

docker service rm nginx-container
docker service rm webapp-home
docker service rm webapp-postgres
docker service rm webapp-auth

docker kill vis
docker swarm leave --force













events {
    worker_connections 1024;
}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://webapp-home;
        }

        location /login {
            proxy_pass http://webapp-home;
        }

        location /register {
            proxy_pass http://webapp-home;
        }

        location /auth/login {
            proxy_pass http://webapp-auth;
        }

        location /auth/register {
            proxy_pass http://webapp-auth;
        }

        location /pg {
            proxy_pass http://webapp-postgres;
        }
    }
}






events {
    worker_connections 1024;
}

http {
    server {
        listen 80;

        location / {
            proxy_pass http://webapp-home:3000;
        }

        location /auth/login {
            proxy_pass http://webapp-auth:5000/auth/login;
        }

        location /auth/connection-status {
            proxy_pass http://webapp-auth:5000/auth/connection-status;
        }
    }
}







http {
    server {
        listen 80;
        server_name localhost;

        location /auth {
            proxy_pass http://webapp-auth:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location / {
            proxy_pass http://webapp-home:3000;
        }
    }
}
