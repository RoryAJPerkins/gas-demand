import pandas as pd

m = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\raw\eurostat_gfp.csv")

m["date"] = pd.to_datetime(m["date"])

key = "country"   # <-- change this
val = "demand"               # <-- change this

def monthly_to_daily(g):
    g = g.sort_values("date").set_index("date")

    # days in month for each row
    dim = g.index.to_period("M").days_in_month

    # per-day value
    g["demand"] = g[val].to_numpy() / dim.to_numpy()

    # upsample to daily and carry that month’s daily_value across all days
    return g[["demand"]].resample("D").ffill()

daily = m.groupby(key, group_keys=True).apply(monthly_to_daily)

# daily has a MultiIndex: (key, date). If you want columns instead:
daily = daily.reset_index()
daily['type'] = 'power'
daily['source'] = 'eurostat'
daily['demand'] = daily['demand']*10.8e6


####################################### Now do same but for total ##################################################


mm = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\raw\eurostat\latest_data.csv")

mm["date"] = pd.to_datetime(mm["date"])

key = "country"   # <-- change this
val = "demand"               # <-- change this

def monthly_to_daily(g):
    g = g.sort_values("date").set_index("date")

    # days in month for each row
    dim = g.index.to_period("M").days_in_month

    # per-day value
    g["demand"] = g[val].to_numpy() / dim.to_numpy()

    # upsample to daily and carry that month’s daily_value across all days
    return g[["demand"]].resample("D").ffill()

dailyy = mm.groupby(key, group_keys=True).apply(monthly_to_daily)

# daily has a MultiIndex: (key, date). If you want columns instead:
dailyy = dailyy.reset_index()
dailyy['type'] = 'total'
dailyy['source'] = 'eurostat'
dailyy['demand'] = dailyy['demand']*10.8e6




####################################### Now replace power data in daily_demand_all with these new datasets ##################################################

df_output = pd.read_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\processed\daily_demand_all.csv")


df_output = df_output.drop(
    df_output[(df_output['type'] == 'power') & (df_output['country'] != 'UK')].index
)

df_output = df_output.drop(
    df_output[(df_output['type'] == 'total') & (df_output['country'] != 'UK')].index
)

result = pd.concat([df_output, daily], ignore_index=True)
result2 = pd.concat([result, dailyy], ignore_index=True)

#result2["date"] = (
#    pd.to_datetime(result2["date"], errors="coerce", dayfirst=True)
#      .dt.strftime("%d/%m/%Y")

result2 = result2.dropna(how="all")

result2.to_csv(r"C:\Users\RoryPerkins\OneDrive - Timera Energy\Documents\GitHub\gas-demand\src\data\processed\daily_demand_all_new.csv")