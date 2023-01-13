# Cancer Risk Exploration

## Deliverable
- RestAPI
```bash
curl --location --request POST 'https://cancer-risk-regressor-4hw2x3sloq-as.a.run.app/api' --header 'Content-Type: application/json' --data-raw '{"Sex":"F","Age":"37.10","Smoking":"former","BMI":28.80,"Heart rate data used":0.0,"MET (activity level)":50.08}'
```

## Usage
## installation (assumed in a [conda] virtual env)
```bash
pip install -r requirements.tx
```

## Model Playground
- [ML](code/disease_explorative_study.ipynb)


## Launch app locally using Gunicorn
```bash
gunicorn -w 2 app:app -b localhost:8000
```

## Docker Build
```bash
docker build --rm -t cancer_risk_regressor:v0 . #use buildx build --platform linux/amd64 for mac m1 in order to deploy to cloud
docker run -d -p 8000:8080 cancer_risk_regressor:v0
```