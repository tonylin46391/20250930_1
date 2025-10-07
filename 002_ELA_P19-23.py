# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd


# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "planned", "translation": "計劃", 
     "sentence": "We carefully planned for the big event.", 
     "sentence_zh": "我們仔細地為這個大活動做了計畫。"},

    {"word": "perfect", "translation": "完美的", 
     "sentence": "The photographer said it was a perfect day to take pictures outside.", 
     "sentence_zh": "攝影師說，今天是個在戶外拍照的完美日子。"},

    {"word": "hamper", "translation": "洗衣籃", 
     "sentence": "I put my dirty sweatshirt in the clothes hamper.", 
     "sentence_zh": "我把髒的運動衫放進洗衣籃裡。"},

    {"word": "disaster", "translation": "災難", 
     "sentence": "My dad was not happy about the disaster my dog made in our living room.", 
     "sentence_zh": "我爸爸對我的狗在客廳造成的災難感到不開心。"},

    {"word": "scowl", "translation": "怒容", 
     "sentence": "When Anna is upset, she makes a scowl.", 
     "sentence_zh": "當安娜心情不好時，她會露出怒容。"},

    {"word": "mood", "translation": "心情", 
     "sentence": "Each of these faces shows a different mood.", 
     "sentence_zh": "這些臉部表情各自展現出不同的心情。"},

    {"word": "queasy", "translation": "噁心的", 
     "sentence": "Sylvia felt queasy after she finished eating breakfast.", 
     "sentence_zh": "西爾維亞吃完早餐後感到有點噁心。"},

    {"word": "fiddled", "translation": "擺弄", 
     "sentence": "Elena fiddled with her hair as she waited for her friend.", 
     "sentence_zh": "艾蓮娜在等朋友時，一邊擺弄著她的頭髮。"},

    {"word": "Picture Day", "translation": "拍照日", 
     "sentence": "Picture day is a special day at school when a photographer takes your picture. You wear nice clothes, smile, and pose for the camera. You get a printed copy to keep and show your family and friends. It's a fun day to remember your time at school.", 
     "sentence_zh": "拍照日是學校裡特別的一天，攝影師會幫你拍照。你會穿上漂亮的衣服、微笑並擺出姿勢拍照。你還會得到一張照片留作紀念，與家人和朋友分享。這是個能回憶學校時光的有趣日子。"},

    {"word": "bedhead", "translation": "睡亂頭髮", 
     "sentence": "Bedhead is a word that means having messy hair when you wake up. It's a fun way to say messy hair.", 
     "sentence_zh": "「Bedhead」是指剛睡醒時頭髮亂糟糟的樣子，是一種有趣的說法來形容凌亂的頭髮。"}
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