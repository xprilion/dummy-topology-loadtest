from flask import Flask
from flask import request,jsonify
import pickle

with open("../project_one_model.pkl","rb") as f_in:
    dv,model = pickle.load(f_in)

app = Flask('Predict')

@app.route('/predict',methods=['POST'])
def predict():
    candidate = request.get_json()
    X = dv.transform(candidate)
    preds = model.predict_proba(X)[:,1]
    placement = preds > 0.5
    result ={
        "Placement_Probability" : float(preds),
        "Placement" :bool(placement)
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)