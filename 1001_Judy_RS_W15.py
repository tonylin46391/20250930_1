import streamlit as st
import datetime
import pandas as pd
import os 
from gtts import gTTS
import io
import difflib 
import re 

# --- 【修正】自定義 CSS 樣式 ---
st.markdown("""
<style>
/* 按鈕樣式 */
div.stButton > button,
button[kind="primary"] {
    min-width: 100%;
    font-size: 22px !important; 
    padding: 16px 10px !important; 
    border-radius: 16px !important;
    background-color: #58CC02 !important; 
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 0 #58A700 !important;
    cursor: pointer !important;
    transition: all 0.1s ease !important;
}

div.stButton > button:hover,
button[kind="primary"]:hover {
    background-color: #61E002 !important;
    box-shadow: 0 4px 0 #58A700 !important;
    transform: translateY(-2px) !important;
}

div.stButton > button:active,
button[kind="primary"]:active {
    background-color: #58A700 !important;
    box-shadow: 0 1px 0 #58A700 !important;
    transform: translateY(2px) !important;
}
    
div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stImage {
    margin-top: 0px; 
}

/* 隱藏文字輸入框標籤 */
.stTextInput > label {
    display: none;
}

/* 輸入框樣式 - 模仿 Duolingo */
.stTextInput > div > div > input {
    border: 3px solid #1CB0F6 !important;
    background: #ffffff !important;
    font-size: 32px !important;
    font-weight: 600 !important;
    color: #1CB0F6 !important;
    text-align: center !important;
    padding: 15px 30px !important;
    box-shadow: 0 2px 8px rgba(28, 176, 246, 0.2) !important;
    outline: none !important;
    border-radius: 12px !important;
    min-width: 250px !important;
    max-width: 400px !important;
}

.stTextInput > div > div > input::placeholder {
    color: #B0B0B0 !important;
    font-weight: 400 !important;
    font-size: 24px !important;
}

.stTextInput > div > div > input:focus {
    border: 3px solid #0D8BD9 !important;
    background: #F0F9FF !important;
    box-shadow: 0 4px 12px rgba(28, 176, 246, 0.3) !important;
    outline: none !important;
}

/* 調整輸入框容器,讓它置中 */
.stTextInput {
    display: flex;
    justify-content: center;
    margin: 15px 0 !important;
}

.stTextInput > div {
    width: auto !important;
}

.stTextInput > div > div {
    width: auto !important;
}

</style>
""", unsafe_allow_html=True)


word_bank = [
    {
        "word": "bounced",
        "translation": "彈跳；反彈 (v.)",
        "sentence": "I bounced the ball three times and threw it into the hoop.",
        "sentence_zh": "我讓球彈了三次，然後將它投進籃框。",
        "definition": "If something bounces, it moves quickly away from a surface it has just hit or you make it do this.",
        "definition_zh": "如果某物彈跳，它會從剛撞擊的表面迅速移開，或者你讓它這樣做。",
		"blank_index": 1
    },
    {
        "word": "author",
        "translation": "作家；作者 (n.)",
        "sentence": "The film is based on a novel written by a French author.",
        "sentence_zh": "這部電影是根據一位法國作家寫的小說改編的。",
        "definition": "A person who writes books.",
        "definition_zh": "寫書的人。",
		"blank_index": 11
    },
    {
        "word": "rejoiced",
        "translation": "歡慶；欣喜 (v.)",
        "sentence": "We rejoiced when we heard school was cancelled because of a typhoon.",
        "sentence_zh": "當我們聽到學校因為颱風而停課時，我們欣喜若狂。",
        "definition": "To show great happiness about something.",
        "definition_zh": "對某事表示極大的快樂。",
		"blank_index": 1
    },
    {
        "word": "loyal",
        "translation": "忠誠的；忠實的 (adj.)",
        "sentence": "The loyal soldiers fought bravely for their country.",
        "sentence_zh": "那些忠誠的士兵為他們的國家勇敢地戰鬥。",
        "definition": "Remaining constant in your support of somebody or something.",
        "definition_zh": "在你的支持中，對某人或某事保持始終如一。",
		"blank_index": 1
    },
    {
        "word": "grow",
        "translation": "生長；成長；增加 (v.)",
        "sentence": "The plant will grow into a tree eventually.",
        "sentence_zh": "這株植物最終會長成一棵樹。",
        "definition": "To increase in size, number, strength or quality.",
        "definition_zh": "在大小、數量、力量或品質上增加。",
		"blank_index": 3
    },
    {
        "word": "ocean",
        "translation": "海洋 (n.)",
        "sentence": "The biggest ocean is the Pacific.",
        "sentence_zh": "最大的海洋是太平洋。",
        "definition": "The mass of salt water that covers most of the earth's surface.",
        "definition_zh": "覆蓋地球表面大部分區域的鹹水體。",
		"blank_index": 2
    },
    {
        "word": "sprout",
        "translation": "發芽；萌芽 (v.)",
        "sentence": "Some seeds will sprout in a few days.",
        "sentence_zh": "有些種子會在幾天內發芽。",
        "definition": "When plants or seed produces new leaves or buds; to start to grow.",
        "definition_zh": "當植物或種子長出新的葉子或芽；開始生長。",
		"blank_index": 3
    },
    {
        "word": "pillows",
        "translation": "枕頭 (n.)",
        "sentence": "How many pillows do you have on your bed?",
        "sentence_zh": "你的床上有多少個枕頭？",
        "definition": "Cloth filled with soft material and used to rest your head on in bed.",
        "definition_zh": "裝滿柔軟材料的布，用於在床上休息頭部。",
		"blank_index": 2
    },
    {
        "word": "trampoline",
        "translation": "蹦床；彈簧墊 (n.)",
        "sentence": "Some kids have a trampoline in their back yards.",
        "sentence_zh": "有些孩子在他們的後院有蹦床。",
        "definition": "A piece of equipment that is used for doing jumps in the air.",
        "definition_zh": "一種用於在空中跳躍的設備。",
		"blank_index": 4
    },
    {
        "word": "thrilled",
        "translation": "非常興奮的；非常高興的 (adj.)",
        "sentence": "I was thrilled when I passed the English test.",
        "sentence_zh": "當我通過英語考試時，我非常興奮。",
        "definition": "Very excited and pleased.",
        "definition_zh": "非常興奮和高興。",
		"blank_index": 2
    },
]

