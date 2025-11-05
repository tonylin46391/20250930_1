# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "news", "translation": "消息；新聞",
     "sentence": "Do you want the good news or the bad news first?",
     "sentence_zh": "你想先聽好消息還是壞消息？"},

    {"word": "youth", "translation": "青年期；年輕人",
     "sentence": "The youth today are used to using electronic devices.",
     "sentence_zh": "現代的年輕人習慣使用電子裝置。"},

    {"word": "soon", "translation": "很快；不久",
     "sentence": "He promises to visit again soon.",
     "sentence_zh": "他答應很快會再次來拜訪。"},

    {"word": "true", "translation": "真實的；正確的（形容詞）",
     "sentence": "The novel is based on a true story.",
     "sentence_zh": "這本小說是根據真實故事改編。"},

    {"word": "stew", "translation": "燉菜（名詞）",
     "sentence": "Mother cooks great stews.",
     "sentence_zh": "媽媽煮的燉菜很好吃。"},

    {"word": "choose", "translation": "選擇（動詞）",
     "sentence": "There are several different options you can choose (from).",
     "sentence_zh": "你可以從好幾個不同的選項中做選擇。"},

    {"word": "weak", "translation": "虛弱的；不強壯的",
     "sentence": "I was too weak to carry all the books by myself.",
     "sentence_zh": "我太虛弱了，無法自己搬走所有的書。"},

    {"word": "loose", "translation": "鬆的；未固定的（形容詞）",
     "sentence": "My loose tooth fell out while I was sleeping.",
     "sentence_zh": "我那顆鬆動的牙齒在我睡覺時掉了。"},

    {"word": "dialogue", "translation": "對話；台詞（名詞）",
     "sentence": "We use speech marks to show dialogue when we write.",
     "sentence_zh": "我們在寫作時用引號來標示對話。"},

    {"word": "climax", "translation": "高潮；最關鍵情節（名詞）",
     "sentence": "Everything changes at the climax of a story.",
     "sentence_zh": "在故事的高潮，一切都會出現轉變。" }
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