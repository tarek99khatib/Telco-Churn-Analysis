import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#ــــــــ This script is for cleaning the Telco Customer Churn dataset ــــــــ# 

# Load the dataset, and print the first few rows and info, to check the data.
df = pd.read_csv("telco_churn_analysis/data/raw/Telco-customer-Churn.csv")
print(df.head())
print(df.info()) 
# there is contradictory information in the dataset,
# such as 'TotalCharges' being an object type but containing numeric values.


# Check for missing values in the dataset.
print(df.isnull().sum())

# cleaning the data, 'TotalCharges' should be numeric, but it is an object type.
# Convert 'TotalCharges' to numeric, forcing errors to NaN.
# replace NaN values with the mean of the column.
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].mean(), inplace=True)
# Check again for missing values after cleaning.
print(df.isnull().sum())

# Now, we can check the data types of the columns again.
print(df.dtypes)
print(df.head())


# change 'SeniorCitizen' to a Yes/No.
# check the unique values in 'SeniorCitizen'.
print(df['SeniorCitizen'].unique())
# replace 0 with 'No' and 1 with 'Yes'.
df['SeniorCitizen'] = df['SeniorCitizen'].replace({0: 'No', 1: 'Yes'})

# check the unique values in 'SeniorCitizen'.
print(df['SeniorCitizen'].unique())

# Now, we can check the data types of the columns again.
print(df.dtypes)
print(df.head())

# removing any unnecessary spacing.
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# saving the cleaned data to a new CSV file.
df.to_csv("telco_churn_analysis/data/processed/telco_churn_clean.csv", index=False)


# ------ KPI Analysis ------ #

total_customers = len(df)
churned_customers = df['Churn'].value_counts().get('Yes', 0)
churn_rate = round((churned_customers / total_customers) * 100, 2)

avg_monthly_yes = df[df['Churn'] == 'Yes']['MonthlyCharges'].mean()
avg_monthly_no = df[df['Churn'] == 'No']['MonthlyCharges'].mean()

avg_tenure_yes = df[df['Churn'] == 'Yes']['tenure'].mean()
avg_tenure_no = df[df['Churn'] == 'No']['tenure'].mean()

kpis = pd.DataFrame({
    'Metric': ['Total Customers', 'Churned Customers', 'Churn Rate (%)',
               'Avg MonthlyCharges (Churn=Yes)', 'Avg MonthlyCharges (Churn=No)',
               'Avg Tenure (Churn=Yes)', 'Avg Tenure (Churn=No)'],
    'Value': [total_customers, churned_customers, churn_rate,
              round(avg_monthly_yes, 2), round(avg_monthly_no, 2),
              round(avg_tenure_yes, 2), round(avg_tenure_no, 2)]
})

kpis.to_csv("telco_churn_analysis/data/processed/kpis.csv", index=False)

# Pivot table to analyze contract type and churn.
pivot_contract = pd.crosstab(df['Contract'], df['Churn'], normalize='index')*100
pivot_contract=pivot_contract.round(2)  # rounding to 2 decimal places
pivot_contract.to_csv("telco_churn_analysis/data/processed/pivot_contract_churn.csv")

# Pivot table to analyze Streaming TV and churn.  
pivot_streaming_tv = pd.crosstab(df['StreamingTV'], df['Churn'], normalize='index')*100
pivot_streaming_tv= pivot_streaming_tv.round(2)  # rounding to 2 decimal places
pivot_streaming_tv.to_csv("telco_churn_analysis/data/processed/pivot_streaming_tv_churn.csv")

# Pivot table to analyze Streaming Movies and churn.
pivot_streaming_movies = pd.crosstab(df['StreamingMovies'], df['Churn'], normalize='index')*100
pivot_streaming_movies=pivot_streaming_movies.round(2)  # rounding to 2 decimal places
pivot_streaming_movies.to_csv("telco_churn_analysis/data/processed/pivot_streaming_movies_churn.csv")

# Pivot table to analyze Internet Service and churn.
pivot_internet_service = pd.crosstab(df['InternetService'], df['Churn'], normalize='index')*100
pivot_internet_service=pivot_internet_service.round(2)  # rounding to 2 decimal places
pivot_internet_service.to_csv("telco_churn_analysis/data/processed/pivot_internet_service_churn.csv")

# Pivot table to analyze PaymentMetod and churn.
pivot_payment_method = pd.crosstab(df['PaymentMethod'], df['Churn'], normalize='index')*100
pivot_payment_method=pivot_payment_method.round(2)  # rounding to 2 decimal places
pivot_payment_method.to_csv("telco_churn_analysis/data/processed/pivot_payment_method_churn.csv") # we can see that customers who pay by electronic check have a higher churn rate.


