from platform import platform
from flask import Flask, render_template, request, jsonify, make_response
from pycaret.regression import load_model, predict_model
import pandas as pd

# import logging
# logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
model = load_model('./model/Final CatBoost Regressor 101122')
num_cols = ['Age', 'BMI', 'MET (activity level)']
cate_cols = ['Sex', 'Smoking', 'Heart rate data used']

def unit_prediction(df):
    prediction = predict_model(model, data=df)
    prediction["Label"] = [i if i>0 else 0 for i in prediction["Label"]]
    return prediction["Label"][0]

def process_ipt(ipts:str):
    new_obs = {
        "Age": [ipts.get("Age",0)],
        "BMI": [ipts.get("BMI",0)],
        "MET (activity level)": [ipts.get("MET (activity level)",0)],
        "Sex": [ipts.get("Sex",'')],
        "Smoking": [ipts.get("Smoking",'')],
        "Heart rate data used": [ipts.get("Heart rate data used",0)],
    }
    #print(new_obs)
    df = pd.DataFrame(new_obs)
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in cate_cols:
        df[col] = df[col].astype("category")
    return df

@app.route('/')
def index():
    return 'Hello World! This API is built using Flask for forecasting cancer risk.'

@app.route("/api", methods=['POST'])
def api():
    ipts = request.get_json()
    new_obs_df = process_ipt(ipts)
    prediction = "NA"
    if request.headers['Content-Type'] == 'application/json':
        if any([new_obs_df[i][0]==0 for i in num_cols]) or any([new_obs_df[i][0]=='' for i in cate_cols]):
            status_code = 406
            prediction = "Incomplete Inputs. Quantifying cancer risk requires all fields are correctly recorded."
        try:
            prediction = unit_prediction(new_obs_df)
            status_code = 200
        except Exception as e:
            print(e)
            status_code = 400
    opt = {"Forecasted Risk": f"{prediction}"}
    return make_response(jsonify(opt), status_code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)