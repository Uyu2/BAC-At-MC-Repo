# -*- coding: utf-8 -*-
"""Just_Ridge_and_Lasso-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wGVpFMt7kNKj0GWPPdsn_cMujxYRHfSB
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import RFE, VarianceThreshold
from sklearn.linear_model import LogisticRegression, Lasso, Ridge
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA

"""### Instantiate the datasets we will use"""

data_cr_2015 = pd.read_csv("2015_CostReport.csv", encoding="latin_1", low_memory=False)
data_cr_2016 = pd.read_csv("2016_CostReport.csv", encoding="latin_1", low_memory=False)
data_cr_2017 = pd.read_csv("2017_CostReport.csv", encoding="latin_1", low_memory=False)
data_cr_2018 = pd.read_csv("2018_CostReport.csv", encoding="latin_1", low_memory=False)
data_cr_2019 = pd.read_csv("2019_CostReport.csv", encoding="latin_1", low_memory=False)
data_cr_2020 = pd.read_csv("2020_CostReport.csv", encoding="latin_1", low_memory=False)

"""### Drop columns and rows that have too many null values"""

data_cr_2015.dropna(thresh=len(data_cr_2015.columns)*0.8, inplace=True)
data_cr_2015.dropna(axis=1, thresh=len(data_cr_2015)*0.75, inplace=True)

data_cr_2016.dropna(thresh=len(data_cr_2016.columns)*0.8, inplace=True)
data_cr_2016.dropna(axis=1, thresh=len(data_cr_2016)*0.75, inplace=True)

data_cr_2017.dropna(thresh=len(data_cr_2017.columns)*0.8, inplace=True)
data_cr_2017.dropna(axis=1, thresh=len(data_cr_2017)*0.75, inplace=True)

data_cr_2018.dropna(thresh=len(data_cr_2018.columns)*0.8, inplace=True)
data_cr_2018.dropna(axis=1, thresh=len(data_cr_2018)*0.75, inplace=True)

data_cr_2019.dropna(thresh=len(data_cr_2019.columns)*0.8, inplace=True)
data_cr_2019.dropna(axis=1, thresh=len(data_cr_2019)*0.75, inplace=True)

data_cr_2020.dropna(thresh=len(data_cr_2020.columns)*0.8, inplace=True)
data_cr_2020.dropna(axis=1, thresh=len(data_cr_2020)*0.75, inplace=True)

"""### Drop all non-essential object and int columns such as Facility Name, City, Fiscal Year dates, etc."""

columns_to_drop = ['Facility_Name', 'Street_Address', 'City', 'Medicare_CBSA_Number', 'Fiscal_Year_Begin_Date',
                   'Fiscal_Year_End_Date', 'Type_of_Control']

data_cr_2015.drop(columns=columns_to_drop, axis=1, inplace=True)
data_cr_2016.drop(columns=columns_to_drop, axis=1, inplace=True)
data_cr_2017.drop(columns=columns_to_drop, axis=1, inplace=True)
data_cr_2018.drop(columns=columns_to_drop, axis=1, inplace=True)
data_cr_2019.drop(columns=columns_to_drop, axis=1, inplace=True)
data_cr_2020.drop(columns=['Facility Name', 'Street Address', 'City', 'Medicare CBSA Number', 'Fiscal Year Begin Date',
                           'Fiscal Year End Date', 'Type of Control'], axis=1, inplace=True)

"""### Understand and fill all numerical and text columns with missing vals with either Median or Mode for the col"""

data_cr_2020.isna().mean().sort_values(ascending=False).head(20)

