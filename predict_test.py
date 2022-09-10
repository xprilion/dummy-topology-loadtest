import requests

candidate = [{
    "gender": "M",
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


url = "http://0.0.0.0:8000/predict"
result = requests.post(url=url,json=candidate).json()
print('The Model Prediction for placement :',result)


# https://dphi.tech/challenges/data-sprint-42-campus-recruitment/146/data
"""
gender: Gender of the candidate (male/female)
ssc_b: senior secondary board
ssc_p: senior secondary percentage scored
hsc_b: higher secondary board
hsc_p: higher secondary percentage scored
hsc_s: higher secondary subject
degree_p: percentage scored in degree/graduation
etest_p: entrance test percentage scored
mba_p: mba percentage scored
specialization: mba specialization
workex: work experience
status: placed or not placed (target variable)
"""