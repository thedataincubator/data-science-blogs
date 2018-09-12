# Flask Apps on Kubernetes

At [The Data Incubator](https://www.thedataincubator.com/) we use Kubernetes with varying hardware back ends to power a large portion of our resources.  Kubernetes orchestrates containers within a cluster of compute resources and allows seamless networking within the cluster.  All your microservices can easily talk to each other without having to care too much about the details of how those requests get routed around the cluster components.  For many services, this internal networking is enough, but sometimes we do need to talk to the outside world.  When we do so, best practices dictate we use SSL encryption which requires both exposing an internal service to external requests and provisioning the proper certificates into the cluster.  This guide will walk you through creating a simple Flask application in a containerized fashion, using Kubernetes to run this as a deployment, and finally exposing the deployment to the outside world over an encrypted connection using an `Ingress` and certificates provisioned for free by [Let's Encrypt](https://letsencrypt.org/).  

This article assumes a running Kubernetes cluster, preferably with helm running.  Our example is built for a bare metal cluster running on [Digital Ocean](https://www.digitalocean.com), but extensions to other providers should be fairly straightforward.  We also assume that `docker` and `kubectl` are installed.

## Dockerize that Flask application

The first step we must take is to Dockerize our Flask application.  We will start an app based on the excellent template by `Kenneth Reitz` [repo](https://github.com/thedataincubator/flask-framework/tree/docker).  Add your flask entry point flask code to the `app/app.py` file, we recommend something very simple.  Once this is complete we can run a docker command to build our application into a Docker image, but before we deploy to our Kubernetes cluster, we should test locally.  One of the many advantages of Docker is that if it works locally it "should" work pretty much anywhere.

So lets do this in a few steps. First we can build our app from the directory containing the `Dockerfile` with the follow command

```bash
docker build -t k8s-flask .
```

and then run it locally with

```bash
docker run -it -e PORT=5000 -p 5000:5000 k8s-flask
```

While this running, you can navigate to `localhost:5000` in a web browser of your choice and hopefully see your application.  The application is being run with `gunicorn` so its fairly ready for the prime time.  Remember to adhere to good practices here, make most things stateless and if you need to use state, use a database. 

Finally, we can push our application to a docker repository (or push to Github and build off CI).  You can use a repository of your choice, a few ones we have used are `AWS` (ECR), `GCP` (GCR), `DockerHub`, `Quay.io`.  If you do use a private repository, you will need set `imagePullSecrets` on the `serviceAccount` relevant to the pod that contains your app.   We have found that properly versioning our images is extremely important and you can always do this either by referencing the relevant commit, or by hashing your code.  Now that we have a containerized application, lets deploy it on our Kubernetes cluster. 

## Create a Deployment

Here we will use a `Deployment` to control how our application is deployed across the Kubernetes cluster (rather well named).  We can think of the `Deployment` as controlling the desired state of our application and it specifies details like how many replicas of our container we desire, how much memory to allocate to each one, and environmental variables that should be passed to each container.  Kubernetes will perform actions to ensure that the state described in the `Deployment` matches reality and handle things like node failures, upgrades, and scaling.  Our deployment should look something like 

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: k8s-flask
  labels:
    app: k8s-flask
spec:
  replicas: 2
  strategy: 
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      app: k8s-flask
  template:
    metadata:
      labels:
        app: k8s-flask
    spec:
      serviceAccountName: default
      containers:
      - name: k8s-flask-container
        image: <Path to image repo>
        env:
        - name: PORT
          value: "5000"
        resources:
          limits:
            memory: "2Gi"
        ports:
        - containerPort: 5000
```

## Create a Service

Next we need to create a `Service` which will allow Kubernetes to know how to route requests to the different pods in our `Deployment`.  We will have it target the port upon which we have set our flask application to run.  Once we create this `Service`, Kubernetes will handle routing requests on the internal cluster network to the proper pods and take care of the details of managing the network addresses.  The configuration might look something like 

```yaml
kind: Service
apiVersion: v1
metadata:
  name: k8s-flask
spec:
  selector:
    app: k8s-flask
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 5000
```


## Create an Ingress
Now that we have the application communicating within the cluster, we need to expose it to the outside world.  There are multiple ways of doing this and some will depend upon the cloud provider you are using, however, one fairly general and flexible way is with an Ingress.  Here we specify a particular host and we can route different paths on that host to different services on our back end.  This is exceptionally useful if you want to have versioned apis or microservices living at different endpoints. 

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: k8s-flask-ingress
  namespace: <Project Namespace>
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: 'true'
spec:
  rules:
  - host: <HOST>
    http:
      paths:
      - path: /
        backend:
          serviceName: k8s-flask
          servicePort: 80

  tls:
    - hosts:
      - <HOST>
      secretName: kubelego-tls-k8s-flask
```

These annotations are important, they tell the `Ingress` to look for a specific type of `Ingress` controller which we will create soon and also that we want to attempt to provision an SSL certificate for this domain.

## Create Ingress Controller
We have created an ingress, but we don't have a proper way of routing traffic without an ingress-controller.  If you are running on GKE, there is a built in ingress controller, but another commonly used on is that [`nginx-ingress-controller`](https://github.com/kubernetes/ingress-nginx).  We will use this to hook up our `Ingress` to the outside world.  We can use helm to deploy this on our cluster and then point an external load balancer with a fixed ip to the ports opened by this controller.  Luckily we can use a prebuilt helm chart to set this up

```bash
helm install stable/nginx-ingress --name my-nginx
```

If you don't want to use helm, the documentation can walk you through setting this up.  If you are using RBAC (and hopeully you are), there is a flag that can be used here to set up the proper resources to make this work.

This next bit depends a bit on your cloud provider, but if an external load balancer is not automatically created, one can get the exposed ports with

```bash
kubectl get svc <ingress-controller>
```

Under the `PORT(s)` section you will see something like `80:<HTTP_PORT>/TCP, 443:<HTTPS_PORT>/TCP` which will give you the HTTP and HTTPS port your ingress is listening on.  We can get at these programmatically by pulling down and parsing the `yaml` config.  Here we will make use of the excellent [`shyaml`](https://github.com/0k/shyaml) tool.

```bash
HTTP_PORT=$(kubectl get svc <ingress-controller> -o yaml | shyaml get-value spec.ports.0.nodePort)
HTTPS_PORT=$(kubectl get svc <ingress-controller> -o yaml | shyaml get-value spec.ports.1.nodePort)
```

## Set Up DNS records
Now we can set up an `A` record to point at our static ip (or a `CNAME` record if you are using a `LoadBalancer` without a static ip).  This will direct traffic to our host to the `LoadBalancer` which will direct the traffic to our ingress-controller.  With this configuration we are relying on the specified host in the Ingress and without this configuration, your website will not be able to run.  If you want to check your application without setting up DNS records, you can use a `NodePort` in your service description.  This will open up a port on all of your nodes through which you can communicate with the service.  You can then point your `LoadBalancer` at these ports.

## Get SSL Certificate
We can use lets-encrypt to supply a ssl certificate for our pods and use the [`kube-lego`](https://github.com/jetstack/kube-lego) service to automatically provision and keep updated certificates for all the hosts specific in our ingresses.  We will need to create an annotation on the ingresses we want to be marked.  Before you deploy this, make sure that your application is reachable over both http and https.

```bash
helm install --name lego stable/kube-lego --set config.LEGO_EMAIL=<email> --set config.LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
```

As before, you can set up the RBAC with just a simple flag.

Now you should have a working flask app backed by a Kubernetes cluster and with a properly provisioned SSL certificate.  Feel free to change the number of replicas in your deployment to seamlessly scale up your Deployment to meet your needs.

If you want the entire code here packaged up a single helm chart, check out [flask-chart](https://github.com/thedataincubator/flask-chart)