columns = ['Other_current_liabilities', 'SNF_Admissions_Title_XIX', 'SNF_Average_Length_stay_XIX',
         'SNF_Discharges_Title_XIX', 'Total_Discharges_Title_XIX', 'SNF_Days_Title_XIX',
         'Total_Days_Title_XIX', 'Salaries_wages_and_fees_payable', 'Less_discounts_on_patients', 'Total_fixed_Assets',
         'Accounts_Receivable', 'Cash_on_hand_and_in_banks', 'SNF_Admissions_Other', 'Accounts_payable',
         'SNF_Discharges_Title_Other', 'Total_Discharges_Title_Other', 'SNF_Days_Other', 'SNF_Admissions_Title_XVIII',
         'Wage_related_Costs_core', 'SNF_Admissions_Total', 'Total_current_liabilities', 'Total_liabilities', 'Net_Income',
         'SNF_Average_Length_stay_XVIII', 'Total_Income', 'SNF_Discharges_Title_XVIII', 'Total_current_assets',
         'Total_Days_Other', 'SNF_Number_of_beds', 'Total_fund_balances', 'General_fund_balance', 'Total_Bed_Days_Available',
         'SNF_bed_Days_Available', 'Number_of_Beds', 'Inpatient_PPS_Amount', 'Total_Costs', 'Total_RUG_Days',
         'Total_Days_Title_XVIII', 'Total_Discharges_Title_XVIII', 'SNF_Days_Title_XVIII', 'Net_Income_from_patients',
         'Total_General_Inpatient_Revenue', 'SNF_Discharges_Total', 'SNF_Average_Length_of_stay_Tot',
         'Total_Liab_and_fund_balances', 'Inpatient_Revenue', 'Gross_Revenue', 'Total_Assets', 'Net_Patient_Revenue',
         'Total_Discharges_Total']

for year in range(2015, 2020):
    data_cr_year = globals()[f"data_cr_{year}"]
    medians = data_cr_year[columns].median()
    modes = data_cr_year['Rural_versus_Urban'].mode()[0]
    data_cr_year.loc[:, columns] = data_cr_year[columns].fillna(medians)
    data_cr_year.loc[:, 'Rural_versus_Urban'] = data_cr_year['Rural_versus_Urban'].fillna(modes)

columns_2020 = ['Notes and Loans Payable (short term)', 'Other Assets', 'Less: Allowances for uncollectible notes and accounts receivable',
                'Land', 'Payroll taxes payable', 'Total other Assets', 'Major movable equipment', 'Land improvements', 'SNF Discharges Title Other',
                'SNF Admissions Title XIX', 'Contract Labor', "Less Contractual Allowance and discounts on patients' accounts", "Accounts payable"]
median = data_cr_2020[columns_2020].median()
mode = data_cr_2020['Rural versus Urban'].mode()[0]
data_cr_2020.loc[:, columns_2020] = data_cr_2020[columns_2020].fillna(median)
data_cr_2020.loc[:, 'Rural versus Urban'] = data_cr_2020['Rural versus Urban'].fillna(mode)

"""### Encode all of the text columns (one-hot for columns with less than 5 unique values and label for any other text columns)"""

cols = ['State_Code', 'Zip_Code', 'County']
data_cr_years = [data_cr_2015, data_cr_2016, data_cr_2017, data_cr_2018, data_cr_2019]

for data_cr_year in data_cr_years:
    for col in cols:
        data_cr_year[f'{col}'] = data_cr_year[f'{col}'].astype('category')
        data_cr_year[f'{col}-coded'] = data_cr_year[f'{col}'].cat.codes
        data_cr_year.drop(f'{col}', axis=1, inplace=True)

for i in range(len(data_cr_years)):
    dummies = pd.get_dummies(data_cr_years[i]['Rural_versus_Urban'], prefix='Rural_versus_Urban', drop_first=True)
    data_cr_years[i] = pd.concat([data_cr_years[i], dummies], axis=1)
    data_cr_years[i].drop('Rural_versus_Urban', axis=1, inplace=True)

data_cr_2015, data_cr_2016, data_cr_2017, data_cr_2018, data_cr_2019 = data_cr_years

cols_2020 = ['State Code', 'Zip Code', 'County']
for col in cols_2020:
    data_cr_2020[f'{col}'] = data_cr_2020[f'{col}'].astype('category')
    data_cr_2020[f'{col}-coded'] = data_cr_2020[f'{col}'].cat.codes
    data_cr_2020.drop(f'{col}', axis=1, inplace=True)

data_cr_2020 = pd.get_dummies(data_cr_2020, columns=['Rural versus Urban'], drop_first=True)

