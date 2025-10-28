# ----------當錯題時在測試一次對了在能下一題----------------

import streamlit as st
from gtts import gTTS
import io
import datetime
import pandas as pd


# 📌 題庫 (單字 + 例句 + 中文翻譯)
word_bank = [
            
    {"word": "a", "translation": "一個",
     "sentence": "She has ??? new book.",
     "sentence_zh": "她有一本新書。"},

    {"word": "and", "translation": "和；以及",
     "sentence": "Tom ??? Jerry are friends.",
     "sentence_zh": "湯姆和傑利是朋友。"},

    {"word": "go", "translation": "去",
     "sentence": "Let's ??? to the park.",
     "sentence_zh": "我們去公園吧。"},

    {"word": "got", "translation": "得到",
     "sentence": "I ??? a gift for my birthday.",
     "sentence_zh": "我生日時收到了一份禮物。"},

    {"word": "have", "translation": "有",
     "sentence": "I ??? two pencils.",
     "sentence_zh": "我有兩支鉛筆。"},

    {"word": "not", "translation": "不是；不",
     "sentence": "I am ??? tired.",
     "sentence_zh": "我不累。"},

    {"word": "the", "translation": "這個；那個",
     "sentence": "??? dog is very cute.",
     "sentence_zh": "那隻狗很可愛。"},

    {"word": "to", "translation": "到；向",
     "sentence": "She went ??? school early.",
     "sentence_zh": "她很早就去上學了。"},

    {"word": "will", "translation": "將要",
     "sentence": "I ??? call you later.",
     "sentence_zh": "我待會會打電話給你。"},

    {"word": "you", "translation": "你；妳；你們",
     "sentence": "??? are my best friend.",
     "sentence_zh": "你是我最好的朋友。"},

    {"word": "sad", "translation": "難過的",
     "sentence": "She felt ??? after the movie.",
     "sentence_zh": "看完電影後她覺得難過。"},

    {"word": "bit", "translation": "一點點",
     "sentence": "He ate a ??? of cake.",
     "sentence_zh": "他吃了一點蛋糕。"},

    {"word": "jam", "translation": "果醬",
     "sentence": "I like strawberry ??? on my toast.",
     "sentence_zh": "我喜歡在烤麵包上塗草莓果醬。"},

    {"word": "glad", "translation": "高興的",
     "sentence": "I am ??? to see you.",
     "sentence_zh": "見到你我很高興。"},

    {"word": "list", "translation": "清單",
     "sentence": "We made a shopping ???.",
     "sentence_zh": "我們列了一張購物清單。"},

    {"word": "win", "translation": "贏",
     "sentence": "They will ??? the game.",
     "sentence_zh": "他們會贏得比賽。"},

    {"word": "flat", "translation": "平的；公寓",
     "sentence": "The table is ???.",
     "sentence_zh": "這張桌子是平的。"},

    {"word": "if", "translation": "如果",
     "sentence": "??? it rains, we will stay home.",
     "sentence_zh": "如果下雨，我們就待在家裡。"},

    {"word": "fix", "translation": "修理",
     "sentence": "Dad can ??? the bike.",
     "sentence_zh": "爸爸會修理腳踏車。"},

    {"word": "rip", "translation": "撕裂",
     "sentence": "Be careful not to ??? your shirt.",
     "sentence_zh": "小心不要把襯衫撕破。"},

    {"word": "kit", "translation": "工具組；套裝",
     "sentence": "I have a first aid ???.",
     "sentence_zh": "我有一個急救包。"},

    {"word": "mask", "translation": "口罩；面具",
     "sentence": "He wore a ??? to the party.",
     "sentence_zh": "他戴著面具去參加派對。"},

    {"word": "as", "translation": "如同；當作",
     "sentence": "She works ??? a teacher.",
     "sentence_zh": "她的工作是老師。"},

    {"word": "his", "translation": "他的",
     "sentence": "This is ??? book.",
     "sentence_zh": "這是他的書。"},

    {"word": "clap", "translation": "拍手",
     "sentence": "Let's ??? for the singer.",
     "sentence_zh": "讓我們為歌手拍手。"},

    {"word": "chip", "translation": "薄片；晶片",
     "sentence": "He ate a potato ???.",
     "sentence_zh": "他吃了一片洋芋片。"},

    {"word": "picnic", "translation": "野餐",
     "sentence": "We had a ??? by the lake.",
     "sentence_zh": "我們在湖邊野餐。"},

    {"word": "sandwich", "translation": "三明治",
     "sentence": "I ate a ham ??? for lunch.",
     "sentence_zh": "我午餐吃了一個火腿三明治。"},

    {"word": "best", "translation": "最好的",
     "sentence": "She is my ??? friend.",
     "sentence_zh": "她是我最好的朋友。"},

    {"word": "does", "translation": "做（第三人稱單數）",
     "sentence": "He ??? his homework every day.",
     "sentence_zh": "他每天都做功課。"},

    {"word": "end", "translation": "結束",
     "sentence": "The movie will ??? soon.",
     "sentence_zh": "電影很快就要結束了。"},

    {"word": "job", "translation": "工作",
     "sentence": "He has a new ???.",
     "sentence_zh": "他有一份新工作。"},

    {"word": "left", "translation": "離開；剩下",
     "sentence": "She ??? her bag at home.",
     "sentence_zh": "她把包包忘在家裡了。"},

    {"word": "men", "translation": "男人（複數）",
     "sentence": "The ??? are working outside.",
     "sentence_zh": "那些男人正在外面工作。"},

    {"word": "more", "translation": "更多",
     "sentence": "I want ??? water.",
     "sentence_zh": "我想要更多水。"},

    {"word": "see", "translation": "看見",
     "sentence": "I can ??? the stars at night.",
     "sentence_zh": "我晚上可以看到星星。"},

    {"word": "than", "translation": "比",
     "sentence": "She is taller ??? me.",
     "sentence_zh": "她比我高。"},

    {"word": "wash", "translation": "洗",
     "sentence": "Please ??? your hands.",
     "sentence_zh": "請洗手。"},

    {"word": "yes", "translation": "是的",
     "sentence": "???, I like ice cream.",
     "sentence_zh": "是的，我喜歡冰淇淋。"},

    {"word": "hug", "translation": "擁抱",
     "sentence": "She gave me a big ???.",
     "sentence_zh": "她給了我一個大大的擁抱。"},

    {"word": "rest", "translation": "休息",
     "sentence": "You need to ??? after work.",
     "sentence_zh": "你下班後需要休息。"},

    {"word": "frog", "translation": "青蛙",
     "sentence": "A ??? jumped into the pond.",
     "sentence_zh": "一隻青蛙跳進池塘。"},

    {"word": "hum", "translation": "哼歌",
     "sentence": "She likes to ??? while cooking.",
     "sentence_zh": "她喜歡邊煮飯邊哼歌。"},

    {"word": "melt", "translation": "融化",
     "sentence": "The ice will ??? in the sun.",
     "sentence_zh": "冰會在太陽下融化。"},

    {"word": "plum", "translation": "李子",
     "sentence": "He ate a sweet ???.",
     "sentence_zh": "他吃了一顆甜李子。"},

    {"word": "shut", "translation": "關上",
     "sentence": "Please ??? the door.",
     "sentence_zh": "請關上門。"},

    {"word": "net", "translation": "網子",
     "sentence": "The fish got caught in the ???.",
     "sentence_zh": "魚被網子困住了。"},

    {"word": "dot", "translation": "點",
     "sentence": "Put a ??? on the paper.",
     "sentence_zh": "在紙上畫一個點。"},

    {"word": "puddle", "translation": "水坑",
     "sentence": "The kids jumped in the ???.",
     "sentence_zh": "孩子們在水坑裡跳來跳去。"},

    {"word": "helmet", "translation": "安全帽",
     "sentence": "Wear a ??? when you ride a bike.",
     "sentence_zh": "騎車時要戴安全帽。"},

    {"word": "do", "translation": "做",
     "sentence": "I will ??? my homework now.",
     "sentence_zh": "我現在要寫作業。"},

    {"word": "give", "translation": "給",
     "sentence": "Please ??? me the pen.",
     "sentence_zh": "請把筆給我。"},

    {"word": "he", "translation": "他",
     "sentence": "??? is my brother.",
     "sentence_zh": "他是我哥哥。"},

    {"word": "line", "translation": "線；排隊",
     "sentence": "Please stand in ???.",
     "sentence_zh": "請排隊。"},

    {"word": "said", "translation": "說",
     "sentence": "She ??? it was a nice day.",
     "sentence_zh": "她說今天天氣很好。"},

    {"word": "set", "translation": "設定；放置",
     "sentence": "??? the table for dinner.",
     "sentence_zh": "把餐桌擺好準備吃飯。"},

    {"word": "seven", "translation": "七",
     "sentence": "I have ??? apples.",
     "sentence_zh": "我有七顆蘋果。"},

    {"word": "sure", "translation": "確定的",
     "sentence": "Are you ??? about that?",
     "sentence_zh": "你確定嗎？"},

    {"word": "upon", "translation": "在...之上；一...就",
     "sentence": "Once ??? a time, there was a king.",
     "sentence_zh": "從前，有一位國王。"},

    {"word": "walk", "translation": "走路",
     "sentence": "Let's ??? to school together.",
     "sentence_zh": "我們一起走路去上學吧。"},

    {"word": "cake", "translation": "蛋糕",
     "sentence": "She baked a chocolate ???.",
     "sentence_zh": "她烤了一個巧克力蛋糕。"},

    {"word": "mine", "translation": "我的",
     "sentence": "That book is ???.",
     "sentence_zh": "那本書是我的。"},

    {"word": "plate", "translation": "盤子",
     "sentence": "Put the food on the ???e.",
     "sentence_zh": "把食物放在盤子上。"},

    {"word": "size", "translation": "大小；尺寸",
     "sentence": "What is your shoe ??? ?",
     "sentence_zh": "你的鞋子尺寸是多少？"},

    {"word": "ate", "translation": "吃了",
     "sentence": "He ??? all the cookies.",
     "sentence_zh": "他把餅乾都吃光了。"},

    {"word": "grape", "translation": "葡萄",
     "sentence": "I like to eat purple ???s.",
     "sentence_zh": "我喜歡吃紫色的葡萄。"},

    {"word": "prize", "translation": "獎品",
     "sentence": "She won a big ???.",
     "sentence_zh": "她贏得了一個大獎。"},

    {"word": "wipe", "translation": "擦拭",
     "sentence": "Please ??? the table clean.",
     "sentence_zh": "請把桌子擦乾淨。"},

    {"word": "race", "translation": "比賽；競賽",
     "sentence": "They ran a ??? at school.",
     "sentence_zh": "他們在學校參加了一場賽跑。"},

    {"word": "pile", "translation": "堆",
     "sentence": "There is a ??? of books on the desk.",
     "sentence_zh": "桌上有一堆書。"},

    {"word": "rake", "translation": "耙子；耙",
     "sentence": "He used a ??? to clean the leaves.",
     "sentence_zh": "他用耙子清理落葉。"},

    {"word": "mistake", "translation": "錯誤",
     "sentence": "Everyone makes a ??? sometimes.",
     "sentence_zh": "每個人有時都會犯錯。"},

    {"word": "guide", "translation": "導遊；指引",
     "sentence": "The ??? showed us around the museum.",
     "sentence_zh": "導遊帶我們參觀博物館。"}
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