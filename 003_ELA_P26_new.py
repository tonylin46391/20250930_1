# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
import datetime
import pandas as pd
import os  # 用來讀取本地 mp3 檔案

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "close", "translation": "關上；合上（動詞）",
     "sentence": "Please close the door.",
     "sentence_zh": "請把門關上。"},

    {"word": "cold", "translation": "冷的",
     "sentence": "The water is cold.",
     "sentence_zh": "水很冷。"},

    {"word": "come", "translation": "來；過來",
     "sentence": "Please come here.",
     "sentence_zh": "請到這裡來。"},

    {"word": "done", "translation": "完成了",
     "sentence": "I am done with my homework.",
     "sentence_zh": "我的作業做完了。"},

    {"word": "fire", "translation": "火；火焰",
     "sentence": "The fire kept us warm.",
     "sentence_zh": "火讓我們保持溫暖。"},

    {"word": "front", "translation": "前面",
     "sentence": "She stood in front of the class.",
     "sentence_zh": "她站在班級前面。"},

    {"word": "life", "translation": "生活；生命",
     "sentence": "life is full of surprises.",
     "sentence_zh": "生活充滿驚喜。"},

    {"word": "name", "translation": "名字",
     "sentence": "What is your "name",
     "sentence_zh": "你叫什麼名字？"},

    {"word": "small", "translation": "小的",
     "sentence": "This is a small cat.",
     "sentence_zh": "這是一隻小貓。"},

    {"word": "times", "translation": "次數；倍",
     "sentence": "I read the book three times.",
     "sentence_zh": "我把這本書讀了三次。"},

    {"word": "doze", "translation": "打盹；小睡",
     "sentence": "He began to doze on the bus.",
     "sentence_zh": "他在公車上開始打盹。"},

    {"word": "nose", "translation": "鼻子",
     "sentence": "My nose is itchy.",
     "sentence_zh": "我的鼻子很癢。"},

    {"word": "use", "translation": "使用",
     "sentence": "We use pencils in class.",
     "sentence_zh": "我們在課堂上使用鉛筆。"},

    {"word": "rose", "translation": "玫瑰；玫瑰花",
     "sentence": "The rose smells sweet.",
     "sentence_zh": "這朵玫瑰聞起來很香。"},

    {"word": "pole", "translation": "竿；柱；桿子",
     "sentence": "The flag hangs on the pole.",
     "sentence_zh": "旗子掛在旗桿上。"},

    {"word": "close", "translation": "親近的；接近的（形容詞）",
     "sentence": "We are close friends.",
     "sentence_zh": "我們是要好的朋友。"},

    {"word": "June", "translation": "六月",
     "sentence": "School ends in June.",
     "sentence_zh": "學校在六月結束學期。"},

    {"word": "woke", "translation": "醒來（wake 的過去式）",
     "sentence": "She woke up early.",
     "sentence_zh": "她很早就醒來了。"},

    {"word": "rule", "translation": "規則；規定",
     "sentence": "Please follow the rule.",
     "sentence_zh": "請遵守規則。"},

    {"word": "rode", "translation": "騎（ride 的過去式）",
     "sentence": "He rode his bike to school.",
     "sentence_zh": "他騎腳踏車去上學。"},

    {"word": "role", "translation": "角色",
     "sentence": "He played the role of a king.",
     "sentence_zh": "他扮演國王的角色。"},

    {"word": "tune", "translation": "曲調；旋律",
     "sentence": "I like this tune.",
     "sentence_zh": "我喜歡這首旋律。"},

    {"word": "hum", "translation": "哼唱",
     "sentence": "She likes to hum songs.",
     "sentence_zh": "她喜歡哼唱歌曲。"},

    {"word": "shut", "translation": "關上；闔上",
     "sentence": "shut the window, please.",
     "sentence_zh": "請把窗戶關上。"},

    {"word": "frog", "translation": "青蛙",
     "sentence": "The frog jumped into the pond.",
     "sentence_zh": "那隻青蛙跳進池塘裡。"},

    {"word": "job", "translation": "工作；職業",
     "sentence": "He found a new job.",
     "sentence_zh": "他找到了一份新工作。"},

    {"word": "wrote", "translation": "寫（write 的過去式）",
     "sentence": "She wrote a letter.",
     "sentence_zh": "她寫了一封信。"},

    {"word": "flute", "translation": "長笛",
     "sentence": "He plays the flute well.",
     "sentence_zh": "他長笛吹得很好。"}
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