"""### Take care of multicoliniarity between X columns"""

y_2015 = data_cr_2015['Net_Income']
y_2016 = data_cr_2016['Net_Income']
y_2017 = data_cr_2017['Net_Income']
y_2018 = data_cr_2018['Net_Income']
y_2019 = data_cr_2019['Net_Income']
y_2020 = data_cr_2020['Net Income']

X_2015 = data_cr_2015.drop(['Net_Income', 'Total_Income', 'Total_Costs', 'Net_Income_from_patients', 'Net_Patient_Revenue',
                       'Less_Total_Operating_Expense'], axis=1)
X_2016 = data_cr_2016.drop(['Net_Income', 'Total_Income', 'Total_Costs', 'Net_Income_from_patients', 'Net_Patient_Revenue',
                       'Less_Total_Operating_Expense'], axis=1)
X_2017 = data_cr_2017.drop(['Net_Income', 'Total_Income', 'Total_Costs', 'Net_Income_from_patients', 'Net_Patient_Revenue',
                       'Less_Total_Operating_Expense'], axis=1)
X_2018 = data_cr_2018.drop(['Net_Income', 'Total_Income', 'Total_Costs', 'Net_Income_from_patients', 'Net_Patient_Revenue',
                       'Less_Total_Operating_Expense'], axis=1)
X_2019 = data_cr_2019.drop(['Net_Income', 'Total_Income', 'Total_Costs', 'Net_Income_from_patients', 'Net_Patient_Revenue',
                       'Less_Total_Operating_Expense'], axis=1)
X_2020 = data_cr_2020.drop(['Net Income', 'Total Income', 'Total Costs', 'Net Income from service to patients', 'Net Patient Revenue',
                       'Less Total Operating Expense'], axis=1)

scaler = StandardScaler()
X_2015_scaled = scaler.fit_transform(X_2015)
X_2016_scaled = scaler.fit_transform(X_2016)
X_2017_scaled = scaler.fit_transform(X_2017)
X_2018_scaled = scaler.fit_transform(X_2018)
X_2019_scaled = scaler.fit_transform(X_2019)
X_2020_scaled = scaler.fit_transform(X_2020)

scaled_datasets = [X_2015_scaled, X_2016_scaled, X_2017_scaled, X_2018_scaled, X_2019_scaled, X_2020_scaled]
years = [2015, 2016, 2017, 2018, 2019, 2020]
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
fig.subplots_adjust(hspace=0.5, wspace=0.3)

for ax, dataset, year in zip(axes.flatten(), scaled_datasets, years):
    pca = PCA(n_components=None)
    pca.fit_transform(dataset)
    cum_explained_variance = np.cumsum(pca.explained_variance_ratio_)
    ax.plot(cum_explained_variance)
    ax.set_title(f'{year} Cumulative Explained Variance')
    ax.set_xlabel('Number of Components')
    ax.set_ylabel('Cumulative Explained Variance')
    ax.grid(True)

plt.show()

def preprocess_data(data, year):
    X = data
    selector = VarianceThreshold(threshold=3)
    selector.fit_transform(X)
    X_var_df = X[selector.feature_names_in_]
    return X_var_df


def remove_collinearity(data, threshold=0.75):
    corr_matrix = data.corr().abs()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    tri_df = corr_matrix.mask(mask)
    to_drop = [c for c in tri_df.columns if any(tri_df[c] > threshold)]
    reduced_df = data.drop(to_drop, axis=1)
    return reduced_df

X_2015_corr = remove_collinearity(X_2015)
X_2016_corr = remove_collinearity(X_2016)
X_2017_corr = remove_collinearity(X_2017)
X_2018_corr = remove_collinearity(X_2018)
X_2019_corr = remove_collinearity(X_2019)
X_2020_corr = remove_collinearity(X_2020)

X_2015_corr_var = preprocess_data(X_2015_corr, 2015)
X_2016_corr_var = preprocess_data(X_2016_corr, 2016)
X_2017_corr_var = preprocess_data(X_2017_corr, 2017)
X_2018_corr_var = preprocess_data(X_2018_corr, 2018)
X_2019_corr_var = preprocess_data(X_2019_corr, 2019)
X_2020_corr_var = preprocess_data(X_2020_corr, 2020)


