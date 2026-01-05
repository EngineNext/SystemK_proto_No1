import streamlit as st
import pandas as pd

# 1. データのセットアップ（スプレッドシートの内容を反映）
def get_hokudai_data():
    data = [
        {"学部": "総合入試文系", "共通比率": 0.5, "二次比率": 0.5, "偏差値": 60.0, "重点": "英語・国語", "倍率": 3.2},
        {"学部": "総合入試理系", "共通比率": 0.4, "二次比率": 0.6, "偏差値": 57.5, "重点": "数学・理科", "倍率": 3.8},
        {"学部": "文学部", "共通比率": 0.5, "二次比率": 0.5, "偏差値": 60.0, "重点": "国語・英語", "倍率": 2.8},
        {"学部": "経済学部", "共通比率": 0.6, "二次比率": 0.4, "偏差値": 60.0, "重点": "数学・英語", "倍率": 3.5},
        {"学部": "医学部医学科", "共通比率": 0.17, "二次比率": 0.83, "偏差値": 67.5, "重点": "全教科", "倍率": 4.1},
    ]
    return pd.DataFrame(data)

# 2. 逆転指数の計算ロジック
def calculate_index(row, user_dev, user_strong):
    # 偏差値差分
    diff = row['偏差値'] - user_dev
    # 2次比率が高いほど、得意科目が合致しているほど逆転しやすい
    bonus = 20 if user_strong in row['重点'] else 0
    ratio_bonus = row['二次比率'] * 100
    
    index = 100 - (diff * 8) + (ratio_bonus * 0.5) + bonus
    return min(max(int(index), 5), 99)

# --- UI実装 ---
st.set_page_config(page_title="SystemK Prototype", layout="wide")
st.title("🏹 SystemK | 北海道大学・戦略判定エンジン")
st.write("用意された最新データに基づき、あなたの「逆転合格」を設計します。")

# サイドバー：ユーザー入力
st.sidebar.header("User Profile")
user_dev = st.sidebar.slider("現在の偏差値（全統模試等）", 45.0, 75.0, 55.0)
user_strong = st.sidebar.selectbox("記述で勝負できる得意教科", ["数学・理科", "英語・国語", "数学・英語", "国語・英語"])

# 判定実行
df = get_hokudai_data()
df['逆転指数'] = df.apply(lambda r: calculate_index(r, user_dev, user_strong), axis=1)
df = df.sort_values("逆転指数", ascending=False)

# 結果表示
st.subheader(f"偏差値 {user_dev} / {user_strong} 重点の戦略ルート")

for _, row in df.iterrows():
    with st.expander(f"{row['学部']} (逆転指数: {row['逆転指数']}%)"):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("逆転指数", f"{row['逆転指数']}%")
            st.write(f"**2次配点比率:** {int(row['二次比率']*100)}%")
        with col2:
            # 決定稿の思想に基づいたキラーコピー生成（簡易版）
            if row['逆転指数'] > 70:
                st.success(f"【戦略】共テのミスは誤差。2次の{row['重点']}で周囲を突き放せ。君のための配点だ。")
            elif row['逆転指数'] > 40:
                st.warning(f"【戦略】堅実な守りが必要。倍率 {row['倍率']}倍を逆手に取り、標準問題を完遂せよ。")
            else:
                st.error("【戦略】特攻は自死に近い。だが、記述配点に望みを繋ぐなら特定単元に全振りせよ。")

st.info("※このモックアップはスプレッドシートの配点比率データを参照しています。")
