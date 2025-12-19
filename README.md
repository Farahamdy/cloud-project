Income API – Kubernetes Deployment & Autoscaling
📌 Overview

Income API is deployed on Kubernetes and automatically scales based on CPU usage using Horizontal Pod Autoscaler (HPA).
This project demonstrates:

Kubernetes Deployment & Service

Metrics Server integration

CPU-based autoscaling

Load testing using a load generator

✅ Prerequisites

Make sure you have the following:

1. Kubernetes Cluster (Docker Desktop Kubernetes / Minikube / Kind)

2. kubectl configured

3. Metrics Server installed & working

Verify Metrics Server:

kubectl top nodes
kubectl top pods


If they show CPU usage, you are ready 🚀

🚀 Deploy the Application
1️⃣ Apply Deployment & Service

(These YAML files were generated using kubectl — not manually written.)

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml


Check resources:

kubectl get pods
kubectl get svc

🌐 Access the API
🔹 Option 1 — Port Forward (Recommended)
kubectl port-forward svc/income-api 8080:80


Open in browser / Postman:

http://localhost:8080

🔹 Option 2 — NodePort (If Service is NodePort)

Check:

kubectl get svc income-api


Then access:

http://localhost:<NodePort>

🧪 Test the API

Example request:

curl http://localhost:8080/


If your API has endpoints (like /income, /predict, etc.), replace accordingly.

📈 Horizontal Pod Autoscaler (HPA)

Check HPA:

kubectl get hpa
kubectl describe hpa income-api


Watch live scaling:

kubectl get hpa income-api -w


Check pods:

kubectl get pods

🔥 Load Testing (Trigger Autoscaling)

If a load-generator pod is deployed, it will automatically generate traffic.

You should start seeing:

TARGETS increasing
REPLICAS increasing


Example:

cpu: 70% / 50%
Replicas: 1 → 5

🧹 Cleanup

To remove everything:

kubectl delete deployment income-api
kubectl delete svc income-api
kubectl delete hpa income-api
