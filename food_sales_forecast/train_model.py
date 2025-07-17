import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from utils import WEATHER_OPTIONS, EVENT_OPTIONS, POINT_OPTIONS, PROMOTION_OPTIONS


# データ読み込み
data_dir = "data"
all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]

# ファイルを読み込んで列名を統一
df_list = []
for f in all_files:
    df = pd.read_csv(f, parse_dates=["日付"], encoding="utf-8")
    df.rename(columns={"プロモ": "プロモーション"}, inplace=True)
    df_list.append(df)

all_data = pd.concat(df_list, ignore_index=True)

# 欠損行を除去（フード売上がNaNの行は学習対象外）
all_data = all_data.dropna(subset=["フード売上"])

# 特徴量と目的変数
target_col = "フード売上"
feature_cols = ["天気", "気温", "イベント", "ポイント", "プロモーション"]

# 祝日列が存在しない場合は追加（例外回避）
if "祝日" not in all_data.columns:
    all_data["祝日"] = 0
feature_cols.append("祝日")

X = all_data[feature_cols]
y = all_data[target_col]

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデル学習
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 精度評価
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Test MSE: {mse:.2f}")

# モデル保存
os.makedirs("models", exist_ok=True)
joblib.dump(model, os.path.join("models", "food_sales_model.pkl"))
print("モデルを保存しました: models/food_sales_model.pkl")
