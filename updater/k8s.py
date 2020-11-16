from kubernetes import client, config
import os
import json
import re

class k8s_updater:

    deployments = [{"image": "test/test:tag"}]

    #APISERVER='kubernetes.default.svc:443'

    def __init__(self):
        self.namespace='csc-wes'
        if os.getenv('KUBERNETES_SERVICE_HOST'):
            k8s_config = config.load_incluster_config()
        else:
            k8s_config = config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apiV1 = client.AppsV1Api()

    def get_deployments(self, name=None):
        if name is None:
            pod_list = self.apiV1.list_namespaced_deployment(self.namespace)
            pods = []
            for pod in pod_list.items:
                pods.append(pod.metadata.name)
            return pods

        deployments = self.apiV1.list_namespaced_deployment(self.namespace)
        # Probably not the best way to do it
        for deployment in deployments.items:
            if deployment.metadata.name == name:
                return deployment.spec.template.spec.containers[0].image
        
        return None

    def set_deployment(self, name, image):

        # Allow only to change the tag
        old_image = self.get_deployments(name)

        if re.split(":", old_image)[0] != re.split(":", image)[0]:
            return "Cannot change image, only tag"

        patch = [{"op":"replace", "value":image,
                 "path": "/spec/template/spec/containers/0/image"}]

        print("Patch: %s" % patch)
        response = self.apiV1.patch_namespaced_deployment(
                name=name,
                namespace=self.namespace,
                body=patch)

        return str(response.spec.template.spec.containers[0].image)