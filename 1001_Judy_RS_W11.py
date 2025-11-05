# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "uneducated", "translation": "未受良好教育的；缺乏教育的",
     "sentence": "The uneducated man found it difficult to find a well-paid job.",
     "sentence_zh": "那位未受良好教育的男子發現，要找到一份高薪工作很困難。"},

    {"word": "undecided", "translation": "未決定的；拿不定主意的",
     "sentence": "I’m still undecided about who to vote for.",
     "sentence_zh": "我仍然沒有決定要把票投給誰。"},

    {"word": "nonsense", "translation": "胡說；荒謬的話；無稽之談",
     "sentence": "Don’t listen to him. He is talking nonsense again!",
     "sentence_zh": "別理他。他又在說胡話了！"},

    {"word": "nonstick", "translation": "（鍋具）不沾的",
     "sentence": "My mom has plenty of nonstick pans.",
     "sentence_zh": "我媽媽有很多個不沾鍋。"},    

    {"word": "disown", "translation": "斷絕關係；不再承認（關係或責任）",
     "sentence": "The girl’s family disowned her for marrying an old man who was twice her age.",
     "sentence_zh": "那女孩因嫁給一位年紀是她兩倍的老人而被家人斷絕關係。"},

    {"word": "disuse", "translation": "廢置；不再使用（名詞）",
     "sentence": "The typewriter fell into disuse twenty years ago.",
     "sentence_zh": "打字機在二十年前就被淘汰不用了。"},    

    {"word": "dusty", "translation": "佈滿灰塵的",
     "sentence": "I wiped the dusty desk clean with a wet rag.",
     "sentence_zh": "我用濕抹布把滿是灰塵的桌子擦乾淨。"},    

    {"word": "sandy", "translation": "佈滿沙的；沙質的",
     "sentence": "I love the sandy beaches along the coast of Thailand.",
     "sentence_zh": "我喜歡泰國海岸線沿途那些沙質海灘。"},    

    {"word": "readily", "translation": "容易地；迅速地；不費力地",
     "sentence": "All ingredients are readily available from your local store.",
     "sentence_zh": "所有食材在你家附近的商店很容易就能買到。"},    

    {"word": "smoothly", "translation": "順利地；平順地",
     "sentence": "Today’s lesson went smoothly. The students understood everything.",
     "sentence_zh": "今天的課進行得很順利，學生們全都聽懂了。"}
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