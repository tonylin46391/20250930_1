# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
import datetime
import pandas as pd
import os  # 用來讀取本地 mp3 檔案

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "ash", "translation": "灰燼",
     "sentence": "There was ash all over the fireplace after we burned the wood.",
     "sentence_zh": "我們把木頭燒完後，壁爐裡到處都是灰燼。"},
    
    {"word": "block graph", "translation": "長條方塊圖；統計方塊圖",
     "sentence": "Our teacher showed us a block graph to compare how many books we read.",
     "sentence_zh": "老師用一張長條方塊圖來比較我們各自讀了多少本書。"},
    
    {"word": "burn", "translation": "燃燒；燒掉",
     "sentence": "Be careful not to burn the paper when you light the candle.",
     "sentence_zh": "點蠟燭的時候要小心，別把紙給燒掉了。"},
    
    {"word": "fabric", "translation": "布料",
     "sentence": "This T-shirt is made of soft cotton fabric.",
     "sentence_zh": "這件 T 恤是用柔軟的棉質布料做成的。"},
    
    {"word": "flexible", "translation": "有彈性的；可彎曲的",
     "sentence": "A rubber band is flexible and can stretch without breaking.",
     "sentence_zh": "橡皮筋很有彈性，可以拉長而不會斷掉。"},
    
    {"word": "light", "translation": "輕的",
     "sentence": "The plastic cup is light, so even a child can lift it easily.",
     "sentence_zh": "這個塑膠杯很輕，所以小朋友也能輕鬆拿起來。"},
    
    {"word": "manufactured", "translation": "人造的；製造出來的",
     "sentence": "Glass is a manufactured material made by heating sand.",
     "sentence_zh": "玻璃是一種人造材料，是把沙子加熱製造出來的。"},
    
    {"word": "naturally", "translation": "自然地；天然地",
     "sentence": "Some materials, like wood and cotton, occur naturally.",
     "sentence_zh": "有些材料像木頭和棉花，是在大自然中自然形成的。"},
    
    {"word": "not see-through", "translation": "不透明的",
     "sentence": "The cardboard is not see-through, so we cannot see the toy behind it.",
     "sentence_zh": "這塊卡紙是不透明的，所以我們看不到後面的玩具。"},
    
    {"word": "rust", "translation": "銹；鐵銹",
     "sentence": "The old bike was covered in rust after being left in the rain.",
     "sentence_zh": "那台舊腳踏車淋雨之後，整個都生滿了鐵銹。"},
    
    {"word": "see-through", "translation": "透明的",
     "sentence": "The glass window is see-through so we can watch the birds outside.",
     "sentence_zh": "玻璃窗是透明的，所以我們可以看到外面的鳥。"},
    
    {"word": "strong", "translation": "堅固的；強韌的",
     "sentence": "The metal bridge is strong and can hold many cars.",
     "sentence_zh": "這座金屬橋很堅固，可以承受很多車子通過。"},
    
    {"word": "test", "translation": "測試",
     "sentence": "We can test which material is stronger by putting weights on it.",
     "sentence_zh": "我們可以在材料上放重物，來測試哪一種比較堅固。"},
    
    {"word": "waterproof", "translation": "防水的",
     "sentence": "My raincoat is waterproof, so the rain cannot soak my clothes.",
     "sentence_zh": "我的雨衣是防水的，所以雨水不會把衣服弄濕。"},

     {
        "word": "metal",
        "translation": "金屬",
        "sentence": "Clue 1: I am a strong and hard material. I come from under the ground. I am used to make the body of a car. What material am I?",
        "sentence_zh": "線索 1：我是一種堅固又硬的材料。我來自地底下。我被用來製造汽車的車身。我是什麼材料呢？"
    },
    {
        "word": "cotton",
        "translation": "棉花",
        "sentence": "Clue 2: I am a light and soft material. I come from a plant. I am used to make clothes. What material am I?",
        "sentence_zh": "線索 2：我是一種輕又柔軟的材料。我來自一種植物。我被用來做衣服。我是什麼材料呢？"
    },
    {
        "word": "plastic",
        "translation": "塑膠",
        "sentence": "Clue 3: I am a waterproof material. I am used to make some toys and containers. What material am I?",
        "sentence_zh": "線索 3：我是一種防水的材料。我被用來製造一些玩具和容器。我是什麼材料呢？"
    },
    {
        "word": "glass",
        "translation": "玻璃",
        "sentence": "Clue 4: I am made from sand. I am see-through and used to make windows. What material am I?",
        "sentence_zh": "線索 4：我是用沙子做成的。我是透明的，常被用來做窗戶。我是什麼材料呢？"
    },
    {
        "word": "waterproof",
        "translation": "防水的",
        "sentence": "Ella can tell that the box is made of a waterproof material if the table is still dry and the box does not let water through.",
        "sentence_zh": "如果桌子依然是乾的，而且盒子不讓水漏出去，Ella 就可以判斷這個盒子是由防水材料做成的。"
    },
    {"word": "raincoat", 
    "translation": "雨衣",
     "sentence": "I wear a raincoat on rainy days to keep my clothes dry.",
     "sentence_zh": "下雨天我會穿雨衣，讓衣服保持乾燥。"}


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
