import pandas as pd
import holidays

def predict_sales(input_data: list[dict], model):
    df = pd.DataFrame(input_data)
    df["日付"] = pd.to_datetime(df["日付"])

    # 日本語の曜日（ロケール非依存）
    WEEKDAY_JP = ["月", "火", "水", "木", "金", "土", "日"]
    df["曜日"] = df["日付"].dt.weekday.apply(lambda x: WEEKDAY_JP[x])

    # 日本の祝日判定
    jp_holidays = holidays.Japan()
    df["祝日"] = df["日付"].apply(lambda x: 1 if x in jp_holidays else 0)

    # 特徴量抽出
    features = ["天気", "気温", "イベント", "ポイント", "プロモーション", "祝日"]
    X = df[features]

    preds = model.predict(X)
    df["予測フード売上"] = preds.round(1)

    return df[["日付", "曜日", "天気", "気温", "予測フード売上"]]