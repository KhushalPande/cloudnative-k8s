# CloudNative Notes - Docker & Kubernetes Deployment

A small Flask web app that shows which container/pod served the request.
It is containerized with a multi-stage Dockerfile and deployed to Kubernetes (k3s) on AWS EC2
with a Deployment (3 replicas), ConfigMap and NodePort Service.

## Structure
```
.
├── app.py               # Flask app (/, /health, /api/info)
├── requirements.txt
├── Dockerfile           # multi-stage, slim image, non-root user, HEALTHCHECK
├── .dockerignore
└── k8s/
    ├── configmap.yaml   # environment configuration
    ├── deployment.yaml  # 3 replicas, probes, resource requests/limits, rolling update
    └── service.yaml     # NodePort 30080 -> 80 -> 5000
```

## Docker
```bash
docker build -t cloudnative-app:1.0 .
docker images cloudnative-app
docker run -d --name cn-test -p 5000:5000 cloudnative-app:1.0
curl http://localhost:5000/health
docker logs cn-test
docker stop cn-test && docker rm cn-test
```

## Kubernetes (k3s on Ubuntu EC2)
```bash
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
docker save cloudnative-app:1.0 | sudo k3s ctr images import -
kubectl apply -f k8s/
kubectl get pods -o wide
kubectl get svc
```
Open `http://<EC2-PUBLIC-IP>:30080` (security group must allow TCP 30080).
