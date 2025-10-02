import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 題庫
words = [
    "external/ placed or growing outside or on the outside of something." , "difference", "kind", "munch", 
    "bellowed", "rough", "handle", "cool", 
    "bounce", "grinned", "might"
]

# 新增：中英文對照表
translations = {
    "external": "外部 / 句子:位於或生長在某物外部",
    "difference": "差異",
    "kind": "種類 / 善良的",
    "munch": "大聲咀嚼",
    "bellowed": "吼叫",
    "rough": "粗糙的 / 粗暴的",
    "handle": "處理 / 把手",
    "cool": "涼爽 / 酷的",
    "bounce": "彈跳",
    "grinned": "咧嘴笑",
    "might": "可能 / 力量"
}

# 初始化 session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "mode" not in st.session_state:  # normal / review
    st.session_state.mode = "normal"
if "retry_queue" not in st.session_state:
    st.session_state.retry_queue = []
if "answered" not in st.session_state:
    st.session_state.answered = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "stats" not in st.session_state:
    st.session_state.stats = {w: {"正確": 0, "錯誤": 0} for w in words}
if "last_result" not in st.session_state:
    st.session_state.last_result = None  

st.markdown('<p style="font-size:26px">🎧 聽音辨字練習</p>', unsafe_allow_html=True)

def generate_tts(word):
    tts = gTTS(text=word, lang="en", tld="com")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp.read(), format="audio/mp3")

    # 新增：播放時顯示中文翻譯
    if word in translations:
        st.markdown(f"<p style='font-size:20px'>中文翻譯：<b>{translations[word]}</b></p>", unsafe_allow_html=True)

# 📌 取得下一個題目
def get_next_word():
    if st.session_state.mode == "review":
        if st.session_state.retry_queue:
            return st.session_state.retry_queue[0]
        else:
            st.session_state.mode = "normal"
            st.session_state.index = 0
            st.session_state.last_result = "🎉 錯題複習完成！開始新一輪！"
            return words[st.session_state.index]

    if st.session_state.index < len(words):
        return words[st.session_state.index]
    else:
        wrongs = [w for w, ans in st.session_state.answered.items() if ans is False]
        if wrongs:
            st.session_state.mode = "review"
            st.session_state.retry_queue = wrongs.copy()
            st.session_state.last_result = "🔁 進入錯題複習！"
            return st.session_state.retry_queue[0]
        else:
            st.session_state.index = 0
            st.session_state.answered = {}
            st.session_state.last_result = "🎉 全部正確！開始新一輪！"
            return words[st.session_state.index]

# 取得目前題目
current_word = get_next_word()
input_key = f"input_{current_word}_{st.session_state.index}_{st.session_state.mode}"

# 自動播放音訊 + 顯示翻譯
if "played" not in st.session_state or st.session_state.get("last_word") != current_word:
    generate_tts(current_word)
    st.session_state.played = True
    st.session_state.last_word = current_word

# 顯示最新答題結果訊息
if st.session_state.last_result:
    st.info(st.session_state.last_result)

# 提交答案
def submit_answer():
    user_input = st.session_state[input_key]
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user_input == current_word:
        st.session_state.stats[current_word]["正確"] += 1
        result = "正確"
        st.session_state.last_result = "✅ 答對了！"
        if st.session_state.mode == "review":
            if current_word in st.session_state.retry_queue:
                st.session_state.retry_queue.remove(current_word)
        else:
            st.session_state.answered[current_word] = True
    else:
        st.session_state.stats[current_word]["錯誤"] += 1
        result = "錯誤"
        st.session_state.last_result = "❌ 答錯！"
        if st.session_state.mode != "review":
            st.session_state.answered[current_word] = False

    st.session_state.history.append({
        "題目": current_word,
        "結果": result,
        "學生輸入的答案": user_input,
        "時間": now_str
    })

    if st.session_state.mode == "normal":
        st.session_state.index += 1

    st.session_state.played = False
    st.session_state.last_word = None

# 輸入表單
with st.form(key=f"form_{current_word}", clear_on_submit=False):
    st.text_input("請輸入你聽到的英文字：", key=input_key, autocomplete="off")
    st.form_submit_button("提交答案", on_click=submit_answer)

# 側邊欄進度
st.sidebar.header("📊 學習進度")
done = sum(1 for v in st.session_state.answered.values() if v is True)
total = len(words)
st.sidebar.write(f"✅ 已正確答對：{done} / {total}")

# 答題歷史
st.sidebar.header("📝 答題歷史")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.sidebar.dataframe(df, use_container_width=True)

# 單字正確率統計
st.sidebar.header("📊 單字正確率統計")
stats_list = []
for w, s in st.session_state.stats.items():
    total_attempts = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_attempts}" if total_attempts > 0 else "0/0"
    stats_list.append({"單字": w, "正確/總次數": rate})
df_stats = pd.DataFrame(stats_list)
st.sidebar.dataframe(df_stats, use_container_width=True)
