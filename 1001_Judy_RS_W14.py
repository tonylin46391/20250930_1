import streamlit as st
import datetime
import pandas as pd
# 引入 os 用來檢查本地音檔路徑
import os 
# 引入 gTTS 來生成語音，以及 io 來處理音訊數據流
from gtts import gTTS
import io
# 【新增】引入 difflib 進行字串差異比對
import difflib 

word_bank = [
    {
        "word": "mysterious",
        "translation": "神秘的；難以理解的",
        "sentence": "Nobody knows what is in the mysterious box.",
        "sentence_zh": "沒有人知道這個神秘的箱子裡裝了什麼。",
        "definition": "Something that is mysterious is not fully understood or explainable.",
        "definition_zh": "神秘的事物是沒有被完全理解或無法解釋的。"
    },
    {
        "word": "matted",
        "translation": "糾結的；雜亂的",
        "sentence": "The dog's fur was so matted that we had to cut all the dog's fur off.",
        "sentence_zh": "這隻狗的毛髮糾結得太嚴重了，以至於我們不得不全部剪掉。",
        "definition": "Something that is matted is a tangled mess.",
        "definition_zh": "糾結的事物是雜亂無章的。"
    },
    {
        "word": "tendrils",
        "translation": "（植物的）捲鬚",
        "sentence": "The plant had long tendrils that wrapped around the other plants.",
        "sentence_zh": "這株植物有長長的捲鬚纏繞在其他植物上。",
        "definition": "Tendrils are thin sections of plants that often twist around another plant.",
        "definition_zh": "捲鬚是植物的細長部分，通常會纏繞在另一株植物上。"
    },
    {
        "word": "fastenings",
        "translation": "扣件；緊固件（將物體固定在一起的東西）",
        "sentence": "Dad repaired the fastenings that attached the door to the frame.",
        "sentence_zh": "爸爸修理了將門固定在門框上的扣件。",
        "definition": "Fastenings attach objects to other things. (Something that put two things together.)",
        "definition_zh": "扣件是用來將物體附著到其他東西上的。（將兩樣東西放在一起的東西。）"
    },
    {
        "word": "awakening",
        "translation": "喚醒；醒來",
        "sentence": "The child began awakening at sunrise.",
        "sentence_zh": "孩子在日出時開始醒來。",
        "definition": "If you are awakening someone, you are waking him or her from sleep.",
        "definition_zh": "如果你正在喚醒某人，你就是在叫醒他或她睡覺。"
    },
    {
        "word": "mansion",
        "translation": "大廈；豪宅",
        "sentence": "England has many old mansions in the countryside.",
        "sentence_zh": "英國的鄉村有許多古老的豪宅。",
        "definition": "A large, impressive house. (Very big house)",
        "definition_zh": "一棟大型且令人印象深刻的房子。（非常大的房子）"
    },
    {
        "word": "robin",
        "translation": "知更鳥",
        "sentence": "The robin twittered happily in the garden.",
        "sentence_zh": "知更鳥在花園裡快樂地鳴叫。",
        "definition": "A small brown European bird with a red breast.",
        "definition_zh": "一種胸部為紅色的歐洲小型棕色鳥類。"
    },
    {
        "word": "orchard",
        "translation": "果園",
        "sentence": "The orchard is full of trees growing different kinds of apples and pears.",
        "sentence_zh": "果園裡種滿了不同種類的蘋果樹和梨樹。",
        "definition": "A piece of land in which fruit trees are grown. (where fruit are grown)",
        "definition_zh": "一片種植果樹的土地。（種植水果的地方）"
    },
    {
        "word": "arches",
        "translation": "拱門；拱形結構",
        "sentence": "There is a bridge with three arches near my house.",
        "sentence_zh": "我家附近有一座有三個拱門的橋。",
        "definition": "Curved structures that support the weight of something above it.",
        "definition_zh": "支撐其上方物體重量的彎曲結構。"
    },
    {
        "word": "mantle",
        "translation": "覆蓋物；地幔（在這裡指覆蓋物）",
        "sentence": "In winter I love to see hills with a mantle of snow.",
        "sentence_zh": "在冬天，我喜歡看到山丘上覆蓋著一層雪。",
        "definition": "A layer of something that covers a surface.",
        "definition_zh": "覆蓋在某個表面上的一層東西。"
    }
]

