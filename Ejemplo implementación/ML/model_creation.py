import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import joblib

df = pd.read_csv("datos.csv")

df = df.drop(columns=["EmployeeNumber"])

X = df.drop(columns=["Attrition"])
y = df["Attrition"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

X_train, X_test = X_train.align(X_test, join="left", axis=1)

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

joblib.dump(model, "GaussianNB_model.joblib")