import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Create skill frequency trends over time
def skill_trend_over_time(df, date_col='posted_date', skills_col='skills'):
    trend = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        date = pd.to_datetime(row[date_col]).strftime('%Y-%m')
        for skill in row[skills_col]:
            trend[skill][date] += 1
    return pd.DataFrame(trend).fillna(0).sort_index()