# --- 播放函式 (處理本地檔案) ---

def play_local_audio(filename: str):
    """
    播放本地上傳的音訊檔案，利用 Streamlit 的 st.audio。
    """
    if not os.path.exists(filename):
        st.warning(f"⚠ 找不到音訊檔案：'{filename}'，請確認檔案是否存在。")
        return
    
    try:
        # 讀取檔案為 bytes 並讓 Streamlit 播放
        audio_bytes = open(filename, 'rb').read()
        # 加上 autoplay=True 使其在頁面加載時自動播放
        
        # 使用 st.empty() 容器來避免佔用頁面佈局
        placeholder = st.empty()
        with placeholder:
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
            
    except Exception as e:
        st.error(f"播放本地音訊時發生錯誤：{e}")


# --- 播放函式 (處理 gTTS) ---

def set_gtts_to_play(text: str, lang: str):
    """
    將要播放的 gTTS 內容儲存到 Session State 中，並觸發重新執行。
    """
    if text:
        st.session_state.gtts_to_play = (text, lang)
        st.rerun() # 立即重新執行，在頁面頂部播放
    else:
        st.warning("⚠ 播放內容為空，無法生成語音。")
        
def centralized_gtts_playback():
    """
    在頁面頂部集中處理 gTTS 音訊播放。
    """
    if st.session_state.gtts_to_play is not None:
        text, lang = st.session_state.gtts_to_play
        st.session_state.gtts_to_play = None # 播放前清除狀態
        
        # 使用 st.empty() 容器，播放器會被渲染在頂部且不影響下方佈局
        placeholder = st.empty() 
        
        try:
            tts = gTTS(text=text, lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            with placeholder:
                st.audio(fp, format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.error(f"生成語音時發生錯誤：{e}")

# --- 【修改】差異化顯示函式 (已調整字體大小與錯誤顏色) ---
def get_diff_html(a: str, b: str) -> str:
    """
    使用 difflib.SequenceMatcher 比對兩個單字 'a' (正確答案) 和 'b' (使用者輸入)，
    並生成帶有顏色標記的 HTML 字串，以實現圖片中的上下比對效果。
    """
    # 將兩字串轉為小寫進行比對
    a = a.lower()
    b = b.lower()
    s = difflib.SequenceMatcher(None, a, b)
    
    correct_html = ""
    input_html = ""

    # 🌟 修改點: 使用您指定的深紅色 #b22222 (FireBrick)
    RED_BG = "background-color: #b22222; color: #ffffff" # **注意：深紅色背景建議搭配白色字體 #ffffff 確保可讀性**
    GREEN_BG = "background-color: #ddffdd" # 綠色保持不變，表示正確

    # 遍歷操作碼 (opcodes)
    for opcode, a_start, a_end, b_start, b_end in s.get_opcodes():
        sub_a = a[a_start:a_end]
        sub_b = b[b_start:b_end]

        if opcode == 'equal':
            # 兩邊相同 (綠色背景)
            correct_html += f"<span style='{GREEN_BG}'>{sub_a}</span>"
            input_html += f"<span style='{GREEN_BG}'>{sub_b}</span>"
        elif opcode == 'delete':
            # 正確答案有，使用者輸入刪了 (正確答案標深紅色)
            correct_html += f"<span style='{RED_BG}'>{sub_a}</span>"
            # 使用者輸入在這裡沒有對應的字元，所以留空
        elif opcode == 'insert':
            # 正確答案沒有，使用者輸入新增了 (使用者輸入標深紅色)
            input_html += f"<span style='{RED_BG}'>{sub_b}</span>"
            # 正確答案在這裡沒有對應的字元，所以留空
        elif opcode == 'replace':
            # 兩邊發生替換
            # 正確答案中被替換的部分 (標深紅色)
            correct_html += f"<span style='{RED_BG}'>{sub_a}</span>"
            # 使用者輸入中替換進來的部分 (標深紅色)
            input_html += f"<span style='{RED_BG}'>{sub_b}</span>"

    # 包裝成帶有居中和字體大小的 div，模擬圖片效果
    style = "display: inline-block; padding: 2px 0; border-radius: 3px; font-size: 26px; line-height: 1.5; font-family: monospace; letter-spacing: 2px;"
    
    final_html = f"""
    <div style='text-align: center; margin-top: 15px; margin-bottom: 5px;'>
        <div style='{style}'>{correct_html}</div>
        <div style='font-size: 20px; line-height: 1.5; margin: 5px 0;'>⬇️</div>
        <div style='{style}'>{input_html}</div>
    </div>
    """
    
    return final_html
# ----------------------------------------
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
    st.session_state.last_message = ""      # 用於儲存最新的結果訊息
    st.session_state.gtts_to_play = None    # <-- gTTS 播放狀態
    st.session_state.local_sound_to_play = "" # <-- 本地音效播放狀態
    st.toast("新題庫已載入！")
else:
    # 確保所有變數都存在
    if "last_message" not in st.session_state:
        st.session_state.last_message = ""
    if "gtts_to_play" not in st.session_state:
        st.session_state.gtts_to_play = None
    if "local_sound_to_play" not in st.session_state:
        st.session_state.local_sound_to_play = ""


# --- 邏輯控制函式 (保持不變) ---

def go_next_question():
    """
    更新狀態以指向下一題。
    """
    
    # 邏輯 A: 複習模式 (Review Mode)
    if st.session_state.study_mode == 'REVIEW':
        if len(st.session_state.wrong_queue) > 0:
            next_idx = st.session_state.wrong_queue[0]
            st.session_state.current_display_index = next_idx
        else:
            # 錯題都複習完了 -> 回到新一輪
            st.session_state.study_mode = 'LEARNING'
            st.session_state.sequence_cursor = 0
            st.session_state.last_message = "🎉 錯題複習完畢！開始新的一輪！"
            st.session_state.current_display_index = 0
    
    # 邏輯 B: 順序學習模式 (Learning Mode)
    elif st.session_state.study_mode == 'LEARNING':
        
        st.session_state.sequence_cursor += 1
        
        if st.session_state.sequence_cursor < total_questions:
            st.session_state.current_display_index = st.session_state.sequence_cursor
        
        else:
            # --- 處理一輪結束 ---
            
            if len(st.session_state.wrong_queue) > 0:
                st.session_state.study_mode = 'REVIEW'
                st.session_state.last_message = "🔄 一輪結束，進入錯題複習模式！"
                go_next_question()
            else:
                st.session_state.sequence_cursor = 0
                st.session_state.current_display_index = 0
                st.session_state.last_message = "💯 太強了！全部答對，直接開始新的一輪！"


# --- 介面顯示 ---

# 確保一開始有題目
current_index = st.session_state.current_display_index
current_item = word_bank[current_index]

# 取出資料
current_word = current_item["word"]
translation = current_item["translation"]
sentence = current_item["sentence"]
sentence_zh = current_item["sentence_zh"]
definition = current_item.get("definition", "N/A")
definition_zh = current_item.get("definition_zh", "N/A") 


# --- 標題與狀態顯示 ---
st.markdown("<p style='font-size:22px'><b>🎧 單字 + 句子 發音練習</b></p>", unsafe_allow_html=True)

# *** 頁面頂部：集中播放音效 (本地檔案) ***
if st.session_state.local_sound_to_play:
    play_local_audio(st.session_state.local_sound_to_play)
    st.session_state.local_sound_to_play = ""

# *** 頁面頂部：集中播放音效 (gTTS) ***
centralized_gtts_playback()


# 顯示最新的結果訊息
if st.session_state.last_message:
    message = st.session_state.last_message
    
    font_size = "13px" 
    
    # --- 【修改】處理差異化 HTML 顯示 ---
    if message.startswith("HTML_DIFF_START") and message.endswith("HTML_DIFF_END"):
        
        # 提取前綴訊息和 HTML 內容
        content = message[len("HTML_DIFF_START"):-len("HTML_DIFF_END")]
        
        # 以差異 HTML 的開頭作為分隔
        parts = content.split('<div style=\'text-align: center') 
        prefix_message = parts[0]
        diff_html_content = '<div style=\'text-align: center' + parts[1] # 重新組合 HTML
        
        # 移除訊息中 Streamlit 內建的圖示
        display_message = prefix_message.replace("❌ ", "").replace("⏭️ ", "").replace("🔄 ", "")
        
        # 創建完整的 HTML 內容，結合錯誤提示框和差異化顯示
        html_content = f"""
        <div style="background-color: #ffeaea; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #f00; color: #000;">
            <span style="font-size: {font_size};">❌ {display_message}</span>
            {diff_html_content} 
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    # --------------------------------------

    elif "答對了" in message or "複習完畢" in message or "全部答對" in message: 
        
        # 移除訊息中 Streamlit 內建的圖示
        display_message = message.replace("✅ ", "").replace("🎉 ", "").replace("💯 ", "")

        html_content = f"""
        <div style="background-color: #e6ffed; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #090; color: #000;">
            <span style="font-size: {font_size};">✅ {display_message}</span> 
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        
    elif "答錯" in message or "跳過" in message or "🔄" in message:
        
        # 移除訊息中 Streamlit 內建的圖示
        display_message = message.replace("❌ ", "").replace("⏭️ ", "").replace("🔄 ", "")
        
        html_content = f"""
        <div style="background-color: #ffeaea; border-radius: 0.25rem; padding: 1rem; border-left: 0.5rem solid #f00; color: #000;">
            <span style="font-size: {font_size};">❌ {display_message}</span>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    else:
        st.info(message)
    
    # 確保訊息在顯示後被清除
    st.session_state.last_message = ""
        
# --- 狀態模式顯示 ---
if st.session_state.study_mode == 'REVIEW':
    st.warning(f"🔥 錯題複習模式 (剩餘 {len(st.session_state.wrong_queue)} 題)")
else:
    display_progress = st.session_state.sequence_cursor 
    if display_progress == total_questions: display_progress = 0
    st.info(f"📖 順序學習模式 (進度 {display_progress + 1} / {total_questions})")

#st.markdown("<p style='font-size:18px'>📌 發音按鈕 (單字 / 英文例句 / 中文翻譯 / 英文定義 / 中文定義)</p>", unsafe_allow_html=True)
#st.markdown("<p style='font-size:18px'>✏️ 單字測驗</p>", unsafe_allow_html=True)

# --- 發音按鈕 (使用 set_gtts_to_play) ---
col1, col2, col3, col4, col5 = st.columns(5) 
with col1:
    if st.button("▶ 單字（英）"):
        set_gtts_to_play(current_word, 'en')
with col2:
    if st.button("▶ 例句（英）"):
        set_gtts_to_play(sentence, 'en')
#with col3:
#    if st.button("▶ 例句（中）"):
#        set_gtts_to_play(sentence_zh, 'zh-tw')
with col3: 
    if st.button("▶ 定義（英）"):
        set_gtts_to_play(definition, 'en')
#with col5: 
#    if st.button("▶ 定義（中）"):
#        set_gtts_to_play(definition_zh, 'zh-tw')


# 顯示文字 (保持不變)
st.write(f"中文單字翻譯：**{translation}**")
st.write(f"**英文例句：** *{sentence}*")
st.write(f"**中文翻譯：** *{sentence_zh}*")
st.markdown(f"**英文定義：** *{definition}*") 
st.write(f"**中文定義：** *{definition_zh}*") 


# --- 單字答題表單 ---
input_key = f"input_{current_index}_{st.session_state.study_mode}" 

with st.form(key=f"form_{current_index}", clear_on_submit=True):
    user_input = st.text_input("請輸入單字 (輸入完按 Enter 即可)", key=input_key, autocomplete="off")
    submitted = st.form_submit_button("提交答案 (或按 Enter)")
    
    if submitted:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_text = user_input.strip().lower()
        is_correct = (user_text == current_word.lower())

        # --- 答案處理與狀態更新 ---
        
        if is_correct:
            st.session_state.stats[current_index]["正確"] += 1
            st.session_state.last_message = "✅ 答對了！" 
            if current_index in st.session_state.wrong_queue:
                st.session_state.wrong_queue.remove(current_index) 
            
            # *** 設定正確音效路徑 (本地音效) ***
            st.session_state.local_sound_to_play = "audio/duolingo_style_correct.mp3" 
            
            # 立即跳下一題 (無延遲)
            go_next_question()

        else:
            st.session_state.stats[current_index]["錯誤"] += 1
            
            # --- 【修改】加入差異化顯示 ---
            # 1. 計算並取得差異 HTML 內容
            diff_html = get_diff_html(current_word, user_text)
            
            # 2. 準備顯示訊息 (將差異 HTML 儲存到 last_message)
            # 使用一個特殊的標籤來指示結果顯示區域需要渲染 HTML
            msg_prefix = f"❌ 答錯！正確答案是：**{current_word}** (你的輸入：**{user_text}**)" if user_text else f"⏭️ 跳過！正確答案是：**{current_word}**"
            st.session_state.last_message = f"HTML_DIFF_START{msg_prefix}{diff_html}HTML_DIFF_END"
            # --------------------------------

            if current_index not in st.session_state.wrong_queue:
                st.session_state.wrong_queue.append(current_index) 
            
            if st.session_state.study_mode == 'REVIEW' and current_index in st.session_state.wrong_queue:
                if st.session_state.wrong_queue[0] == current_index:
                    item = st.session_state.wrong_queue.pop(0)
                    st.session_state.wrong_queue.append(item)
            
            # *** 設定錯誤音效路徑 (本地音效) ***
            st.session_state.local_sound_to_play = "audio/dong_dong.mp3" 

            # 立即跳下一題 (無延遲)
            go_next_question()


        # 紀錄歷史
        st.session_state.history.append({
            "模式": "複習" if st.session_state.study_mode == 'REVIEW' else "一般",
            "題號": current_index + 1,
            "單字": current_word,
            "輸入": user_input,
            "結果": "正確" if is_correct else "錯誤",
            "時間": now_str
        })

        st.rerun() # 重新執行腳本

# --- 側邊欄統計 (保持不變) ---
st.sidebar.header("📊 練習進度統計")
st.sidebar.write(f"目前模式：**{st.session_state.study_mode}**")
st.sidebar.write(f"待複習錯題數：{len(st.session_state.wrong_queue)}")

st.sidebar.subheader("📈 單字答題統計")
stats_list = []
for i, item in enumerate(word_bank):
    s = st.session_state.stats[i]
    total_try = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_try}" if total_try > 0 else "0/0"
    
    # --- 狀態燈邏輯 ---
    status_light = "⚪" # 預設: 尚未作答
    
    # 1. 🔴 錯題隊列中 (最高優先級)
    if i in st.session_state.wrong_queue:
        status_light = "🔴" 
    
    # 2. 🟢 已經正確答對過 (至少答對一次，且不在錯題隊列中)
    elif s["正確"] > 0:
        status_light = "🟢" 
    
    # 3. 🟡 曾答錯，待複習 (曾有錯誤記錄，但還沒有正確記錄，且不在隊列中)
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