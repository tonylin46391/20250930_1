# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
import datetime
import pandas as pd
import os  # 用來讀取本地 mp3 檔案

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





# 預先下載的 mp3 放在這個資料夾
AUDIO_DIR = "audio"


def play_audio(filepath: str):
    """播放本地 mp3，如果檔案不存在就提示警告。"""
    if not os.path.exists(filepath):
        st.warning(f"⚠ 找不到音檔：{os.path.basename(filepath)}")
        return
    try:
        with open(filepath, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"讀取音檔時發生錯誤：{e}")


# --- 初始化 session state ---
total_questions = len(word_bank)

if "index" not in st.session_state:
    st.session_state.index = 0  # 題目索引（0 ~ len-1）

# 每一題的答題狀態：None / True / False
if "answered" not in st.session_state:
    st.session_state.answered = [None] * total_questions

# 每一題的統計：用 list 依 index 存，避免同字不同題目互相覆蓋
if "stats" not in st.session_state:
    st.session_state.stats = [{"正確": 0, "錯誤": 0} for _ in range(total_questions)]

if "history" not in st.session_state:
    st.session_state.history = []

# 目前題目（用 index 直接對應 word_bank，不再用字典 key）
current_index = st.session_state.index
current_item = word_bank[current_index]
current_word = current_item["word"]
translation = current_item["translation"]
sentence = current_item["sentence"]
sentence_zh = current_item["sentence_zh"]

# 對應 make_audio_files.py 的命名規則：XX_word_en.mp3 / XX_sent_en.mp3 / XX_sent_zh.mp3
# base = 01_close / 02_cold / ...
base_name = f"{current_index + 1:02d}_{current_word}"

word_audio_path    = os.path.join(AUDIO_DIR, f"{base_name}_word_en.mp3")
sent_en_audio_path = os.path.join(AUDIO_DIR, f"{base_name}_sent_en.mp3")
sent_zh_audio_path = os.path.join(AUDIO_DIR, f"{base_name}_sent_zh.mp3")

# --- 標題 ---
st.markdown("<p style='font-size:22px'><b>🎧 單字 + 句子 發音練習</b></p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>📌 發音按鈕 (單字 / 英文例句 / 中文翻譯)</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>✏️ 單字測驗（請輸入你聽到的單字）</p>", unsafe_allow_html=True)

# --- 三個發音按鈕 ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ 單字（英文）"):
        play_audio(word_audio_path)

with col2:
    if st.button("▶ 例句（英文）"):
        play_audio(sent_en_audio_path)

with col3:
    if st.button("▶ 中文翻譯"):
        play_audio(sent_zh_audio_path)

# 顯示文字（這裡就直接用 current_item，不會被另一個 close 蓋掉）
st.write(f"中文單字翻譯：**{translation}**")
st.write(f"英文例句：*{sentence}*")
st.write(f"中文翻譯：*{sentence_zh}*")

# --- 單字答題表單 ---
input_key = f"input_{current_word}_{current_index}"
with st.form(key=f"form_{current_index}", clear_on_submit=False):
    user_input = st.text_input("", key=input_key, autocomplete="off")
    submitted = st.form_submit_button("提交答案")
    if submitted:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_correct = (user_input.strip().lower() == current_word.lower())

        # 依「題號」記錄統計
        if is_correct:
            st.session_state.stats[current_index]["正確"] += 1
            st.success("✅ 答對了！")
            st.session_state.answered[current_index] = True
        else:
            st.session_state.stats[current_index]["錯誤"] += 1
            st.error(f"❌ 答錯！正確答案是：**{current_word}**")
            st.session_state.answered[current_index] = False

        # 紀錄歷史
        st.session_state.history.append({
            "題號": current_index + 1,
            "單字": current_word,
            "學生輸入答案": user_input,
            "結果": "正確" if is_correct else "錯誤",
            "正確答案": current_word,
            "時間": now_str
        })

# --- 下一題 ---
if st.button("➡ 下一題"):
    st.session_state.index = (st.session_state.index + 1) % total_questions
    st.rerun()

# --- 側邊欄統計 ---
st.sidebar.header("📊 練習進度統計")
done = sum(1 for v in st.session_state.answered if v is True)
st.sidebar.write(f"✅ 已練習並答對：{done} / {total_questions} 個單字")

st.sidebar.subheader("📈 單字答題統計")
stats_list = []
for i, item in enumerate(word_bank):
    s = st.session_state.stats[i]
    total_try = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_try}" if total_try > 0 else "0/0"
    stats_list.append({
        "題號": i + 1,
        "單字": item["word"],
        "正確/總次數": rate
    })
st.sidebar.dataframe(pd.DataFrame(stats_list), use_container_width=True)

st.sidebar.subheader("📝 歷史紀錄")
if st.session_state.history:
    st.sidebar.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
