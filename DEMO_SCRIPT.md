# Video Demo Script (4-5 minutes)

**Intro (20s)** "I'm <NAME>, PRN <PRN>. I containerized a Flask app with Docker and deployed it on Kubernetes (k3s) on AWS EC2."

**Docker (90s)**
- `cat Dockerfile` : multi-stage build (deps in stage 1, small runtime in stage 2), slim base, requirements copied first for layer caching, --no-cache-dir, non-root user, HEALTHCHECK, gunicorn.
- `sudo docker build -t cloudnative-app:1.0 .` and `sudo docker images`
- `sudo docker run -d --name cn-test -p 5000:5000 cloudnative-app:1.0`, `sudo docker ps`, `curl localhost:5000/health`, `sudo docker logs cn-test`

**Kubernetes files (60s)**
- `cat k8s/deployment.yaml` : replicas 3, labels/selector, ConfigMap env, resource requests/limits, readiness + liveness probes, rolling update.
- `cat k8s/service.yaml` : NodePort 30080 -> port 80 -> container port 5000, selector matches pod labels.

**Deploy & demo (90s)**
- `kubectl apply -f k8s/`
- `kubectl get pods -o wide`, `kubectl get deploy`, `kubectl get svc`
- Browser `http://<EC2-IP>:30080`, refresh several times: pod name changes = load balancing.
- `kubectl delete pod <one-pod>` then `kubectl get pods`: a new pod is created = self-healing.
- `kubectl scale deployment cloudnative-app --replicas=5`: scaling.

**Concepts recap (20s)** Image, container, Dockerfile layers, Pod, Deployment, ReplicaSet, Service, ConfigMap, probes, resource limits, self-healing, scaling, rolling updates.
