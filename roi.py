# -*- coding: utf-8 -*-
"""ROI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZFIPvuO4p8Gn_C8eZUl6si11Ge87aW8A

Combine Cost Report 2020 and Cost Report 2021 into one cost report, to measure end of year Shareholder's Equity, Purchase cost (as Assets + Liabilities), and to tell a story on the financials
"""

import pandas as pd

cr2 = pd.read_csv('cr2.csv')
cr3 = pd.read_csv('cr3.csv')

df = pd.concat([cr2, cr3], ignore_index=True)
df

"""From the big cost report, extrapolate the Provider CCN or Federally assigned number, state, ZIP, total assets, and total liabilities

Then sort based on the top 25 ZIP Codes in only the best performing states (Ohio, Colorado, New York, and California) returning the overall most reliable 139 nursing homes
"""

return_df = df[['Provider CCN', 'State Code', 'Zip Code', 'Total Assets', 'Total liabilities', 'Net Income']]
zip_code_list = ['11354', '94541', '92020', '44691', '95608', '10463', '92835', '92025', '90247', '44256', '44202', '95661', '80222', '80214']

best_zips = return_df[return_df['Zip Code'].isin(zip_code_list)].copy()
best_zips

"""Using Shareholder's Equity (Assets - Liabilities), or Net Asset Value as the investment value was because it is the total value of the nursing home if the assets and liabilities were liquidated. Essentially, it is everything left once the debts are paid off, or what the owner's value in the company actually is, so it is a baseline for what we would be paying as an investment to have the equal value of the current owner.

We then add a column to this dataframe to have this liquidated value as our base investment.
"""

best_zips['Liquidated Value'] = best_zips['Total Assets'] - best_zips['Total liabilities']
best_zips

"""ROI is calculated by dividing net income"""

best_zips['ROI'] = (best_zips['Net Income'] / best_zips['Liquidated Value'] * 100).round(0)
best_zips['ROA'] = (best_zips['Net Income'] / best_zips['Total Assets'] * 100).round(0)
best_zips

"""From the top 4 states and the top 25 ZIP Codes amongst them, this calculates how many nursing homes will have an ROI greater than 10%, or a "safe" annual investment, and an ROI greater than 30%, or a riskier annual investment. Clearly, across both categories, New York nursing homes have a high chance of being the most successful in their return on investment, especially while touting the greatest ratings."""

states = ['FL', 'NY']

data = []

for state in states:
    state_df = best_zips[best_zips['State Code'] == state]
    total_count = len(state_df)
    roi_gt_10_count = (state_df['ROI'] > 10).sum()
    roi_gt_30_count = (state_df['ROI'] > 30).sum()
    roa_gt_10_count = (state_df['ROA'] > 5).sum()
    roa_gt_30_count = (state_df['ROA'] > 20).sum()
    roi_gt_10_percentage = ((roi_gt_10_count / total_count) * 100).round(0) if total_count > 0 else 0
    roi_gt_30_percentage = ((roi_gt_30_count / total_count) * 100).round(0) if total_count > 0 else 0
    roa_gt_10_percentage = ((roa_gt_10_count / total_count) * 100).round(0) if total_count > 0 else 0
    roa_gt_30_percentage = ((roa_gt_30_count / total_count) * 100).round(0) if total_count > 0 else 0
    data.append((state, total_count, roi_gt_10_percentage, roi_gt_30_percentage, roa_gt_10_percentage, roa_gt_30_percentage))

roi_counts_df = pd.DataFrame(data, columns=['State', 'Total Facilities', 'ROI > 10%', 'ROI > 30%', 'ROA > 5%', 'ROA > 20%'])
percentage_columns = ['ROI > 10%', 'ROI > 30%', 'ROA > 5%', 'ROA > 20%']
roi_counts_df[percentage_columns] = roi_counts_df[percentage_columns].applymap(lambda x: "{:.0f}%".format(x))

roi_counts_df.sort_values(by = 'ROI > 10%', ascending = False)

d = df.copy()
d['Liquidated Value'] = d['Total Assets'] - d['Total liabilities']
d['ROI'] = (d['Net Income'] / d['Liquidated Value'] * 100).round(0)
d['ROA'] = (d['Net Income'] / d['Total Assets'] * 100).round(0)

state = ['FL', 'NY']

data = []

for stat in state:
    states_df = d[d['State Code'] == stat]
    total_coun = len(states_df)
    roi_gt_10_coun = (states_df['ROI'] > 10).sum()
    roi_gt_30_coun = (states_df['ROI'] > 30).sum()
    roi_gt_10_percentag = ((roi_gt_10_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roi_gt_30_percentag = ((roi_gt_30_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roa_gt_10_coun = (states_df['ROA'] > 10).sum()
    roa_gt_30_coun = (states_df['ROA'] > 30).sum()
    roa_gt_10_percentag = ((roa_gt_10_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roa_gt_30_percentag = ((roa_gt_30_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    data.append((stat, total_coun, roi_gt_10_percentag, roi_gt_30_percentag, roa_gt_10_percentag, roa_gt_30_percentag))

roi_count_df = pd.DataFrame(data, columns=['State', 'Total Facilities', 'ROI > 10%', 'ROI > 30%', 'ROA > 10%', 'ROA > 30%'])
percentages_columns = ['ROI > 10%', 'ROI > 30%', 'ROA > 10%', 'ROA > 30%']
roi_count_df[percentages_columns] = roi_count_df[percentages_columns].applymap(lambda x: "{:.0f}%".format(x))

roi_count_df.sort_values(by = 'ROI > 10%', ascending = False)

d = df.copy()
d['Liquidated Value'] = d['Total Assets'] - d['Total liabilities']
d['ROI'] = (d['Net Income'] / d['Liquidated Value'] * 100).round(0)
d['ROA'] = (d['Net Income'] / d['Total Assets'] * 100).round(0)

state = ['CA', 'NY', 'OH', 'CO', 'NC', 'ID', 'HI']

data = []

for stat in state:
    states_df = d[d['State Code'] == stat]
    total_coun = len(states_df)
    roi_gt_10_coun = (states_df['ROI'] > 10).sum()
    roi_gt_30_coun = (states_df['ROI'] > 30).sum()
    roi_gt_10_percentag = ((roi_gt_10_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roi_gt_30_percentag = ((roi_gt_30_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roa_gt_10_coun = (states_df['ROA'] > 10).sum()
    roa_gt_30_coun = (states_df['ROA'] > 30).sum()
    roa_gt_10_percentag = ((roa_gt_10_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    roa_gt_30_percentag = ((roa_gt_30_coun / total_coun) * 100).round(0) if total_coun > 0 else 0
    data.append((stat, total_coun, roi_gt_10_percentag, roi_gt_30_percentag, roa_gt_10_percentag, roa_gt_30_percentag))

roi_count_df = pd.DataFrame(data, columns=['State', 'Total Facilities', 'ROI > 10%', 'ROI > 30%', 'ROA > 10%', 'ROA > 30%'])
percentages_columns = ['ROI > 10%', 'ROI > 30%', 'ROA > 10%', 'ROA > 30%']
roi_count_df[percentages_columns] = roi_count_df[percentages_columns].applymap(lambda x: "{:.0f}%".format(x))

roi_count_df.sort_values(by = 'ROI > 10%', ascending = False)