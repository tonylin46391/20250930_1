# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
import datetime
import pandas as pd
import os  # 用來讀取本地 mp3 檔案

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
