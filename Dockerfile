# Dockerfile, Image, Container
# Dockerfile is a blueprint for building images
# Image is a template for running containers
# Container is the actual running process

From python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN echo eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJwcm9kLXVzZXItY2xpZW50OnRpYWdvZmVybmFuZGVzIiwiaXNzIjoiYWdlbnQ6dGlhZ29mZXJuYW5kZXM6OjQyZWExNTFmLWE0ODktNDE4Ni05MWVhLWRmMGI3MGIwNzcwMSIsImlhdCI6MTU3MTU4NzUxMSwicm9sZSI6WyJ1c2VyX2FwaV9yZWFkIiwidXNlcl9hcGlfd3JpdGUiXSwiZ2VuZXJhbC1wdXJwb3NlIjp0cnVlLCJzYW1sIjp7fX0.gPMTGzt5r-puRdW6IgFhe2gtHh8DOmsQsF5AWX6nRp2zqKACmKohH8J9k3qs_yisSuYrWDHiFMpd1usG7gn-gg | dw configure

CMD ["python3.8", "./main.py"]
