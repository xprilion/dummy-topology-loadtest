from flask import Flask
from flask import request,jsonify
import json
import random
import requests

app = Flask('Router')

candidate = [{"gender": "M",
  "ssc_p": 71.0,
  "ssc_b": 'Central',
  "hsc_p": 90.66,
  "hsc_b": 'Central',
  "hsc_s": 'Science',
  "degree_p": 90.0,
  "degree_t": 'Sci&Tech',
  "etest_p": 90.0,
  "mba_p": 90.3,
  "specialisation": 'Mkt&Fin',
  "workex": 'Yes',
  }]

node_threshold = 10

topologies = ["single", "2active", "3active"]

topology = 0

topologyFile =  "topology/"+topologies[topology]+".json"

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    nodes = None
    with open(topologyFile) as f:
        nodes = json.load(f)
    nodeLoad = 0
    nodesTried = 0
    activeNodes = {item:data for (item,data) in nodes.items() if data["status"] == True}
    passiveNodes = {item:data for (item,data) in nodes.items() if data["status"] == False}
    # print("Starting loop")
    while nodesTried < len(nodes.keys()):
        nodesTried += 1
        # print("nodesTried: ", nodesTried)
        randomNodeKey = random.choice(list(activeNodes.keys()))
        nodeLoad = nodes[randomNodeKey]["load"]
        if nodeLoad < node_threshold:
            nodesTried = 0
            nodes[randomNodeKey]["load"] += 1
            with open(topologyFile, "w") as f:
                json.dump(nodes, f, indent=4)

            url = "http://0.0.0.0:"+nodes[randomNodeKey]["port"]+"/predict"
            result = requests.post(url=url,json=candidate).json()

            nodes[randomNodeKey]["load"] -= 1
            with open(topologyFile, "w") as f:
                json.dump(nodes, f, indent=4)

            return result
        else:
            del activeNodes[randomNodeKey]
            # print("Removing node from available nodes:", randomNodeKey)
            if len(activeNodes.keys()) == 0 and len(passiveNodes.keys()) > 0:
                print("Condition met, activating node")
                randomNodeKey = random.choice(list(passiveNodes.keys()))
                nodeLoad = nodes[randomNodeKey]["load"]
                if nodeLoad < node_threshold:
                    nodes[randomNodeKey]["status"] = True
                    activeNodes[randomNodeKey] = nodes[randomNodeKey]
                    del passiveNodes[randomNodeKey]
            else:
                pass
                # print("Active nodes: ", len(activeNodes.keys()), activeNodes.keys())
                # print("Passive nodes: ", len(passiveNodes.keys()), passiveNodes.keys())
    
    return {"error": "No available nodes"}, 501
    # return jsonify(nodes)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)