import pandas as pd
import os
from datetime import date, timedelta

DATA_DIR = "data"

def load_all_csv_data():
    all_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    df_list = []
    for f in all_files:
        df = pd.read_csv(f, parse_dates=["日付"], encoding="utf-8")
        df.rename(columns={"プロモ": "プロモーション"}, inplace=True)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def generate_next_week_dates():
    today = date.today()
    # 今日が月曜なら来週の月曜、火曜...日曜を出す
    # 今日が水曜なら同様に来週の月曜～日曜
    days_ahead = 7 - today.weekday()  # 次の月曜までの日数
    next_monday = today + timedelta(days=days_ahead)
    return [next_monday + timedelta(days=i) for i in range(7)]