X_train1, X_test1, y_train1, y_test1 = train_test_split(X_2015_corr_var, y_2015, test_size=0.3, random_state=90)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_2016_corr_var, y_2016, test_size=0.3, random_state=90)
X_train3, X_test3, y_train3, y_test3 = train_test_split(X_2017_corr_var, y_2017, test_size=0.3, random_state=90)
X_train4, X_test4, y_train4, y_test4 = train_test_split(X_2018_corr_var, y_2018, test_size=0.3, random_state=90)
X_train5, X_test5, y_train5, y_test5 = train_test_split(X_2019_corr_var, y_2019, test_size=0.3, random_state=90)
X_train6, X_test6, y_train6, y_test6 = train_test_split(X_2020_corr_var, y_2020, test_size=0.3, random_state=90)

"""### Just Ridge and Lasso 😎"""

scaler = StandardScaler()
X_train_scaled1 = scaler.fit_transform(X_train1)
X_test_scaled1 = scaler.transform(X_test1)
X_train_scaled2 = scaler.fit_transform(X_train2)
X_test_scaled2 = scaler.transform(X_test2)
X_train_scaled3 = scaler.fit_transform(X_train3)
X_test_scaled3 = scaler.transform(X_test3)
X_train_scaled4 = scaler.fit_transform(X_train4)
X_test_scaled4 = scaler.transform(X_test4)
X_train_scaled5 = scaler.fit_transform(X_train5)
X_test_scaled5 = scaler.transform(X_test5)
X_train_scaled6 = scaler.fit_transform(X_train6)
X_test_scaled6 = scaler.transform(X_test6)

X_train_scaled1.shape

RModel = Ridge()
Rparam_grid = {'alpha': (0.1, 0.5, 1, 5, 10, 25, 50, 100)}

Rgrid_search1 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search1.fit(X_train_scaled1, y_train1)
print("Train and Test Scores:", Rgrid_search1.score(X_train_scaled1, y_train1), Rgrid_search1.score(X_test_scaled1, y_test1))

Rgrid_search2 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search2.fit(X_train_scaled2, y_train2)
print("Train and Test Scores:", Rgrid_search2.score(X_train_scaled2, y_train2), Rgrid_search2.score(X_test_scaled2, y_test2))

Rgrid_search3 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search3.fit(X_train_scaled3, y_train3)
print("Train and Test Scores:", Rgrid_search3.score(X_train_scaled3, y_train3), Rgrid_search3.score(X_test_scaled3, y_test3))

Rgrid_search4 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search4.fit(X_train_scaled4, y_train4)
print("Train and Test Scores:", Rgrid_search4.score(X_train_scaled4, y_train4), Rgrid_search4.score(X_test_scaled4, y_test4))

Rgrid_search5 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search5.fit(X_train_scaled5, y_train5)
print("Train and Test Scores:", Rgrid_search5.score(X_train_scaled5, y_train5), Rgrid_search5.score(X_test_scaled5, y_test5))

Rgrid_search6 = GridSearchCV(RModel, Rparam_grid, n_jobs=-1, cv=6, scoring='r2')
Rgrid_search6.fit(X_train_scaled6, y_train6)
print("Train and Test Scores:", Rgrid_search6.score(X_train_scaled6, y_train6), Rgrid_search6.score(X_test_scaled6, y_test6))

LModel = Lasso(max_iter=2500)
Lparam_grid = {'alpha': [0.001, 0.005, 0.01, 0.05, 0.1, 0.025, 0.05, 1]}

Lgrid_search1 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search1.fit(X_train_scaled1, y_train1)
print("Train and Test Scores:", Lgrid_search1.score(X_train_scaled1, y_train1), Lgrid_search1.score(X_test_scaled1, y_test1))

Lgrid_search2 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search2.fit(X_train_scaled2, y_train2)
print("Train and Test Scores:", Lgrid_search2.score(X_train_scaled2, y_train2), Lgrid_search2.score(X_test_scaled2, y_test2))

