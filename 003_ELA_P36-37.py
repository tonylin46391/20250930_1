# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "examine", "translation": "檢查；仔細查看",
     "sentence": "Grace and Kelly wanted to examine the soil for any bugs.",
     "sentence_zh": "Grace 和 Kelly 想要檢查土壤是否有任何蟲子。"},
    
    {"word": "identify", "translation": "識別；辨認",
     "sentence": "These road signs identify a railroad crossing, the speed limit, a highway exit, and a school crosswalk.",
     "sentence_zh": "這些道路標誌分別代表鐵路平交道、速限、高速公路出口，以及學校行人穿越道。"},
    
    {"word": "record", "translation": "記錄",
     "sentence": "Trevor will record what he learned in his notebook.",
     "sentence_zh": "Trevor 會把學到的內容記錄在筆記本裡。"},
    
    {"word": "amount", "translation": "數量",
     "sentence": "Each glass has a different amount of juice.",
     "sentence_zh": "每個杯子裡的果汁量都不同。"},
    
    {"word": "material", "translation": "布料；材料",
     "sentence": "My mother was trying to choose material to make a skirt.",
     "sentence_zh": "我媽媽正打算選布料來做一件裙子。"},
    
    {"word": "space", "translation": "空間",
     "sentence": "These books do not take up much space on the shelf.",
     "sentence_zh": "這些書在書架上不太佔空間。"},
    
    {"word": "example", "translation": "例子",
     "sentence": "A banana is an example of a fruit.",
     "sentence_zh": "香蕉是水果的一個例子。"},
    
    {"word": "easily", "translation": "容易地；輕鬆地",
     "sentence": "I can easily count to five.",
     "sentence_zh": "我可以輕鬆數到五。"},
    
    {"word": "forms", "translation": "形狀；形式（複數）",
     "sentence": "Pasta comes in many different forms.",
     "sentence_zh": "義大利麵有許多不同的形狀。"},
    
    {"word": "planet", "translation": "行星",
     "sentence": "Our planet moves around the sun.",
     "sentence_zh": "我們的行星繞著太陽運行。"},
    
    {"word": "tasty", "translation": "美味的",
     "sentence": "We all enjoyed a slice of the tasty pizza.",
     "sentence_zh": "我們大家都很享受那一片美味的披薩。"}
]

        
            
        
    



# 將題庫整理為字典，方便查詢
words = [item["word"] for item in word_bank]
translations = {item["word"]: item["translation"] for item in word_bank}
sentences = {item["word"]: item["sentence"] for item in word_bank}
sentences_zh = {item["word"]: item["sentence_zh"] for item in word_bank}

# --- 初始化 session state ---
if "index" not in st.session_state:
    st.session_state.index = 0
if "answered" not in st.session_state:
    st.session_state.answered = {}
if "stats" not in st.session_state:
    st.session_state.stats = {w: {"正確": 0, "錯誤": 0} for w in words}
if "history" not in st.session_state:
    st.session_state.history = []

# 目前題目
current_word = words[st.session_state.index]
translation = translations[current_word]
sentence = sentences[current_word]
sentence_zh = sentences_zh[current_word]

# --- 標題縮小 ---
st.markdown("<p style='font-size:22px'><b>🎧 單字 + 句子 發音練習</b></p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>📌 發音按鈕 (單字 / 英文例句 / 中文翻譯)</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>✏️ 單字測驗（請輸入你聽到的單字）</p>", unsafe_allow_html=True)

# --- 三個發音按鈕 ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ 單字（英文）"):
        # 直接播放英文單字
        tts = gTTS(current_word, lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format="audio/mp3")

with col2:
    if st.button("▶ 例句（英文）"):
        tts = gTTS(sentence, lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format="audio/mp3")

with col3:
    if st.button("▶ 中文翻譯"):
        tts = gTTS(sentence_zh, lang="zh-TW")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format="audio/mp3")


# 顯示文字 (不顯示英文單字)
st.write(f"中文單字翻譯：**{translation}**")
st.write(f"英文例句：*{sentence}*")
st.write(f"中文翻譯：*{sentence_zh}*")

# --- 單字答題表單 ---
input_key = f"input_{current_word}_{st.session_state.index}"
with st.form(key=f"form_{current_word}", clear_on_submit=False):
    user_input = st.text_input("", key=input_key, autocomplete="off")
    submitted = st.form_submit_button("提交答案")
    if submitted:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if user_input.strip().lower() == current_word.lower():
            st.session_state.stats[current_word]["正確"] += 1
            st.success("✅ 答對了！")
            st.session_state.answered[current_word] = True
        else:
            st.session_state.stats[current_word]["錯誤"] += 1
            # ❌ 答錯時顯示正確答案
            st.error(f"❌ 答錯！正確答案是：**{current_word}**")
            st.session_state.answered[current_word] = False
        
        # 紀錄歷史
        st.session_state.history.append({
            "單字": current_word,
            "學生輸入答案": user_input,
            "結果": "正確" if user_input.strip().lower()==current_word.lower() else "錯誤",
            "正確答案": current_word,
            "時間": now_str
        })


# --- 下一題 ---
if st.button("➡ 下一題"):
    st.session_state.index = (st.session_state.index + 1) % len(words)
    st.rerun()

# --- 側邊欄統計 ---
st.sidebar.header("📊 練習進度統計")
done = sum(1 for v in st.session_state.answered.values() if v)
total = len(words)
st.sidebar.write(f"✅ 已練習並答對：{done} / {total} 個單字")

st.sidebar.subheader("📈 單字答題統計")
stats_list = [{"單字": w, "正確/總次數": f"{s['正確']}/{s['正確']+s['錯誤']}" if s['正確']+s['錯誤']>0 else "0/0"} for w,s in st.session_state.stats.items()]
st.sidebar.dataframe(pd.DataFrame(stats_list), use_container_width=True)

st.sidebar.subheader("📝 歷史紀錄")
if st.session_state.history:
    st.sidebar.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)