import streamlit as st
import datetime
import pandas as pd
import os # 用來讀取本地 mp3 檔案

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
        st.caption(f"請確保您的音檔檔名符合格式，例如：{os.path.basename(filepath)}")
        return
    try:
        with open(filepath, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"讀取音檔時發生錯誤：{e}")

# --- 初始化 Session State ---
total_questions = len(word_bank)
current_word_hash = hash(tuple(item['word'] for item in word_bank))

if "word_bank_hash" not in st.session_state or st.session_state.word_bank_hash != current_word_hash:
    st.session_state.wrong_queue = []
    st.session_state.study_mode = 'LEARNING' 
    st.session_state.sequence_cursor = 0
    st.session_state.current_display_index = 0
    st.session_state.stats = [{"正確": 0, "錯誤": 0} for _ in range(total_questions)]
    st.session_state.history = []
    st.session_state.word_bank_hash = current_word_hash
    st.session_state.last_message = "" # 【新增】用於儲存最新的結果訊息
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

# 組合音檔路徑
base_name = f"{current_index + 1:02d}_{current_word}"
word_audio_path    = os.path.join(AUDIO_DIR, f"{base_name}_word_en.mp3")
sent_en_audio_path = os.path.join(AUDIO_DIR, f"{base_name}_sent_en.mp3")
sent_zh_audio_path = os.path.join(AUDIO_DIR, f"{base_name}_sent_zh.mp3")


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

st.markdown("<p style='font-size:18px'>📌 發音按鈕 (單字 / 英文例句 / 中文翻譯)</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>✏️ 單字測驗</p>", unsafe_allow_html=True)

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

# 顯示文字
st.write(f"中文單字翻譯：**{translation}**")
st.write(f"英文例句：*{sentence}*")
st.write(f"中文翻譯：*{sentence_zh}*")

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

# --- 側邊欄統計 ---
st.sidebar.header("📊 練習進度統計")
st.sidebar.write(f"目前模式：**{st.session_state.study_mode}**")
st.sidebar.write(f"待複習錯題數：{len(st.session_state.wrong_queue)}")

st.sidebar.subheader("📈 單字答題統計")
stats_list = []
for i, item in enumerate(word_bank):
    s = st.session_state.stats[i]
    total_try = s["正確"] + s["錯誤"]
    rate = f"{s['正確']}/{total_try}" if total_try > 0 else "0/0"
    
    # --- 狀態燈邏輯 (使用 002_ch_u8.py 的思路，基於 index 和 stats 判斷) ---
    status_light = "⚪" # 預設: 尚未作答 (或還沒進入該輪)
    
    # 1. 🔴 錯題隊列中 (最高優先級)
    if i in st.session_state.wrong_queue:
        status_light = "🔴" 
    
    # 2. 🟢 已經正確答對過 (至少答對一次，且不在錯題隊列中)
    elif s["正確"] > 0:
        status_light = "🟢" 
    
    # 3. 🟡 曾答錯，待複習 (曾有錯誤記錄，但還沒有正確記錄，且不在隊列中)
    elif s["錯誤"] > 0 and s["正確"] == 0:
        status_light = "🟡" 
        
    # 否則，保持 ⚪
    
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