Lgrid_search3 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search3.fit(X_train_scaled3, y_train3)
print("Train and Test Scores:", Lgrid_search3.score(X_train_scaled3, y_train3), Lgrid_search3.score(X_test_scaled3, y_test3))

Lgrid_search4 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search4.fit(X_train_scaled4, y_train4)
print("Train and Test Scores:", Lgrid_search4.score(X_train_scaled4, y_train4), Lgrid_search4.score(X_test_scaled4, y_test4))

Lgrid_search5 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search5.fit(X_train_scaled5, y_train5)
print("Train and Test Scores:", Lgrid_search5.score(X_train_scaled5, y_train5), Lgrid_search5.score(X_test_scaled5, y_test5))

Lgrid_search6 = GridSearchCV(LModel, Lparam_grid, n_jobs=-1, cv=10, scoring='r2')
Lgrid_search6.fit(X_train_scaled6, y_train6)
print("Train and Test Scores:", Lgrid_search6.score(X_train_scaled6, y_train6), Lgrid_search6.score(X_test_scaled6, y_test6))

def features_to_keep(coefficients, threshold=0):
    return np.abs(coefficients) > threshold

ridge1_features_to_keep = features_to_keep(Rgrid_search1.best_estimator_.coef_)
lasso1_features_to_keep = features_to_keep(Lgrid_search1.best_estimator_.coef_)
ridge2_features_to_keep = features_to_keep(Rgrid_search2.best_estimator_.coef_)
lasso2_features_to_keep = features_to_keep(Lgrid_search2.best_estimator_.coef_)
ridge3_features_to_keep = features_to_keep(Rgrid_search3.best_estimator_.coef_)
lasso3_features_to_keep = features_to_keep(Lgrid_search3.best_estimator_.coef_)
ridge4_features_to_keep = features_to_keep(Rgrid_search4.best_estimator_.coef_)
lasso4_features_to_keep = features_to_keep(Lgrid_search4.best_estimator_.coef_)
ridge5_features_to_keep = features_to_keep(Rgrid_search5.best_estimator_.coef_)
lasso5_features_to_keep = features_to_keep(Lgrid_search5.best_estimator_.coef_)
ridge6_features_to_keep = features_to_keep(Rgrid_search6.best_estimator_.coef_)
lasso6_features_to_keep = features_to_keep(Lgrid_search6.best_estimator_.coef_)

ridge1_coefficients = Rgrid_search1.best_estimator_.coef_[ridge1_features_to_keep]
keep_features = X_2015_corr_var.loc[:, ridge1_features_to_keep]
feature_names1 = keep_features.columns
sorted_idx = np.argsort(ridge1_coefficients)[::-1]
sorted_feature_names = feature_names1[sorted_idx]
sorted_coefficients = ridge1_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2015 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

ridge2_coefficients = Rgrid_search2.best_estimator_.coef_[ridge2_features_to_keep]
keep_features = X_2016_corr_var.loc[:, ridge2_features_to_keep]
feature_names2 = keep_features.columns
sorted_idx = np.argsort(ridge2_coefficients)[::-1]
sorted_feature_names = feature_names2[sorted_idx]
sorted_coefficients = ridge2_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2016 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

ridge3_coefficients = Rgrid_search3.best_estimator_.coef_[ridge3_features_to_keep]
keep_features = X_2017_corr_var.loc[:, ridge3_features_to_keep]
feature_names3 = keep_features.columns
sorted_idx = np.argsort(ridge3_coefficients)[::-1]
sorted_feature_names = feature_names3[sorted_idx]
sorted_coefficients = ridge3_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2017 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

ridge4_coefficients = Rgrid_search4.best_estimator_.coef_[ridge4_features_to_keep]
keep_features = X_2018_corr_var.loc[:, ridge4_features_to_keep]
feature_names4 = keep_features.columns
sorted_idx = np.argsort(ridge4_coefficients)[::-1]
sorted_feature_names = feature_names4[sorted_idx]
sorted_coefficients = ridge4_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2018 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

