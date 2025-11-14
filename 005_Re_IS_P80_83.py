# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd
 
            
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