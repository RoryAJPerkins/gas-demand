import pandas as pd
#df = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\raw\eurostat_gfp.csv")
#df.to_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\raw\power_data.csv")#
#########################################

df_output = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\analyzed\monthly_demand_clean.csv")
df = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\raw\eurostat\latest_data.csv")

df_output = df_output.drop(
    df_output[(df_output['country'] != 'UK') & (df_output['type'] == 'total')].index
)

# Parse date
df['date'] = pd.to_datetime(df['date'])

# Extract year and month
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Set / map type (example: total -> power)
#df['type'] = 'power'   # or use a mapping if needed

# Select and reorder columns to match target schema
df = df[['country', 'type', 'year', 'month', 'demand', 'source']]

#print(df.head(), df_output.head())

df_output = pd.concat([df, df_output], ignore_index=True)

df_output['date'] = pd.to_datetime(
    dict(year=df_output['year'], month=df_output['month'], day=1)
)

cols = ['date'] + [c for c in df_output.columns if c != 'date']
df_output = df_output[cols]

df_output.to_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\analyzed\monthly_demand_clean_new.csv", index=False)