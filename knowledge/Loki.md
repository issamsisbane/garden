# Deployment Modes

https://grafana.com/docs/loki/latest/get-started/deployment-modes/

Loki is composed of differents microservices. We can run them in different mode depending of our need (small or big clusters with big scaling needs)
## Monolithic Mode

With this mode we just have a single binary handling all the microservices.

![[monolithic-mode.png]]

## Simple Scalable

The microservices are grouped by typed :
- Read
- Write
- Backend
![[scalable-monolithic-mode.png]]
## Microservices

Each microservice is an indepdendant application which can be scale independently.

![[microservices-mode.png]]