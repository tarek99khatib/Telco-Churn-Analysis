PROJECT OVERVIEW - 
This project analyzes customer churn patterns using the Telco Customer Churn dataset.
The goal is to clean the data, generate Key Performance Indicators (KPIs), and perform Exploratory Data Analysis (EDA) to uncover insights about customer behavior and churn rates.


DATASET -
Source: Kaggle - Telco Customer Churn
Rows: ~7,000 customers
Key Columns:
	•	Churn – Whether the customer left the company
	•	tenure – Number of months the customer has stayed
	•	MonthlyCharges – The amount charged per month
	•	TotalCharges – Total amount charged
	•	Service-related columns: StreamingMovies, StreamingTV, InternetService, etc.


KPIs -
Metric,Value
Total Customers,7043.0
Churned Customers,1869.0
Churn Rate (%),26.54
Avg MonthlyCharges (Churn=Yes),74.44
Avg MonthlyCharges (Churn=No),61.27
Avg Tenure (Churn=Yes),17.98
Avg Tenure (Churn=No),37.57


Key Insights - 
1. Customers with month-to-month contracts have the highest churn rate.
2. Customers who pay by Electronic Check are more likely to churn than those paying via credit card or bank transfer.
3. Higher MonthlyCharges are correlated with a higher probability of churn.
4. Shorter tenure is strongly associated with churn.
5. Fiber optic internet customers show higher churn rates compared to DSL customers.

Tech Stack
	•	Python (Pandas, NumPy, Matplotlib, Seaborn)
	•	Data Cleaning & Processing
	•	Exploratory Data Analysis (EDA)
	•	KPI Reporting