# now, EDA can be performed on the cleaned data.
summary = df.describe() # descriptive statistics of the dataset.
print(summary)
summary.to_csv("telco_churn_analysis/data/processed/telco_churn_summary.csv", index=False)

summary_str =df.describe(include='object') # descriptive statistics of the object type columns.
print(summary_str)
summary_str.to_csv("telco_churn_analysis/data/processed/telco_churn_summary_str.csv", index=False)

# Visualizing the distribution of the 'Churn' column.
sns.countplot(x='Churn', data=df)
plt.title('Distribution of Churn')
plt.savefig("telco_churn_analysis/figures/churn_distribution.png")
plt.close()

# visualizing the distribution of 'tenure' column.
plt.figure(figsize=(10, 6))
sns.histplot(df['tenure'], bins=30, kde=True)
plt.title('Distribution of Tenure')
plt.xlabel('Tenure (Months)')
plt.ylabel('Frequency')
plt.savefig("telco_churn_analysis/figures/tenure_distribution.png")
plt.close() # we can see that most customers have a tenure of less than 30 months.

# Visualizing Contract Type vs Churn.
sns.countplot(x='Contract', hue='Churn', data=df)
plt.title('Contract Type vs Churn')
plt.savefig("telco_churn_analysis/figures/contract_vs_churn.png")
plt.close() # we can see that customers with month-to-month contracts have a higher churn rate.

#visualizing PaymentMethod vs Churn.
plt.figure(figsize=(6,6))
df[df['Churn'] == 'Yes']['PaymentMethod'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'black'}
)
plt.ylabel('')
plt.title('Payment Methods for Customers Who Churned')
plt.tight_layout()
plt.savefig("telco_churn_analysis/figures/payment_method_churn_yes.png")
plt.close() # we can see that customers who pay by electronic check have a higher churn rate.

# Visualizing Internet Service vs Churn.
pivot_internet_service.plot(
    kind='bar',
    stacked=True,
    figsize=(7,5),
)
plt.title('Churn Rate by Internet Service')
plt.ylabel('Percentage (%)')
plt.xlabel('Internet Service Type')
plt.legend(title='Churn')
plt.tight_layout()
plt.savefig("telco_churn_analysis/figures/internet_service_vs_churn.png")
plt.close() # we can see that customers with fiber optic internet service have a higher churn rate.

# Visualizing monthly charges vs Churn.
sns.boxplot(x='Churn', y='MonthlyCharges', data=df)
plt.title('Monthly Charges vs Churn')
plt.savefig("telco_churn_analysis/figures/monthly_charges_vs_churn.png")
plt.close()# we can see that customers with higher monthly charges have a higher churn rate.

# Visualizing Movies/TV vs Churn.
sns.countplot(x='StreamingMovies', hue='Churn', data=df)
plt.title('Churn Rate by Streaming Movies Subscription')
plt.savefig("telco_churn_analysis/figures/streaming_movies_vs_churn.png")
plt.close() 
sns.countplot(x='StreamingTV', hue='Churn', data=df)
plt.title('Churn Rate by StreamingTV Subscription')
plt.savefig("telco_churn_analysis/figures/streaming_tv_vs_churn.png")
plt.close()# we can see that customers who do not have an internet service have a lower churn rate.

#visualizing Senior Citizen vs Churn.
sns.countplot(x='SeniorCitizen', hue='Churn', data=df)
plt.title('Churn Rate by Senior Citizen Status')
plt.savefig("telco_churn_analysis/figures/senior_citizen_vs_churn.png") # we can see that senior citizens have a higher churn rate.
plt.close()

# Visualizing the distribution of 'TotalCharges'.
plt.figure(figsize=(10, 6))
sns.histplot(df['TotalCharges'], bins=30, kde=True)
plt.title('Distribution of Total Charges')
plt.xlabel('Total Charges')
plt.ylabel('Frequency')
plt.savefig("telco_churn_analysis/figures/total_charges_distribution.png")
plt.close() # we can see that the distribution is right-skewed, indicating that most customers have lower total charges.


####### Correlation Analysis ########
df['Churn_numeric'] = df['Churn'].apply(lambda x: 1 if x.strip().lower() == 'yes' else 0)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
corr = df[numeric_cols].corr()
plt.figure(figsize=(8,6))
heatmap = sns.heatmap(
    corr,
    annot=True,           
    fmt=".2f",             
    cmap="RdYlBu",        
    linewidths=0.5,        
    cbar_kws={'label': 'Correlation Coefficient'} 
)
plt.title("Correlation Heatmap (Numeric Features)", fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig("telco_churn_analysis/figures/correlation_heatmap.png", dpi=300)
plt.close() # we can see that 'Churn_numeric' has a strong positive correlation with 'MonthlyCharges' and 'TotalCharges', indicating that customers with higher monthly charges and total charges are more likely to churn.


