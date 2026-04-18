# Лабораторная работа 2

## Устанавливаем **Istio:**
``` 
curl -L https://istio.io/downloadIstio | sh -
```
Выбор пал на Istio, потому что является стандартом для Kubernetes.

### Структура папки
- ```bin/istioctl``` — исполняемый файл для управления mesh.
- ```samples/bookinfo/platform/kube/bookinfo.yaml``` — основной файл приложения (Deployment, Services).
- ```samples/bookinfo/networking/``` — файлы для настройки трафика (Gateways, VirtualServices).
- ```samples/addons/``` — манифесты для мониторинга (Kiali, Prometheus, Grafana, Jaeger).

## Запуск стенда
### Подготовка 
```
export PATH=$PWD/bin:$PATH

istioctl install --set profile=demo -y

kubectl label namespace default istio-injection=enabled
```
Благодаря этим командам мы создаем систему, где сервисы просто работают, а всю сложную работу по безопасности и мониторингу берет на себя Istio.

### Запуск приложения Bookinfo
```
kubectl delete -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
```
### Запуск Dashboard
```
istioctl dashboard kiali
```
<img width="1512" height="871" alt="Screenshot 2026-04-18 at 17 39 07" src="https://github.com/user-attachments/assets/8c6352b4-a309-4022-ac83-37bdf9d27fcc" />

Для создания трафика запускаем:
```
 kubectl port-forward svc/productpage 9080:9080
```
### Создание 2 файлов
Создаем файл security.yaml и my-gateway.yaml. 

my-gateway.yaml
- Gateway: Открывает «дверь» (порт 80) в кластер для внешнего мира.
- VirtualService: Объясняет, куда идти. Если пришел запрос на /productpage, он направляет его к конкретному микросервису.

security.yaml
- mTLS (STRICT): Заставляет все сервисы общаться только по зашифрованному каналу.
- Аутентификация: Каждый сервис проверяет сертификат другого перед тем, как передать данные.

График в kaili:
<img width="1197" height="776" alt="Screenshot 2026-04-18 at 18 11 05" src="https://github.com/user-attachments/assets/39b2cb54-c92f-4d27-9e01-64a85eca8c66" />
