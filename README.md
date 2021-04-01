# k8s-updater

Very basic web service to update a deployment. In the future this code will evolve, it is just a prototype.

## Deployment

The image must run inside the namespace of the deployment to update. It must have a variable called 'SECRET_UUID' containing the secret that will be required in order to be allowed to update the deployment. The container must be running as a user that is allowed to change deployments.

## End points

* **GET**, `/deploy`. Returns a list of all deployments. For example:

```
curl -X GET https://$URL/deploy
["celery-worker", "cwlwes", "flower", "mongodb", "rabbitmq"]
```

* **GET**, `/deploy/<name>`. Returns the current image of the given <name> deployment. For example:

```
curl -X GET  https://$URL/deploy/example_name
"path/name:tag"
```

* **POST**, `/deploy/<name>`. Changes the tag of an image in the deployment. For example:

```
curl -X POST https://$URL/deploy/example_name -d 'image={"image":"path/name:tag2"}' \
-d 'uuid=XXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX'
{"API status": "path/name:tag2"}
```

In principle this will fail if the image name does not match with the current one.

