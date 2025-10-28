# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd


# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "planned", "translation": "計畫；規劃",
     "sentence": "We carefully planned for the big event.",
     "sentence_zh": "我們仔細地為這個大活動做了計畫。"},

    {"word": "citizen", "translation": "公民；市民",
     "sentence": "A citizen pledges loyalty to her country’s flag.",
     "sentence_zh": "一位公民向自己國家的國旗宣示效忠。"},

    {"word": "difference", "translation": "差異；改變（造成正面影響）",
     "sentence": "We all made a difference by working together to clean up the park.",
     "sentence_zh": "我們齊心協力清理公園，確實帶來了改變。"},

    {"word": "kind", "translation": "善良的；友善的",
     "sentence": "Sharing an umbrella on a rainy day is a kind thing to do.",
     "sentence_zh": "在雨天與人共用一把雨傘是一件很友善的事。"},

    {"word": "munch", "translation": "嘎吱嘎吱地吃；咀嚼",
     "sentence": "After school, Claire likes to munch on fresh vegetables.",
     "sentence_zh": "放學後，克萊兒喜歡咀嚼新鮮蔬菜。"},    

    {"word": "bellowed", "translation": "（低沉地）吼叫；咆哮（過去式）",
     "sentence": "The elk bellowed to communicate with other elk.",
     "sentence_zh": "那隻麋鹿發出低沉的吼聲，與其他麋鹿溝通。"},

    {"word": "rough", "translation": "粗魯的；激烈的；粗糙的",
     "sentence": "Sometimes the puppies play too rough.",
     "sentence_zh": "有時候這些小狗玩得太激烈了。"},

    {"word": "handle", "translation": "處理；應付；掌握",
     "sentence": "Andrew is able to handle many activities in one day.",
     "sentence_zh": "安德魯能在一天內處理許多活動。"},    

    {"word": "cool", "translation": "冷卻；使冷靜；冷靜下來",
     "sentence": "Listening to music is one way to cool down and feel calm.",
     "sentence_zh": "聽音樂是一種讓自己冷靜下來、感到平靜的方法。"},    

    {"word": "bounce", "translation": "彈跳；使反彈",
     "sentence": "My friends and I like to bounce in a bounce house.",
     "sentence_zh": "我和朋友們喜歡在充氣彈跳屋裡彈跳。"},    

    {"word": "grinned", "translation": "露齒而笑；咧嘴笑（過去式）",
     "sentence": "Emma grinned at the camera.",
     "sentence_zh": "艾瑪對著相機咧嘴一笑。"},    

    {"word": "might", "translation": "力氣；力量；威力",
     "sentence": "She kicked the ball with all her might.",
     "sentence_zh": "她用盡全力把球踢了出去。"}
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