ridge5_coefficients = Rgrid_search5.best_estimator_.coef_[ridge5_features_to_keep]
keep_features = X_2019_corr_var.loc[:, ridge5_features_to_keep]
feature_names5 = keep_features.columns
sorted_idx = np.argsort(ridge5_coefficients)[::-1]
sorted_feature_names = feature_names5[sorted_idx]
sorted_coefficients = ridge5_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2019 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

ridge6_coefficients = Rgrid_search6.best_estimator_.coef_[ridge6_features_to_keep]
keep_features = X_2020_corr_var.loc[:, ridge6_features_to_keep]
feature_names6 = keep_features.columns
sorted_idx = np.argsort(ridge6_coefficients)[::-1]
sorted_feature_names = feature_names6[sorted_idx]
sorted_coefficients = ridge6_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Ridge')
plt.xticks(rotation=90)
plt.title("Cost Report 2020 Ridge Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso1_coefficients = Lgrid_search1.best_estimator_.coef_[lasso1_features_to_keep]
keep_features = X_2015_corr_var.loc[:, lasso1_features_to_keep]
feature_names1 = keep_features.columns
sorted_idx = np.argsort(lasso1_coefficients)[::-1]
sorted_feature_names = feature_names1[sorted_idx]
sorted_coefficients = lasso1_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2015 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso2_coefficients = Lgrid_search2.best_estimator_.coef_[lasso2_features_to_keep]
keep_features = X_2016_corr_var.loc[:, lasso2_features_to_keep]
feature_names2 = keep_features.columns
sorted_idx = np.argsort(lasso2_coefficients)[::-1]
sorted_feature_names = feature_names2[sorted_idx]
sorted_coefficients = lasso2_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2016 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso3_coefficients = Lgrid_search3.best_estimator_.coef_[lasso3_features_to_keep]
keep_features = X_2017_corr_var.loc[:, lasso3_features_to_keep]
feature_names3 = keep_features.columns
sorted_idx = np.argsort(lasso3_coefficients)[::-1]
sorted_feature_names = feature_names3[sorted_idx]
sorted_coefficients = lasso3_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2017 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso4_coefficients = Lgrid_search4.best_estimator_.coef_[lasso4_features_to_keep]
keep_features = X_2018_corr_var.loc[:, lasso4_features_to_keep]
feature_names4 = keep_features.columns
sorted_idx = np.argsort(lasso4_coefficients)[::-1]
sorted_feature_names = feature_names4[sorted_idx]
sorted_coefficients = lasso4_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2018 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso5_coefficients = Lgrid_search5.best_estimator_.coef_[lasso5_features_to_keep]
keep_features = X_2019_corr_var.loc[:, lasso5_features_to_keep]
feature_names5 = keep_features.columns
sorted_idx = np.argsort(lasso5_coefficients)[::-1]
sorted_feature_names = feature_names5[sorted_idx]
sorted_coefficients = lasso5_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2019 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

lasso6_coefficients = Lgrid_search6.best_estimator_.coef_[lasso6_features_to_keep]
keep_features = X_2020_corr_var.loc[:, lasso6_features_to_keep]
feature_names6 = keep_features.columns
sorted_idx = np.argsort(lasso6_coefficients)[::-1]
sorted_feature_names = feature_names6[sorted_idx]
sorted_coefficients = lasso6_coefficients[sorted_idx]

plt.figure(figsize=(15, 6))
plt.bar(sorted_feature_names, sorted_coefficients, label='Lasso')
plt.xticks(rotation=90)
plt.title("Cost Report 2020 Lasso Feature Importances")
plt.ylabel('Coefficient Value')
plt.xlabel('Feature')
plt.legend()
plt.show()

print("The Ridge best parameters are: ", Rgrid_search1.best_params_)
print("The Ridge best score is: ", Rgrid_search1.best_score_)
print("The Ridge test set R^2 score is: ", Rgrid_search1.score(X_test_scaled1, y_test1))

print("The Lasso best parameters are: ", Lgrid_search1.best_params_)
print("The Lasso best score is: ", Lgrid_search1.best_score_)
print("The Lasso test set R^2 score is: ", Lgrid_search1.score(X_test_scaled1, y_test1))