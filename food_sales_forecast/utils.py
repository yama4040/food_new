import jpholiday

# 天気オプション
WEATHER_OPTIONS = {
    "晴れ": 2,
    "曇り": 1,
    "雨": 0
}


# イベントの辞書
EVENT_OPTIONS = {
    "なし": 0,
    "その他": 1,
    "花火": 2,
    "子供商店街": 3,
    "ライブ小": 4,
    "ライブ大": 5,
}

# ポイントの辞書
POINT_OPTIONS = {
    "通常": 0,
    "3倍": 1,
    "10倍": 2,
}

# プロモーションの辞書
PROMOTION_OPTIONS = {
    "特になし": 0,
    "プロモーション初日": 1,
    "新ドリンク・新フード追加": 2,
}

def get_event_options():
    return EVENT_OPTIONS

def get_point_options():
    return POINT_OPTIONS

def get_promotion_options():
    return PROMOTION_OPTIONS

def is_holiday(date):
    return jpholiday.is_holiday(date)