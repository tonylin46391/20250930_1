import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd

# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
    {"word": "external", "translation": "外部", "sentence": "External means placed or growing outside or on the outside of something.", "sentence_zh": "外部：位於某物外側或在外側生長。"},
    {"word": "front leg", "translation": "前腳", "sentence": "The front legs are at the front of an animal.", "sentence_zh": "前腳：動物的前面腿。"},
    {"word": "hind leg", "translation": "後腳", "sentence": "The hind legs are at the back of an animal.", "sentence_zh": "後腳：動物的後面腿。"},
    {"word": "wing", "translation": "翅膀", "sentence": "A wing is the body part of a bird that helps it fly.", "sentence_zh": "翅膀：鳥用來飛行的身體部位。"},
    {"word": "head", "translation": "頭", "sentence": "The head of an animal has eyes, ears, a nose, and a mouth.", "sentence_zh": "頭：動物的頭部有眼睛、耳朵、鼻子和嘴巴。"},
    {"word": "foot", "translation": "腳", "sentence": "A foot is a body part used for walking.", "sentence_zh": "腳：用來走路的身體部位。"},
    {"word": "tail", "translation": "尾巴", "sentence": "A tail is a body part found on many mammals and even fish.", "sentence_zh": "尾巴：許多哺乳動物甚至魚類身上的部位。"},
    {"word": "claws", "translation": "爪子", "sentence": "Claws are the sharp nails of the foot or paw of some animals.", "sentence_zh": "爪子：某些動物腳或爪的尖銳指甲。"},
    {"word": "skin", "translation": "皮膚", "sentence": "Skin is a layer that covers the body of many animals.", "sentence_zh": "皮膚：覆蓋許多動物身體的層。"},
    {"word": "skin coverings", "translation": "皮膚覆蓋物", "sentence": "Skin coverings are the outer covering over the skin of an animal.", "sentence_zh": "皮膚覆蓋物：覆蓋動物皮膚的外層。"},
    {"word": "fur", "translation": "毛皮", "sentence": "Fur is the body covering of mammals like dogs and cats.", "sentence_zh": "毛皮：哺乳動物如狗和貓的體毛。"},
    {"word": "scales", "translation": "鱗片", "sentence": "Scales are the body covering of snakes, fish, and crocodiles.", "sentence_zh": "鱗片：蛇、魚和鱷魚的身體覆蓋物。"},
    {"word": "feathers", "translation": "羽毛", "sentence": "Feathers are the body covering of birds.", "sentence_zh": "羽毛：鳥的身體覆蓋物。"},
    {"word": "spines", "translation": "刺", "sentence": "Spines are the sharp body covering of some animals like hedgehogs.", "sentence_zh": "刺：某些動物如刺蝟的尖銳體表。"},
    {"word": "offspring", "translation": "後代", "sentence": "Offspring are the young of an animal.", "sentence_zh": "後代：動物的幼崽。"},
    {"word": "young", "translation": "幼獸", "sentence": "Young is the baby of an animal.", "sentence_zh": "幼獸：動物的嬰兒。"},
    {"word": "adult", "translation": "成年體", "sentence": "An adult is all grown up, not a baby or child anymore.", "sentence_zh": "成年體：已完全成長，不再是嬰兒或小孩。"},
    {"word": "reproduce", "translation": "繁殖", "sentence": "To reproduce means to have young or to make more.", "sentence_zh": "繁殖：產生後代。"},
    {"word": "give birth", "translation": "生產", "sentence": "Giving birth is having live young.", "sentence_zh": "生產：生下活的後代。"},
    {"word": "lay eggs", "translation": "產卵", "sentence": "Birds lay eggs instead of giving birth.", "sentence_zh": "產卵：鳥產蛋而不是生小鳥。"},
    {"word": "hatch", "translation": "孵化", "sentence": "To hatch is coming out of an egg.", "sentence_zh": "孵化：從蛋中孵出。"},
    {"word": "crawl", "translation": "爬行", "sentence": "To crawl is moving on hands and knees, how babies move.", "sentence_zh": "爬行：用手和膝蓋移動，嬰兒的移動方式。"},
    {"word": "calf", "translation": "小牛", "sentence": "A calf is the young of a cow, camel, and hippo.", "sentence_zh": "小牛：牛、駱駝和河馬的幼崽。"},
    {"word": "chick", "translation": "小雞", "sentence": "A chick is the young of a hen (chicken).", "sentence_zh": "小雞：母雞的幼崽。"},
    {"word": "foal", "translation": "小馬", "sentence": "A foal is the young of a horse.", "sentence_zh": "小馬：馬的幼崽。"},
    {"word": "repeated", "translation": "重複的", "sentence": "Repeated means something that is repeated.", "sentence_zh": "重複的：被重複的事物。"},
    {"word": "poacher", "translation": "偷獵者", "sentence": "A poacher is a person who hunts and kills animals illegally.", "sentence_zh": "偷獵者：非法捕獵動物的人。"},
    {"word": "tusks", "translation": "長牙", "sentence": "Tusks are long body parts of an elephant or walrus, like a tooth.", "sentence_zh": "長牙：大象或海象的長形牙齒。"},
    {"word": "horns", "translation": "角", "sentence": "Horns are hard body parts that grow on the head of some animals, like rhinos and cows.", "sentence_zh": "角：某些動物頭部生長的硬部位，如犀牛和牛。"},
    {"word": "zoologist", "translation": "動物學家", "sentence": "A zoologist is a person who studies animals.", "sentence_zh": "動物學家：研究動物的人。"}
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
            st.error(f"❌ 答錯！")
            st.session_state.answered[current_word] = False
        st.session_state.history.append({
            "單字": current_word,
            "學生輸入答案": user_input,
            "結果": "正確" if user_input.strip().lower()==current_word.lower() else "錯誤",
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
