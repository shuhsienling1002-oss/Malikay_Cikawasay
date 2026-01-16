import streamlit as st
import datetime
import time

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="Malikay工作室",
    page_icon="🌿",
    layout="centered"
)

# --- 2. 系統邏輯核心 (不變的物理內核) ---
DIAGNOSIS_DB = {
    "弦脈 (Wiry)": {
        "pattern": "肝氣鬱結 / 自律神經張力過高",
        "strategy": "疏肝理氣，解痙攣",
        "acupoints": [
            {"name": "太衝 (LR3)", "loc": "足背大拇趾與二趾縫後凹陷", "method": "瀉法 (逆時針重揉) 3分鐘"},
            {"name": "內關 (PC6)", "loc": "手腕橫紋上三指", "method": "平補平瀉 2分鐘"}
        ]
    },
    "滑脈 (Slippery)": {
        "pattern": "痰濕 / 食積 / 消化系統負載過重",
        "strategy": "健脾祛濕，化痰",
        "acupoints": [
            {"name": "豐隆 (ST40)", "loc": "小腿外側中點", "method": "重按 (強刺激) 3分鐘"},
            {"name": "中脘 (CV12)", "loc": "肚臍上四寸", "method": "溫灸或順時針揉 5分鐘"}
        ]
    },
    "沉細 (Deep & Thready)": {
        "pattern": "腎氣不足 / 氣血兩虛 / 系統能量低",
        "strategy": "補益氣血，提升基礎代謝",
        "acupoints": [
            {"name": "足三里 (ST36)", "loc": "膝眼下四指", "method": "補法 (順時針輕揉/灸) 5分鐘"},
            {"name": "氣海 (CV6)", "loc": "肚臍下1.5寸", "method": "靜按或熱敷"}
        ]
    },
    "數脈 (Rapid)": {
        "pattern": "熱證 / 發炎反應 / 代謝亢進",
        "strategy": "清熱涼血，降低系統熵值",
        "acupoints": [
            {"name": "曲池 (LI11)", "loc": "手肘橫紋外側端", "method": "瀉法 (強刺激) 2分鐘"},
            {"name": "合谷 (LI4)", "loc": "虎口處", "method": "間歇點按"}
        ]
    },
    "虛脈 (Empty)": {
        "pattern": "氣血虧虛 / 循環動力不足",
        "strategy": "大補元氣，激活幫浦",
        "acupoints": [
            {"name": "百會 (GV20)", "loc": "頭頂正中", "method": "輕按 1分鐘"},
            {"name": "關元 (CV4)", "loc": "肚臍下三寸", "method": "長時間溫灸"}
        ]
    }
}

# --- 3. 登入系統邏輯 ---
def check_password():
    """驗證密碼函數"""
    def password_entered():
        if st.session_state["password"] == "1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 安全起見，不儲存密碼明文
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 首次進入，顯示登入介面
        st.title("🔒 Malikay工作室 - 會員入口")
        st.markdown("### 請輸入訪問密碼")
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        st.info("ℹ️ 會員請向三一協會索取密碼")
        return False
    
    elif not st.session_state["password_correct"]:
        # 密碼錯誤
        st.title("🔒 Malikay工作室 - 會員入口")
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        st.error("❌ 密碼錯誤，請重試")
        st.info("ℹ️ 會員請向三一協會索取密碼")
        return False
    
    else:
        # 密碼正確
        return True

# --- 4. 主程式介面 (App Body) ---
if check_password():
    # 只有通過驗證才會執行這裡
    st.title("🌿 Malikay工作室")
    st.subheader("生物邏輯共振助手 v2.0 (Cloud Ver.)")
    
    # 側邊欄：病患資料
    with st.sidebar:
        st.header("📋 病患檔案")
        patient_name = st.text_input("病患姓名")
        main_complaint = st.text_area("主要訴求 (症狀描述)")
        st.markdown("---")
        st.caption("由 Malikay 工作室開發")

    # Step 1: 脈診輸入
    st.markdown("### Step 1: 脈象輸入 (Input)")
    selected_pulse = st.selectbox(
        "請選擇最明顯的脈象特徵：",
        options=list(DIAGNOSIS_DB.keys())
    )

    # 按鈕觸發分析
    if st.button("⚡ 執行系統分析"):
        data = DIAGNOSIS_DB[selected_pulse]
        
        # Step 2: 系統診斷
        st.markdown("---")
        st.markdown("### Step 2: 系統邏輯 (Diagnostic Logic)")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**系統狀態：**\n\n{data['pattern']}")
        with col2:
            st.success(f"**調理策略：**\n\n{data['strategy']}")
            
        # Step 3: 穴位方案
        st.markdown("### Step 3: 穴位干預方案 (Action Protocol)")
        
        # 整理數據為表格
        points_data = data['acupoints']
        st.table(points_data)
        
        # 產生病歷報告文本
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_text = f"""
========================================
Malikay工作室 - 療程記錄
時間: {timestamp}
病患: {patient_name}
主訴: {main_complaint}
----------------------------------------
[診斷結果]
脈象: {selected_pulse}
判讀: {data['pattern']}
策略: {data['strategy']}
----------------------------------------
[執行穴位]
{points_data}
========================================
"""
        # 下載按鈕 (Web版不能直接存到硬碟，必須用下載的方式)
        st.download_button(
            label="💾 下載本次病歷記錄 (.txt)",
            data=report_text,
            file_name=f"Malikay_Log_{patient_name}_{datetime.date.today()}.txt",
            mime="text/plain"
        )

    # 簡單計時器工具
    st.markdown("---")
    with st.expander("⏱️ 按摩計時器工具"):
        timer_minutes = st.slider("設定時間 (分鐘)", 1, 10, 3)
        if st.button("開始計時"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_seconds = timer_minutes * 60
            
            for i in range(total_seconds):
                # 更新進度條
                progress = (i + 1) / total_seconds
                progress_bar.progress(progress)
                # 更新文字
                remaining = total_seconds - i - 1
                mins, secs = divmod(remaining, 60)
                status_text.metric("剩餘時間", f"{mins:02d}:{secs:02d}")
                time.sleep(1)
            
            st.success("✅ 療程結束！")
            st.balloons()
