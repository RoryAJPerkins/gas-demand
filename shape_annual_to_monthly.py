import pandas as pd

annual = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\International Energy Agency - final consumption of gas by sector in Poland (1).csv")
monthly = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\eurostat_monthly.csv", parse_dates=["date"], dayfirst=True)
mapping = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\eurostat_mapping.csv")

#annual.to_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\eurostat_test.csv")

monthly["date"] = pd.to_datetime(monthly["date"])
monthly["demand"] = pd.to_numeric(monthly["demand"])
monthly["Year"] = monthly["date"].dt.year
monthly["year_total"] = monthly.groupby("Year")["demand"].transform("sum")
monthly["weighting"] = monthly["demand"]/monthly["year_total"]

merged = monthly.merge(annual, on="Year", how="left")

merged['final_demand'] = merged['weighting']*merged['Value']

merged.to_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\eurostat_annual_test.csv")