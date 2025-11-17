# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd
import os  # ✅ 新增：用來讀取本地 mp3 檔案

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "close", "translation": "關上；合上（動詞）",
     "sentence": "Please ??? the door.",
     "sentence_zh": "請把門關上。"},

    {"word": "cold", "translation": "冷的",
     "sentence": "The water is ???.",
     "sentence_zh": "水很冷。"},

    {"word": "come", "translation": "來；過來",
     "sentence": "Please ??? here.",
     "sentence_zh": "請到這裡來。"},

    {"word": "done", "translation": "完成了",
     "sentence": "I am ??? with my homework.",
     "sentence_zh": "我的作業做完了。"},

    {"word": "fire", "translation": "火；火焰",
     "sentence": "The ??? kept us warm.",
     "sentence_zh": "火讓我們保持溫暖。"},

    {"word": "front", "translation": "前面",
     "sentence": "She stood in ??? of the class.",
     "sentence_zh": "她站在班級前面。"},

    {"word": "life", "translation": "生活；生命",
     "sentence": "??? is full of surprises.",
     "sentence_zh": "生活充滿驚喜。"},

    {"word": "name", "translation": "名字",
     "sentence": "What is your ????",
     "sentence_zh": "你叫什麼名字？"},

    {"word": "small", "translation": "小的",
     "sentence": "This is a ??? cat.",
     "sentence_zh": "這是一隻小貓。"},

    {"word": "times", "translation": "次數；倍",
     "sentence": "I read the book three ???.",
     "sentence_zh": "我把這本書讀了三次。"},

    {"word": "doze", "translation": "打盹；小睡",
     "sentence": "He began to ??? on the bus.",
     "sentence_zh": "他在公車上開始打盹。"},

    {"word": "nose", "translation": "鼻子",
     "sentence": "My ??? is itchy.",
     "sentence_zh": "我的鼻子很癢。"},

    {"word": "use", "translation": "使用",
     "sentence": "We ??? pencils in class.",
     "sentence_zh": "我們在課堂上使用鉛筆。"},

    {"word": "rose", "translation": "玫瑰；玫瑰花",
     "sentence": "The ??? smells sweet.",
     "sentence_zh": "這朵玫瑰聞起來很香。"},

    {"word": "pole", "translation": "竿；柱；桿子",
     "sentence": "The flag hangs on the ???.",
     "sentence_zh": "旗子掛在旗桿上。"},

    {"word": "close", "translation": "親近的；接近的（形容詞）",
     "sentence": "We are ??? friends.",
     "sentence_zh": "我們是要好的朋友。"},

    {"word": "June", "translation": "六月",
     "sentence": "School ends in ???.",
     "sentence_zh": "學校在六月結束學期。"},

    {"word": "woke", "translation": "醒來（wake 的過去式）",
     "sentence": "She ??? up early.",
     "sentence_zh": "她很早就醒來了。"},

    {"word": "rule", "translation": "規則；規定",
     "sentence": "Please follow the ???.",
     "sentence_zh": "請遵守規則。"},

    {"word": "rode", "translation": "騎（ride 的過去式）",
     "sentence": "He ??? his bike to school.",
     "sentence_zh": "他騎腳踏車去上學。"},

    {"word": "role", "translation": "角色",
     "sentence": "He played the ??? of a king.",
     "sentence_zh": "他扮演國王的角色。"},

    {"word": "tune", "translation": "曲調；旋律",
     "sentence": "I like this ???.",
     "sentence_zh": "我喜歡這首旋律。"},

    {"word": "hum", "translation": "哼唱",
     "sentence": "She likes to ??? songs.",
     "sentence_zh": "她喜歡哼唱歌曲。"},

    {"word": "shut", "translation": "關上；闔上",
     "sentence": "??? the window, please.",
     "sentence_zh": "請把窗戶關上。"},

    {"word": "frog", "translation": "青蛙",
     "sentence": "The ??? jumped into the pond.",
     "sentence_zh": "那隻青蛙跳進池塘裡。"},

    {"word": "job", "translation": "工作；職業",
     "sentence": "He found a new ???.",
     "sentence_zh": "他找到了一份新工作。"},

    {"word": "wrote", "translation": "寫（write 的過去式）",
     "sentence": "She ??? a letter.",
     "sentence_zh": "她寫了一封信。"},

    {"word": "flute", "translation": "長笛",
     "sentence": "He plays the ??? well.",
     "sentence_zh": "他長笛吹得很好。"}
]

# 將題庫整理為字典，方便查詢
words = [item["word"] for item in word_bank]
translations = {item["word"]: item["translation"] for item in word_bank}
sentences = {item["word"]: item["sentence"] for item in word_bank}
sentences_zh = {item["word"]: item["sentence_zh"] for item in word_bank}

# 🔊 本地 mp3 資料夾
AUDIO_DIR = "audio"

def play_word_audio(word: str):
    """
    播放對應單字的本地 mp3 檔案。
    檔名規則：audio/<單字>.mp3，例如 audio/close.mp3
    """
    filename = os.path.join(AUDIO_DIR, f"{word}.mp3")
    if not os.path.exists(filename):
        st.warning(f"⚠ 找不到音檔：{filename}")
        return
    try:
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"讀取音檔時發生錯誤：{e}")

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
        # ✅ 改成播放本地 mp3，不再使用 gTTS
        play_word_audio(current_word)

with col2:
    if st.button("▶ 例句（英文）"):
        # 仍使用 gTTS（如果之後也要改成本地 mp3，可以再調整）
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
stats_list = [
    {
        "單字": w,
        "正確/總次數": f"{s['正確']}/{s['正確']+s['錯誤']}" if s['正確']+s['錯誤']>0 else "0/0"
    }
    for w, s in st.session_state.stats.items()
]
st.sidebar.dataframe(pd.DataFrame(stats_list), use_container_width=True)

st.sidebar.subheader("📝 歷史紀錄")
if st.session_state.history:
    st.sidebar.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
