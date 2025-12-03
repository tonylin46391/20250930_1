import streamlit as st
import datetime
import pandas as pd
# 移除 os 函式庫，因為不再讀取本地檔案
# import os 

# 引入 gTTS 來生成語音，以及 io 來處理音訊數據流
from gtts import gTTS
import io

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



# 移除所有關於本地音檔路徑和檔案讀取的程式碼

def play_audio_gtts(text: str, lang: str):
    """
    使用 gTTS 生成 MP3 音訊並直接在 Streamlit 中播放。
    音訊內容儲存在 BytesIO 中，不產生實體檔案。
    """
    if not text:
        st.warning("⚠ 播放內容為空，無法生成語音。")
        return
        
    try:
        # 1. 產生 gTTS 物件
        tts = gTTS(text=text, lang=lang)
        
        # 2. 使用 BytesIO 儲存生成的音訊
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # 3. 在 Streamlit 中播放
        st.audio(fp, format="audio/mp3")
    except Exception as e:
        st.error(f"生成語音時發生錯誤：{e}")


# --- 初始化 Session State ---
total_questions = len(word_bank)
# 確保 hash 包含新的欄位，讓新的 word_bank 會觸發初始化
current_word_hash = hash(tuple((item['word'], item.get('definition_zh')) for item in word_bank))

if "word_bank_hash" not in st.session_state or st.session_state.word_bank_hash != current_word_hash:
    st.session_state.wrong_queue = []
    st.session_state.study_mode = 'LEARNING' 
    st.session_state.sequence_cursor = 0
    st.session_state.current_display_index = 0
    st.session_state.stats = [{"正確": 0, "錯誤": 0} for _ in range(total_questions)]
    st.session_state.history = []
    st.session_state.word_bank_hash = current_word_hash
    st.session_state.last_message = "" # 用於儲存最新的結果訊息
    st.toast("新題庫已載入！")
else:
    # 確保 last_message 存在
    if "last_message" not in st.session_state:
        st.session_state.last_message = ""

# --- 邏輯控制函式 ---

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
        
        # 1. 先將游標推進
        st.session_state.sequence_cursor += 1
        
        # 2. 檢查推進後的游標是否還在範圍內
        if st.session_state.sequence_cursor < total_questions:
            # 3. 顯示新游標所指向的題目
            st.session_state.current_display_index = st.session_state.sequence_cursor
        
        # 4. 游標已到達或超過範圍 (一輪結束)
        else:
            # --- 處理一輪結束 ---
            
            if len(st.session_state.wrong_queue) > 0:
                st.session_state.study_mode = 'REVIEW'
                st.session_state.last_message = "🔄 一輪結束，進入錯題複習模式！"
                # 遞迴呼叫自己，讓它立刻抓取第一題錯題
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


# 移除所有關於本地音檔路徑的程式碼

# --- 標題與狀態顯示 ---
st.markdown("<p style='font-size:22px'><b>🎧 單字 + 句子 發音練習</b></p>", unsafe_allow_html=True)

# 顯示最新的結果訊息
if st.session_state.last_message:
    # 判斷訊息類型並用不同顏色顯示
    if "答對了" in st.session_state.last_message or "複習完畢" in st.session_state.last_message or "全部答對" in st.session_state.last_message:
        st.success(st.session_state.last_message)
    elif "答錯" in st.session_state.last_message or "跳過" in st.session_state.last_message:
        # 使用 st.error 模擬您的圖片效果 (帶有紅X)
        st.error(st.session_state.last_message)
    else:
        st.info(st.session_state.last_message)
    
    # 確保訊息在顯示後被清除，避免重複顯示
    st.session_state.last_message = "" 


if st.session_state.study_mode == 'REVIEW':
    st.warning(f"🔥 錯題複習模式 (剩餘 {len(st.session_state.wrong_queue)} 題)")
else:
    display_progress = st.session_state.sequence_cursor 
    if display_progress == total_questions: display_progress = 0
    st.info(f"📖 順序學習模式 (進度 {display_progress + 1} / {total_questions})")

# 更新按鈕標題，包含定義
st.markdown("<p style='font-size:18px'>📌 發音按鈕 (單字 / 英文例句 / 中文翻譯 / 英文定義 / 中文定義)</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>✏️ 單字測驗</p>", unsafe_allow_html=True)

# --- 五個發音按鈕 (使用 gTTS 替換 play_audio) ---
col1, col2, col3, col4, col5 = st.columns(5) 
with col1:
    if st.button("▶ 單字（英）"):
        # 呼叫 gTTS 播放單字 (英文 'en')
        play_audio_gtts(current_word, 'en')
with col2:
    if st.button("▶ 例句（英）"):
        # 呼叫 gTTS 播放英文例句 (英文 'en')
        play_audio_gtts(sentence, 'en')
with col3:
    if st.button("▶ 例句（中）"):
        # 呼叫 gTTS 播放中文例句 (中文 'zh-tw')
        play_audio_gtts(sentence_zh, 'zh-tw')
with col4: # 英文定義按鈕
    if st.button("▶ 定義（英）"):
        # 呼叫 gTTS 播放英文定義 (英文 'en')
        play_audio_gtts(definition, 'en')
with col5: # 中文定義按鈕
    if st.button("▶ 定義（中）"):
        # 呼叫 gTTS 播放中文定義 (中文 'zh-tw')
        play_audio_gtts(definition_zh, 'zh-tw')


# 顯示文字
st.write(f"中文單字翻譯：**{translation}**")
st.write(f"英文例句：*{sentence}*")
st.write(f"中文翻譯：*{sentence_zh}*")
st.markdown(f"**英文定義：** *{definition}*") 
st.write(f"中文定義：*{definition_zh}*") 


# --- 單字答題表單 (此處不變) ---
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
            st.session_state.last_message = "✅ 答對了！" # 儲存正確訊息
            if current_index in st.session_state.wrong_queue:
                st.session_state.wrong_queue.remove(current_index) # 答對後移出錯題隊列
        else:
            st.session_state.stats[current_index]["錯誤"] += 1
            msg = f"❌ 答錯！正確答案是：{current_word}" if user_text else f"⏭️ 跳過！正確答案是：{current_word}"
            st.session_state.last_message = msg # 儲存錯誤訊息
            
            if current_index not in st.session_state.wrong_queue:
                st.session_state.wrong_queue.append(current_index) # 答錯後加入錯題隊列
            
            if st.session_state.study_mode == 'REVIEW' and current_index in st.session_state.wrong_queue:
                if st.session_state.wrong_queue[0] == current_index:
                    item = st.session_state.wrong_queue.pop(0)
                    st.session_state.wrong_queue.append(item)


        # 紀錄歷史
        st.session_state.history.append({
            "模式": "複習" if st.session_state.study_mode == 'REVIEW' else "一般",
            "題號": current_index + 1,
            "單字": current_word,
            "輸入": user_input,
            "結果": "正確" if is_correct else "錯誤",
            "時間": now_str
        })

        go_next_question()
        st.rerun()

# --- 側邊欄統計 (此處不變) ---
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