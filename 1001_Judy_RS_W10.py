# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd


# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "panic", "translation": "恐慌；驚惶",
     "sentence": "Panic is a feeling of strong fear that leaves someone unable to think clearly.",
     "sentence_zh": "恐慌是一種強烈的害怕，使人無法清楚思考。"},

    {"word": "favorable", "translation": "有利的；正面的",
     "sentence": "He always makes a favorable impression because he is so friendly.",
     "sentence_zh": "他總能留下正面的印象，因為他非常友善。"},

    {"word": "porthole", "translation": "（船舶）舷窗",
     "sentence": "I looked out the porthole in my cabin as the ship approached land.",
     "sentence_zh": "當船隻接近陸地時，我從艙房的舷窗向外看。"},

    {"word": "densely", "translation": "密集地；稠密地",
     "sentence": "The ivy densely covered the house making it hard to see the window.",
     "sentence_zh": "常春藤密密地覆蓋著房子，讓窗戶難以看見。"},

    {"word": "reasonable", "translation": "合理的；合情理的",
     "sentence": "It is reasonable for this father to think that his son knocked over the plant pot.",
     "sentence_zh": "這位父親認為兒子打翻花盆是合理的。"},

    {"word": "delirious", "translation": "神志不清的；譫妄的",
     "sentence": "What illness was the cause of the character’s delirious feeling?",
     "sentence_zh": "是什麼疾病造成角色神志不清的感覺？"},

    {"word": "projected", "translation": "被投映的；被放映的",
     "sentence": "Why does a movie that is projected in 3-D seem so real?",
     "sentence_zh": "為什麼以 3D 投影的電影看起來如此真實？"},

    {"word": "contents", "translation": "目錄；內容項目",
     "sentence": "Do you read the table of contents before you read a book?",
     "sentence_zh": "你在讀一本書之前會先看目錄嗎？"},

    {"word": "deficiencies", "translation": "缺乏；不足（複數）",
     "sentence": "but it has some vitamin and mineral deficiencies.",
     "sentence_zh": "但它在維生素與礦物質方面仍有一些缺乏。"},

    {"word": "prose", "translation": "散文",
     "sentence": "Unlike poetry, prose is “ordinary writing,” in sentences and paragraphs.",
     "sentence_zh": "和詩不同，散文是由句子與段落組成的「一般寫作」。"}
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