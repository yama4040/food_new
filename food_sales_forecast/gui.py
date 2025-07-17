import streamlit as st
import pandas as pd
import joblib
import subprocess  # ★モデル更新用に追加
from datetime import datetime, timedelta

from data_loader import load_all_csv_data
from predictor import predict_sales
from utils import WEATHER_OPTIONS, EVENT_OPTIONS, POINT_OPTIONS, PROMOTION_OPTIONS

def run_app():
    st.title("フード売上予測システム")

    # ----------------------------
    # モデル更新ボタン
    # ----------------------------
    if st.button("モデルを再学習（CSVから再構築）"):
        with st.spinner("モデルを再学習しています..."):
            try:
                subprocess.run(["python", "train_model.py"], check=True)
                st.success("モデルの更新が完了しました。")
            except subprocess.CalledProcessError:
                st.error("モデルの更新に失敗しました。train_model.py を確認してください。")

    # モデル読み込み
    model = joblib.load("models/food_sales_model.pkl")

    # 過去データ読み込みとグラフ表示
    st.subheader("過去のフード売上推移")
    df = load_all_csv_data()
    df["日付"] = pd.to_datetime(df["日付"])

    start = st.date_input("開始日", df["日付"].min().date())
    end = st.date_input("終了日", df["日付"].max().date())

    view_mode = st.radio("表示モード", ("日別", "週平均"))
    plot_data = df[(df["日付"] >= pd.to_datetime(start)) & (df["日付"] <= pd.to_datetime(end))]

    if view_mode == "週平均":
        plot_data["週"] = plot_data["日付"].dt.to_period("W").apply(lambda r: r.start_time)
        weekly_avg = plot_data.groupby("週")["フード売上"].mean().reset_index()
        weekly_avg.columns = ["日付", "フード売上"]
        st.line_chart(weekly_avg.set_index("日付"))
    else:
        st.line_chart(plot_data.set_index("日付")["フード売上"])

    # 予測UI（横並び形式）
    st.subheader("次週の予測入力")
    today = datetime.today()
    days_ahead = 0 - today.weekday() + 7  # 次の月曜までの日数
    if days_ahead <= 0:
        days_ahead += 7
    start_date = today + timedelta(days=days_ahead)
    dates = [start_date + timedelta(days=i) for i in range(7)]

    # 日付見出し
    cols = st.columns(7)
    for i, col in enumerate(cols):
        col.markdown(f"**{dates[i].strftime('%m月%d日（%a）')}**")

    # 天気
    st.markdown("**天気**")
    weather_inputs = []
    for i, col in enumerate(st.columns(7)):
        w = col.selectbox(" ", WEATHER_OPTIONS.keys(), key=f"weather_{i}")
        weather_inputs.append(WEATHER_OPTIONS[w])

    # 気温
    st.markdown("**最高気温**")
    temp_inputs = []
    for i, col in enumerate(st.columns(7)):
        t = col.number_input(" ", min_value=0.0, max_value=45.0, value=25.0, step=0.1, key=f"temp_{i}")
        temp_inputs.append(t)

    # イベント
    st.markdown("**イベント**")
    event_inputs = []
    for i, col in enumerate(st.columns(7)):
        e = col.selectbox(" ", EVENT_OPTIONS.keys(), key=f"event_{i}")
        event_inputs.append(EVENT_OPTIONS[e])

    # ポイント
    st.markdown("**ポイント**")
    point_inputs = []
    for i, col in enumerate(st.columns(7)):
        p = col.selectbox(" ", POINT_OPTIONS.keys(), key=f"point_{i}")
        point_inputs.append(POINT_OPTIONS[p])

    # プロモーション
    st.markdown("**プロモーション**")
    promo_inputs = []
    for i, col in enumerate(st.columns(7)):
        pr = col.selectbox(" ", PROMOTION_OPTIONS.keys(), key=f"promo_{i}")
        promo_inputs.append(PROMOTION_OPTIONS[pr])

    # 予測ボタン
    if st.button("予測実行"):
        input_data = []
        for i in range(7):
            input_data.append({
                "日付": dates[i],
                "天気": weather_inputs[i],
                "気温": temp_inputs[i],
                "イベント": event_inputs[i],
                "ポイント": point_inputs[i],
                "プロモーション": promo_inputs[i]
            })
        result = predict_sales(input_data, model)
        st.subheader("予測結果")
        st.table(result)

if __name__ == "__main__":
    run_app()