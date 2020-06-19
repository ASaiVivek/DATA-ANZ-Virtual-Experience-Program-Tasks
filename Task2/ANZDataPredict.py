import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

df = pd.read_excel("ANZ synthesised transaction dataset.xlsx")

# Modifying data to obtain salaries for each customer
# Amount column shows annual salary
df_salaries = df[df["txn_description"] == "PAY/SALARY"].groupby("customer_id").sum()*4

salaries = []
for customer_id in df["customer_id"]:
    salaries.append(int(df_salaries.loc[customer_id]["amount"]))
df["annual_salary"] = salaries

df_cus = df.groupby("customer_id").mean()
print("Mean annual salary by customer: ")
print(df_cus.head(), "\n")

#df_ages=df_salaries.groupby('age').mean()
#df_avg_sal=df_cus["annual_salary"]groupby('age').mean()

#mean annual salary by age
df_avg_sal=df_cus.groupby("age").agg({'annual_salary':'mean'})

#annual spendings by customers
df_spendings=df[df["movement"]=="debit"].groupby("customer_id").sum()*4

spendings=[]
for customer_id in df["customer_id"]:
    spendings.append(int(df_spendings.loc[customer_id]["amount"]))
df["annual_spending"]=spendings

df_cus_spending=df.groupby("customer_id").mean()
print("Mean annual spending by customer: ")
print(df_cus_spending.head(),"\n")

#mean annual spending by age
df_avg_spending=df_cus_spending.groupby('age').agg({'annual_spending':'mean'})

#print(df_avg_sal[0])

#print(df_avg_sal.head(),"\n")
#print(df_ages.head(),"\n")
#plotting average annual salary by age
fig=plt.figure()
plt.scatter(df_cus["age"].unique(),df_avg_sal,c="green",label="Average Annual Salary")
plt.title("ANZ Customer's Average Annual Salary v/s Age")
plt.xlabel("Age(years)")
plt.ylabel("Annual Salary AUD($)")
plt.legend()
plt.tight_layout()
fig.savefig('avg_sal_age.png')

#plotting average annual spendings by Age
fig=plt.figure()
plt.scatter(df_cus_spending["age"].unique(),df_avg_spending,c="red",label="Average Annual Spendings")
plt.title("ANZ Customer's Average Annual Spendings v/s Age")
plt.xlabel("Age(years)")
plt.ylabel("Annual Spending AUD($)")
plt.legend()
plt.tight_layout()
fig.savefig('avg_spend_age.png')

# PREDICTIVE ANALYTICS:
print("REGRESSION:\n")
N_train = int(len(df_cus)*0.8)
X_train = df_cus.drop("annual_salary", axis=1).iloc[:N_train]
Y_train = df_cus["annual_salary"].iloc[:N_train]
X_test = df_cus.drop("annual_salary", axis=1).iloc[N_train:]
Y_test = df_cus["annual_salary"].iloc[N_train:]

regression_model = LinearRegression()
regression_model.fit(X_train, Y_train)
print(f"Linear Regression Training Score: {regression_model.score(X_train, Y_train)}\n")

print("Predictions using test data:")
print(regression_model.predict(X_test), "\n")

print(f"Linear Regression Testing Score: {regression_model.score(X_test, Y_test)}\n")
#print(f"Liner Regression Accuracy: {accuracy_score(Y_test,regression_model.predict(X_test))}\n")

# Categorical columns
df_category = df[["txn_description", "gender", "age", "merchant_state", "movement"]]
# Changing all categories to dummies
pd.get_dummies(df_category).head()

N_train = int(len(df)*0.8)
X_train = pd.get_dummies(df_category).iloc[:N_train]
Y_train = df["annual_salary"].iloc[:N_train]
X_test = pd.get_dummies(df_category).iloc[N_train:]
Y_test = df["annual_salary"].iloc[N_train:]

#DecisionTree Regression
print("Decision Tree:\n")
decision_tree_regression = DecisionTreeRegressor()
decision_tree_regression.fit(X_train, Y_train)
print(f"Decision Tree Regressor Training Score: {decision_tree_regression.score(X_train, Y_train)}\n")

print("Predictions using test data:")
print(decision_tree_regression.predict(X_test), "\n")

print(f"Decision Tree Regressor Testing Score: {decision_tree_regression.score(X_test, Y_test)}\n")
#print(f"Decision Tree Regressor Accuracy: {accuracy_score(Y_test,decision_tree_regression.predict(X_test))}\n")