def play_local_audio(filename: str):
    if not os.path.exists(filename):
        return
    
    try:
        audio_bytes = open(filename, 'rb').read()
        placeholder = st.empty()
        with placeholder:
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
    except Exception as e:
        st.error(f"播放本地音訊時發生錯誤:{e}")


def set_gtts_to_play(text: str, lang: str):
    if text:
        st.session_state.gtts_to_play = (text, lang)
        st.rerun()
    else:
        st.warning("⚠ 播放內容為空,無法生成語音。")
        
def centralized_gtts_playback():
    if st.session_state.gtts_to_play is not None:
        text, lang = st.session_state.gtts_to_play
        st.session_state.gtts_to_play = None
        
        placeholder = st.empty() 
        
        try:
            tts = gTTS(text=text, lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            with placeholder:
                st.audio(fp, format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error(f"生成語音時發生錯誤:{e}")


def get_diff_html(a: str, b: str) -> str:
    a = a.lower()
    b = b.lower()
    s = difflib.SequenceMatcher(None, a, b)

    correct = []
    inputed = []

    GREEN = "background:#ddffdd;"
    RED = "background:#b22222;color:white;"
    EMPTY = "background:#eeeeee;color:#888;"

    def span(text, style):
        import html
        text = html.escape(text)
        return f"<span style='{style}display:inline-block;width:20px;height:32px;line-height:27px;margin:1px;border-radius:4px;font-family:monospace;text-align:center;font-size:36px;'>{text}</span>"

    for opcode, a1, a2, b1, b2 in s.get_opcodes():
        A = a[a1:a2]
        B = b[b1:b2]

        if opcode == "equal":
            for x, y in zip(A, B):
                correct.append(span(x, GREEN))
                inputed.append(span(y, GREEN))

        elif opcode == "replace":
            L = max(len(A), len(B))
            for i in range(L):
                ca = A[i] if i < len(A) else "_"
                cb = B[i] if i < len(B) else "_"
                correct.append(span(ca, RED))
                inputed.append(span(cb, RED))

        elif opcode == "delete":
            for ch in A:
                correct.append(span(ch, RED))
                inputed.append(span("_", EMPTY))

        elif opcode == "insert":
            for ch in B:
                correct.append(span("_", EMPTY))
                inputed.append(span(ch, RED))

    return f"""<div style='text-align:center;margin-top:12px;'>
        {''.join(correct)}
        <div style='font-size:13px;margin:3px;'>⬇️</div>
        {''.join(inputed)}
    </div>"""

def create_sentence_with_blank_html(sentence: str, blank_index: int, input_placeholder_id: str) -> str:
    """
    創建一個帶有填空位置的完整句子 HTML,
    其中填空位置會被一個特殊標記替換,稍後會被 Streamlit 輸入框填充
    """
    words = sentence.split()
    
    if 0 <= blank_index < len(words):
        word_to_blank = words[blank_index]
        
        # 檢查是否有標點符號
        trailing_punctuation = ""
        if word_to_blank and not word_to_blank[-1].isalnum():
            trailing_punctuation = word_to_blank[-1]
            
        # 用特殊標記替換該位置
        words[blank_index] = f"{{{{INPUT_PLACEHOLDER}}}}{trailing_punctuation}"
        
    return ' '.join(words)


# --- 初始化 Session State ---
total_questions = len(word_bank)
current_word_hash = hash(tuple((item['word'], item.get('definition_zh')) for item in word_bank))

if "word_bank_hash" not in st.session_state or st.session_state.word_bank_hash != current_word_hash:
    st.session_state.wrong_queue = []
    st.session_state.study_mode = 'LEARNING' 
    st.session_state.sequence_cursor = 0
    st.session_state.current_display_index = 0
    st.session_state.stats = [{"正確": 0, "錯誤": 0} for _ in range(total_questions)]
    st.session_state.history = []
    st.session_state.word_bank_hash = current_word_hash
    st.session_state.last_message = ""      
    st.session_state.gtts_to_play = None    
    st.session_state.local_sound_to_play = ""
    st.toast("新題庫已載入!")
else:
    if "wrong_queue" not in st.session_state: 
        st.session_state.wrong_queue = []
    if "study_mode" not in st.session_state: 
        st.session_state.study_mode = 'LEARNING'
    if "sequence_cursor" not in st.session_state: 
        st.session_state.sequence_cursor = 0
    if "current_display_index" not in st.session_state:
        st.session_state.current_display_index = 0
    if "stats" not in st.session_state: 
        st.session_state.stats = [{"正確": 0, "錯誤": 0} for _ in range(total_questions)]
    if "history" not in st.session_state: 
        st.session_state.history = []
    if "last_message" not in st.session_state:
        st.session_state.last_message = ""
    if "gtts_to_play" not in st.session_state:
        st.session_state.gtts_to_play = None
    if "local_sound_to_play" not in st.session_state:
        st.session_state.local_sound_to_play = ""


def go_next_question():
    if st.session_state.study_mode == 'REVIEW':
        if len(st.session_state.wrong_queue) > 0:
            next_idx = st.session_state.wrong_queue[0]
            st.session_state.current_display_index = next_idx
        else:
            st.session_state.study_mode = 'LEARNING'
            st.session_state.sequence_cursor = 0
            st.session_state.last_message = "🎉 錯題複習完畢!開始新的一輪!"
            st.session_state.current_display_index = 0
    
    elif st.session_state.study_mode == 'LEARNING':
        st.session_state.sequence_cursor += 1
        
        if st.session_state.sequence_cursor < total_questions:
            st.session_state.current_display_index = st.session_state.sequence_cursor
        else:
            is_error_message_present = st.session_state.last_message.startswith("HTML_DIFF_START")
            
            if len(st.session_state.wrong_queue) > 0:
                st.session_state.study_mode = 'REVIEW'
                
                if is_error_message_present: 
                    original_content = st.session_state.last_message[len("HTML_DIFF_START"):-len("HTML_DIFF_END")]
                    parts = original_content.split('|DIFF_SEP|', 1) 
                    
                    if len(parts) == 2:
                        prefix_message = parts[0]
                        diff_html_content = parts[1]
                        new_prefix = f"🔄 一輪結束,進入錯題複習模式!<br><br>{prefix_message.replace('❌ 答錯!', '').replace('⭐️ 跳過!', '')}"
                        st.session_state.last_message = f"HTML_DIFF_START{new_prefix}|DIFF_SEP|{diff_html_content}HTML_DIFF_END"
                    else:
                        st.session_state.last_message = "🔄 一輪結束,進入錯題複習模式!"
                else:
                    st.session_state.last_message = "🔄 一輪結束,進入錯題複習模式!"
                    
                go_next_question()
            else:
                st.session_state.sequence_cursor = 0
                st.session_state.current_display_index = 0
                st.session_state.last_message = "💯 太強了!全部答對,直接開始新的一輪!"


# --- 介面顯示 ---
current_index = st.session_state.current_display_index
current_item = word_bank[current_index]

current_word = current_item["word"]
translation = current_item["translation"]
sentence = current_item["sentence"]
sentence_zh = current_item["sentence_zh"]
definition = current_item.get("definition", "N/A")
definition_zh = current_item.get("definition_zh", "N/A") 
blank_index = current_item.get("blank_index", -1) 

st.markdown("<p style='font-size:22px'><b>🎧 單字 + 句子 發音練習</b></p>", unsafe_allow_html=True)

if st.session_state.local_sound_to_play:
    play_local_audio(st.session_state.local_sound_to_play)
    st.session_state.local_sound_to_play = ""

centralized_gtts_playback()

if st.session_state.last_message:
    message = st.session_state.last_message
    font_size = "12px"
    
    if message.startswith("HTML_DIFF_START") and message.endswith("HTML_DIFF_END"):
        content = message[len("HTML_DIFF_START"):-len("HTML_DIFF_END")]
        parts = content.split('|DIFF_SEP|', 1) 
        
        if len(parts) >= 2:
            prefix_message = parts[0]
            diff_html_content = parts[1]
        else:
            prefix_message = content 
            diff_html_content = "" 
        
        display_message = prefix_message.replace("❌ ", "").replace("⭐️ ", "").replace("🔄 ", "")
        
        html_content = f"""
        <div style="background-color: #ffeaea; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #f00; color: #000;">
            <span style="font-size: {font_size};">{display_message}</span>
            {diff_html_content} 
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    elif "答對了" in message or "複習完畢" in message or "全部答對" in message: 
        display_message = message.replace("✅ ", "").replace("🎉 ", "").replace("💯 ", "")
        html_content = f"""
        <div style="background-color: #e6ffed; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #090; color: #000;">
            <span style="font-size: {font_size};">✅ {display_message}</span> 
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        
    elif "答錯" in message or "跳過" in message or "🔄" in message:
        display_message = message.replace("❌ ", "").replace("⭐️ ", "").replace("🔄 ", "")
        html_content = f"""
        <div style="background-color: #ffeaea; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #f00; color: #000;">
            <span style="font-size: {font_size};">❌ {display_message}</span>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.info(message)
    
    st.session_state.last_message = ""
        
if st.session_state.study_mode == 'REVIEW':
    st.warning(f"🔥 錯題複習模式 (剩餘 **{len(st.session_state.wrong_queue)}** 題)")

col_img, col_btn_word, col_btn_sentence, col_btn_definition = st.columns([1, 2, 2, 2]) 

with col_img:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "Dolingo.jpg") 
        st.image(image_path, width=70) 
    except Exception as e:
        pass 

with col_btn_word:
    if st.button("▶ 單字(英)"):
        set_gtts_to_play(current_word, 'en')
    
with col_btn_sentence:
    if st.button("▶ 例句(英)"):
        set_gtts_to_play(sentence, 'en')
    
with col_btn_definition: 
    if st.button("▶ 定義(英)"):
        set_gtts_to_play(definition, 'en')


# 創建帶有填空標記的句子
sentence_template = create_sentence_with_blank_html(sentence, blank_index, "input_box")

# 分割句子,找出輸入框的位置
parts = sentence_template.split("{{INPUT_PLACEHOLDER}}")

# --- 使用表單 ---
input_key = f"input_{current_index}_{st.session_state.study_mode}" 

with st.form(key=f"form_{current_index}", clear_on_submit=True):
    
    # 顯示完整的句子,輸入框嵌入其中
    if len(parts) == 2:
        # 句子前半部分
        if parts[0].strip():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 8px; padding: 10px 20px; min-height: 60px;">
                <span style="font-size: 36px; font-weight: 1000; color: #FFD700; line-height: 1.5;">
                    {parts[0]}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # 輸入框(不加提示)
        user_input = st.text_input("", key=input_key, autocomplete="off", label_visibility="collapsed", placeholder="輸入單字...")
        
        # 句子後半部分
        if parts[1].strip():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 8px; padding: 10px 20px; margin-top: 5px; min-height: 60px;">
                <span style="font-size: 36px; font-weight: 1000; color: #FFD700; line-height: 1.5;">
                    {parts[1]}
                </span>
            </div>
            """, unsafe_allow_html=True)
    else:
        user_input = st.text_input("", key=input_key, autocomplete="off", label_visibility="collapsed", placeholder="輸入單字...")
    
    submitted = st.form_submit_button("✓ 檢查答案", use_container_width=True, type="primary")

    if submitted:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_text = user_input.strip().lower()
        is_correct = (user_text == current_word.lower())

        if is_correct:
            st.session_state.stats[current_index]["正確"] += 1
            st.session_state.last_message = "✅ 答對了!" 
            if current_index in st.session_state.wrong_queue:
                st.session_state.wrong_queue.remove(current_index) 
            
            st.session_state.local_sound_to_play = "audio/duolingo_style_correct.mp3" 
            go_next_question()

        else:
            st.session_state.stats[current_index]["錯誤"] += 1
            diff_html = get_diff_html(current_word, user_text)
            msg_prefix = f"❌ 答錯!正確答案是:**{current_word}** (你的輸入:**{user_text}**)" if user_text else f"⭐️ 跳過!正確答案是:**{current_word}**"
            st.session_state.last_message = f"HTML_DIFF_START{msg_prefix}|DIFF_SEP|{diff_html}HTML_DIFF_END"

            if current_index not in st.session_state.wrong_queue:
                st.session_state.wrong_queue.append(current_index) 
            
            if st.session_state.study_mode == 'REVIEW' and current_index in st.session_state.wrong_queue:
                if st.session_state.wrong_queue[0] == current_index:
                    item = st.session_state.wrong_queue.pop(0)
                    st.session_state.wrong_queue.append(item)
            
            st.session_state.local_sound_to_play = "audio/dong_dong.mp3" 
            go_next_question()

        st.session_state.history.append({
            "模式": "複習" if st.session_state.study_mode == 'REVIEW' else "一般",
            "題號": current_index + 1,
            "單字": current_word,
            "輸入": user_input,
            "結果": "正確" if is_correct else "錯誤",
            "時間": now_str
        })

        st.rerun()

# --- 【新增】強力自動聚焦腳本 ---
st.components.v1.html("""
<script>
function focusInput() {
    const iframe = window.parent.document.querySelector('iframe[title="streamlit_app"]') || 
                   window.parent.document.querySelector('iframe');
    
    let targetDoc = window.parent.document;
    if (iframe && iframe.contentDocument) {
        targetDoc = iframe.contentDocument;
    }
    
    const input = targetDoc.querySelector('input[type="text"]');
    if (input) {
        input.focus();
        input.select();
        return true;
    }
    
    // 直接在父文檔查找
    const directInput = window.parent.document.querySelector('input[type="text"]');
    if (directInput) {
        directInput.focus();
        directInput.select();
        return true;
    }
    
    return false;
}

// 多次嘗試聚焦
setTimeout(focusInput, 50);
setTimeout(focusInput, 150);
setTimeout(focusInput, 300);
setTimeout(focusInput, 500);
setTimeout(focusInput, 800);
setTimeout(focusInput, 1200);

// 監聽 DOM 變化
const observer = new MutationObserver(focusInput);
if (window.parent.document.body) {
    observer.observe(window.parent.document.body, {
        childList: true,
        subtree: true
    });
}

// 定期檢查
setInterval(function() {
    const activeEl = window.parent.document.activeElement;
    if (!activeEl || activeEl.tagName !== 'INPUT') {
        focusInput();
    }
}, 200);
</script>
""", height=0)

st.write(f"中文單字翻譯:**{translation}**")
st.write(f"**中文翻譯:** *{sentence_zh}*")
st.markdown(f"**英文定義:** *{definition}*") 
st.write(f"**中文定義:** *{definition_zh}*") 
       

st.sidebar.header("📊 練習進度統計")
st.sidebar.write(f"目前模式:**{st.session_state.study_mode}**")
st.sidebar.write(f"待複習錯題數:**{len(st.session_state.wrong_queue)}**")

st.sidebar.subheader("📈 單字答題統計")
stats_list = []
for i, item in enumerate(word_bank):
    s = st.session_state.stats[i]
    total_try = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_try}" if total_try > 0 else "0/0"
    
    status_light = "⚪"
    
    if i in st.session_state.wrong_queue:
        status_light = "🔴" 
    elif s["正確"] > 0:
        status_light = "🟢" 
    elif s["錯誤"] > 0 and s["正確"] == 0:
        status_light = "🟡" 
        
    stats_list.append({
        "狀態": status_light,
        "題號": i + 1,
        "單字": item["word"],
        "正確率": rate
    })
st.sidebar.dataframe(pd.DataFrame(stats_list), use_container_width=True)

st.sidebar.subheader("📝 歷史紀錄")
if st.session_state.history:
    st.sidebar.dataframe(pd.DataFrame(st.session_state.history[::-1]), use_container_width=True)