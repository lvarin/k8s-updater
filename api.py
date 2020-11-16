from flask import Flask, json, request, Response

from updater.k8s import k8s_updater
import os
#get_deployments, set_deployments

try:
    uuid = os.environ['SECRET_UUID']
except KeyError:
    print("ERROR, define a variable 'SECRET_UUID'")
    exit(-1)

api = Flask(__name__)
k8s_updater = k8s_updater()

@api.route('/deploy', methods=['GET'])
def get_deploys():
    return Response(response=json.dumps(k8s_updater.get_deployments()),
                    status=200,
                    mimetype="application/json")

@api.route('/deploy/<name>', methods=['GET'])
def get_deploy(name):
    return Response(response=json.dumps(k8s_updater.get_deployments(name)),
                    status=200,
                    mimetype="application/json")

@api.route('/deploy/<name>', methods=['POST'])
def post_deploy(name):

    try:
        image = json.loads(request.form['image'])
    except:
        return "Error, no image parameter provider", 400

    try:
        if request.form['uuid'] != uuid:
            return "Access denied", 403
    except:
        return "Token 'uuid' required", 401

    status = k8s_updater.set_deployment(name, image['image'])
    return Response(response=json.dumps({"API status": status}),
                    status=201,
                    mimetype="application/json")

if __name__ == '__main__':
    api.run(host='0.0.0.0',
            port=5000)
