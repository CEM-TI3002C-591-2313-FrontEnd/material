import joblib

model = joblib.load("GaussianNB_model.joblib")

print(model.feature_names_in_)