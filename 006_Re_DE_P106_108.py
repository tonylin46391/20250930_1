# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd
 
   # 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "soup", "translation": "湯",
     "sentence": "I eat soup for dinner.",
     "sentence_zh": "我晚餐喝湯。"},
    
    {"word": "salad", "translation": "沙拉",
     "sentence": "Mom makes a big salad with vegetables.",
     "sentence_zh": "媽媽用很多蔬菜做了一大碗沙拉。"},
    
    {"word": "spaghetti", "translation": "義大利麵",
     "sentence": "We have spaghetti for lunch on Saturdays.",
     "sentence_zh": "我們星期六中午吃義大利麵。"},
    
    {"word": "french fries", "translation": "薯條",
     "sentence": "He likes to eat french fries with ketchup.",
     "sentence_zh": "他喜歡配番茄醬吃薯條。"},
    
    {"word": "steak", "translation": "牛排",
     "sentence": "Dad orders a steak at the restaurant.",
     "sentence_zh": "爸爸在餐廳點了一份牛排。"},
    
    {"word": "eggs", "translation": "雞蛋",
     "sentence": "She eats two eggs for breakfast.",
     "sentence_zh": "她早餐吃兩顆雞蛋。"},
    
    {"word": "apple", "translation": "蘋果",
     "sentence": "I have an apple in my lunch box.",
     "sentence_zh": "我的便當盒裡有一顆蘋果。"},
    
    {"word": "banana", "translation": "香蕉",
     "sentence": "The monkey is eating a banana.",
     "sentence_zh": "那隻猴子正在吃香蕉。"},
    
    {"word": "orange", "translation": "柳橙；橘子",
     "sentence": "This orange is sweet and juicy.",
     "sentence_zh": "這顆柳橙又甜又多汁。"},
    
    {"word": "peach", "translation": "桃子",
     "sentence": "She buys a peach from the market.",
     "sentence_zh": "她在市場買了一顆桃子。"},
    
    {"word": "milk", "translation": "牛奶",
     "sentence": "I drink a glass of milk every morning.",
     "sentence_zh": "我每天早上喝一杯牛奶。"},
    
    {"word": "yogurt", "translation": "優格；酸奶",
     "sentence": "Tom eats strawberry yogurt for a snack.",
     "sentence_zh": "Tom 點心時間吃草莓優格。"},
    
    {"word": "cheese", "translation": "起司；乳酪",
     "sentence": "There is cheese on my sandwich.",
     "sentence_zh": "我的三明治裡有起司。"},
    
    {"word": "butter", "translation": "奶油",
     "sentence": "I put butter on my toast.",
     "sentence_zh": "我把奶油塗在吐司上。"},
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