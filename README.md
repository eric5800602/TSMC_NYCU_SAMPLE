# TSMC_NYCU_SAMPLE 期末專題，範例程式碼
## 操作流程
* gcloud config set project trainer-lab
* gcloud config set compute/zone asia-east1
* gcloud config set compute/region asia-east1
* gcloud container clusters get-credentials helloworld-gke
* kubectl config set-context --current --namespace=final-16
* kubectl apply -f crawler-deployment.yaml
* kubectl apply -f crawler-service.yaml
* Run Ingress&service on GKE
* curl IP/google_search/TSMC
    * 把 google search 過去一小時內有包含 TSMC 的 URL 存在 `TSMC.txt`，可以當作 url 管理
    * ![](https://i.imgur.com/kk4ZVfj.png)
* curl IP/query/TSMC
    * 從`TSMC.txt`抓出 url，並爬蟲找出 "TSMC" 關鍵字數量
    * ![](https://i.imgur.com/hO86lQF.png)
* Docker image：https://hub.docker.com/repository/docker/eric5800602/mycrawler




