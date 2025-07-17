import pandas as pd
import datetime
import random
import jpholiday

# イベント、ポイント、プロモーションのマッピング（utils.pyから）
EVENT_OPTIONS = {
    "なし": 0, "その他": 1, "花火": 2, "子供商店街": 3, "ライブ小": 4, "ライブ大": 5,
}
POINT_OPTIONS = {
    "通常": 0, "3倍": 1, "10倍": 2,
}
PROMOTION_OPTIONS = {
    "特になし": 0, "プロモーション初日": 1, "新ドリンク・新フード追加": 2,
}

def is_holiday(date):
    return jpholiday.is_holiday(date)

# 開始日と終了日の定義
start_date = datetime.date(2024, 10, 1)
end_date = datetime.date(2025, 6, 30)

# データを格納するリスト
data = []

current_date = start_date
while current_date <= end_date:
    row = {}
    row['日付'] = current_date.strftime('%Y-%m-%d')

    # 曜日
    day_of_week_japanese = ['月', '火', '水', '木', '金', '土', '日']
    row['曜日'] = day_of_week_japanese[current_date.weekday()]

    # 天気
    row['天気'] = random.randint(0, 2)

    # 気温
    row['気温'] = round(random.uniform(15.0, 30.0), 1)

    # 売上
    base_sales = random.randint(250, 500)
    # 週末/祝日の売上調整（簡易的なヒューリスティック）
    if row['曜日'] in ['土', '日'] or is_holiday(current_date):
        base_sales = int(base_sales * random.uniform(1.1, 1.3)) # 週末/祝日で10-30%増

    row['売上'] = base_sales

    # フード売上
    row['フード売上'] = random.randint(50, 100)

    # イベント
    row['イベント'] = random.choice(list(EVENT_OPTIONS.values()))

    # ポイント
    row['ポイント'] = random.choice(list(POINT_OPTIONS.values()))

    # プロモーション
    row['プロモーション'] = random.choice(list(PROMOTION_OPTIONS.values()))

    data.append(row)
    current_date += datetime.timedelta(days=1)

# pandas DataFrameを作成
df = pd.DataFrame(data)

# CSVファイル名
csv_file_path = 'sales_data_sample_utf8_bom.csv'

# UTF-8 with BOMでCSVを保存
# Excelで文字化けしにくくするために encoding='utf_8_sig' を使用
df.to_csv(csv_file_path, index=False, encoding='utf_8_sig')

print(f"CSVサンプルファイルが生成されました: {csv_file_path}")
print(f"文字コードはUTF-8 (BOM付き) で指定されています。")
print(df.head())
print(df.tail())