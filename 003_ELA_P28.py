# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd


# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "answer", "translation": "答案；回答",
     "sentence": "I know the answer to the question.",
     "sentence_zh": "我知道這個問題的答案。"},
    
    {"word": "find", "translation": "找到；發現",
     "sentence": "Can you find your book on the desk?",
     "sentence_zh": "你可以在桌子上找到你的書嗎？"},
    
    {"word": "its", "translation": "它的",
     "sentence": "The dog is wagging its tail.",
     "sentence_zh": "那隻狗正在搖它的尾巴。"},
    
    {"word": "miss", "translation": "想念；錯過",
     "sentence": "I miss my friends during the holidays.",
     "sentence_zh": "放假期間我很想念我的朋友。"},
    
    {"word": "old", "translation": "老的；舊的",
     "sentence": "My grandfather has an old watch.",
     "sentence_zh": "我爺爺有一只很舊的手錶。"},
    
    {"word": "round", "translation": "圓的",
     "sentence": "The ball is round.",
     "sentence_zh": "這顆球是圓的。"},
    
    {"word": "then", "translation": "然後；那時",
     "sentence": "We ate dinner and then watched a movie.",
     "sentence_zh": "我們先吃晚餐，然後看電影。"},
    
    {"word": "until", "translation": "直到",
     "sentence": "I will wait here until you come back.",
     "sentence_zh": "我會在這裡等到你回來。"},
    
    {"word": "what", "translation": "什麼",
     "sentence": "What is your favorite game?",
     "sentence_zh": "你最喜歡的遊戲是什麼？"},
    
    {"word": "young", "translation": "年輕的；幼小的",
     "sentence": "The young bird cannot fly yet.",
     "sentence_zh": "那隻幼鳥還不會飛。"},
    
    {"word": "tap", "translation": "輕敲；水龍頭",
     "sentence": "Please tap the screen to start the game.",
     "sentence_zh": "請輕敲螢幕來開始遊戲。"},
    
    {"word": "tape", "translation": "膠帶；貼膠帶",
     "sentence": "Use tape to fix the torn paper.",
     "sentence_zh": "用膠帶把撕破的紙黏好。"},
    
    {"word": "fin", "translation": "鰭；魚鰭",
     "sentence": "The shark’s fin is above the water.",
     "sentence_zh": "那條鯊魚的魚鰭露在水面上。"},
    
    {"word": "fine", "translation": "好的；很棒的",
     "sentence": "The weather is fine today.",
     "sentence_zh": "今天天氣很好。"},
    
    {"word": "cute", "translation": "可愛的",
     "sentence": "That puppy is very cute.",
     "sentence_zh": "那隻小狗非常可愛。"},
    
    {"word": "ride", "translation": "騎；乘坐",
     "sentence": "I ride my bike to school.",
     "sentence_zh": "我騎腳踏車上學。"},
    
    {"word": "rob", "translation": "搶劫；搶走",
     "sentence": "The police stopped the man who tried to rob the bank.",
     "sentence_zh": "警方阻止了那個想搶銀行的男子。"},
    
    {"word": "robe", "translation": "長袍；浴袍",
     "sentence": "She wore a long robe at home.",
     "sentence_zh": "她在家裡穿著一件長袍。"},
    
    {"word": "cap", "translation": "帽子（棒球帽等）",
     "sentence": "Ben wears a blue cap every day.",
     "sentence_zh": "Ben 每天都戴一頂藍色帽子。"},
    
    {"word": "cape", "translation": "斗篷；披肩",
     "sentence": "The superhero has a red cape.",
     "sentence_zh": "那位超級英雄有一件紅色斗篷。"},
    
    {"word": "slid", "translation": "滑動；滑行（slide 的過去式）",
     "sentence": "The boy slid down the slide in the playground.",
     "sentence_zh": "那個男孩從遊樂場的溜滑梯上滑下來。"},
    
    {"word": "shop", "translation": "商店；購物",
     "sentence": "We will shop for new shoes this weekend.",
     "sentence_zh": "我們這個週末要去買新鞋子。"},
    
    {"word": "wish", "translation": "希望；許願",
     "sentence": "Make a wish before you blow out the candles.",
     "sentence_zh": "吹蠟燭前先許個願。"},
    
    {"word": "cut", "translation": "切；剪",
     "sentence": "Use scissors to cut the paper.",
     "sentence_zh": "用剪刀把紙剪開。"},
    
    {"word": "rid", "translation": "擺脫；除去",
     "sentence": "We cleaned the room to get rid of the dust.",
     "sentence_zh": "我們打掃房間來擺脫灰塵。"},
    
    {"word": "scrap", "translation": "碎片；廢料",
     "sentence": "He wrote his notes on a scrap of paper.",
     "sentence_zh": "他在一張紙片上寫下筆記。"},
    
    {"word": "scrape", "translation": "刮；擦傷",
     "sentence": "Be careful not to scrape your knee on the ground.",
     "sentence_zh": "小心不要把膝蓋在地上磨破皮。"},
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