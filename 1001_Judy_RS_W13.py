# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "exclude", "translation": "排除；不包括",
     "sentence": "The naughty student was excluded from the lesson and had to stand outside the classroom.",
     "sentence_zh": "那位不守規矩的學生被排除在課程之外，只能站在教室外面。"},

    {"word": "newspaper", "translation": "報紙；新聞媒體",
     "sentence": "Dad reads a newspaper every morning.",
     "sentence_zh": "爸爸每天早上都會讀報紙。"},

    {"word": "routine", "translation": "日常作息；例行公事",
     "sentence": "Try to make exercise a part of your daily routine.",
     "sentence_zh": "試著把運動變成你每日例行的一部分。"},

    {"word": "bassoon", "translation": "低音管；巴松管（木管樂器）",
     "sentence": "Not many people can play the bassoon.",
     "sentence_zh": "能吹奏低音管的人不多。"},

    {"word": "interview", "translation": "面試；訪談",
     "sentence": "I had to answer a lot of questions at the interview for the job.",
     "sentence_zh": "在那場求職面試中，我必須回答很多問題。"},

    {"word": "review", "translation": "複習；評論；回顧",
      "sentence": "We will review the key points before the quiz.",
      "sentence_zh": "小考前我們會複習重點。"},

    {"word": "confusing", "translation": "令人困惑的；不清楚的",
     "sentence": "The students didn’t know what to do because the directions were confusing.",
     "sentence_zh": "學生們不知道該怎麼做，因為指示很讓人困惑。"},

    {"word": "rescue", "translation": "救援；營救",
     "sentence": "The lifeguard rescued the boy when he had trouble swimming in the ocean.",
     "sentence_zh": "那名救生員在男孩於海中游泳遇到困難時把他救起來。"},

    {"word": "foreword", "translation": "（書籍）序言",
     "sentence": "The foreword explained the author’s purpose for writing the book.",
     "sentence_zh": "序言說明了作者撰寫本書的目的。"},

    {"word": "journal", "translation": "日誌；期刊",
     "sentence": "Many people keep a journal to record the day’s events.",
     "sentence_zh": "許多人會寫日誌來記錄一天中發生的事情。"}
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