import streamlit as st
import pandas as pd

# 1. データのセットアップ（スプレッドシートの配点データを精密に反映）
def get_detailed_data():
    return [
        {
            "学部": "北海道大学 総合入試理系", 
            "共通比率": 0.4, "二次比率": 0.6, "偏差値": 57.5, 
            "重点": "数学・理科", "倍率": 3.8,
            "戦略根拠": "2次試験の配点比率が60%と高く、特に数学と理科のウェイトが重い設計。共通テストで多少出遅れても、記述力があれば一気に逆転が可能な『逆転合格の聖地』です。"
        },
        {
            "学部": "北海道大学 経済学部", 
            "共通比率": 0.6, "二次比率": 0.4, "偏差値": 60.0, 
            "重点": "数学・英語", "倍率": 3.5,
            "戦略根拠": "共通テストの配点比率が高いため、基礎を完璧に固めた層に有利。一方で2次試験に『地歴』がなく数学・英語で勝負できるため、文系数学が得意な受験生には極めて効率的なルートです。"
        },
        {
            "学部": "北海道大学 医学部医学科", 
            "共通比率": 0.17, "二次比率": 0.83, "偏差値": 67.5, 
            "重点": "全教科", "倍率": 4.1,
            "戦略根拠": "圧倒的な2次重視（83%）。共通テストは『足切り突破』の道具と割り切り、すべてのリソースを最高難度の記述対策に振るべき特攻ルート。精密な処理能力が試されます。"
        }
    ]

# 2. 逆転指数の詳細計算
def calculate_analysis(row, user_dev, user_strong):
    diff = row['偏差値'] - user_dev
    index = 100 - (diff * 7) + (row['二次比率'] * 40)
    if user_strong in row['重点']: index += 15
    return min(max(int(index), 0), 99)

# --- UI実装 ---
st.set_page_config(page_title="SystemK Strategy Engine", layout="wide")
st.title("🏹 SystemK | 戦略根拠提示エンジン")

# サイドバー設定
st.sidebar.header("診断パラメータ")
u_dev = st.sidebar.slider("現在の偏差値", 45.0, 75.0, 56.0)
u_strong = st.sidebar.selectbox("得意教科", ["数学・理科", "英語・国語", "数学・英語"])

# 判定実行
data = get_detailed_data()
results = []
for r in data:
    r['score'] = calculate_analysis(r, u_dev, u_strong)
    results.append(r)
results = sorted(results, key=lambda x: x['score'], reverse=True)

# メイン表示
st.subheader(f"【判定結果】あなたの属性に基づいた戦略的選択肢")

for res in results:
    # 逆転指数に応じたカラーリング
    color = "green" if res['score'] > 70 else "orange" if res['score'] > 40 else "red"
    
    with st.container():
        st.markdown(f"### {res['学部']} <span style='color:{color}'>（逆転指数: {res['score']}%）</span>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("ターゲット偏差値", res['偏差値'], delta=round(u_dev - res['偏差値'], 1))
            st.write(f"**2次配点比率:** {int(res['二次比率']*100)}%")
            st.write(f"**強化すべき教科:** {res['重点']}")
            
        with col2:
            st.info(f"#### 💡 なぜこのルートが強いのか？\n{res['戦略根拠']}")
            
            # 決定稿に基づく「今日のアクション」
            st.success(f"**【直近の戦術】**\n{res['重点']}の過去問を3年分分析し、配点の25%を占める頻出単元を特定せよ。")
        
        st.divider()
