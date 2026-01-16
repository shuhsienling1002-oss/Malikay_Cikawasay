import streamlit as st
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="Malikay工作室",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. [新增] 字型自動修復模組 ---
def get_chinese_font():
    """
    解決 Linux (Streamlit Cloud) 無法顯示中文的問題。
    自動下載 Google Noto Sans TC 字型檔。
    """
    font_path = "NotoSansTC-Regular.otf"
    
    # 如果字型檔不存在，就從網路下載
    if not os.path.exists(font_path):
        # 使用 Google Fonts 的開源字型 (約 16MB，下載一次即可)
        url = "https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf"
        try:
            with st.spinner("正在下載中文字型檔 (首次執行需約 10 秒)..."):
                urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            st.error(f"字型下載失敗: {e}")
            return None

    # 載入字型屬性
    return fm.FontProperties(fname=font_path)

# --- 3. 視覺化繪圖引擎 (已修復亂碼) ---
def draw_pulse_wave(pulse_type):
    x = np.linspace(0, 4 * np.pi, 400)
    fig, ax = plt.subplots(figsize=(6, 2))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_facecolor('#f0f2f6')
    fig.patch.set_facecolor('#f0f2f6')

    # 取得中文字型物件
    chinese_font = get_chinese_font()

    if "弦脈" in pulse_type:
        y = np.sin(x) + 0.3 * np.sin(3*x) 
        title = "🌊 弦脈波形：張力高，如按琴弦"
        color = '#FF5252'
    elif "滑脈" in pulse_type:
        y = np.sin(x)
        title = "🌊 滑脈波形：圓滑流利，如珠滾盤"
        color = '#448AFF'
    elif "沉細" in pulse_type:
        y = 0.3 * np.sin(x)
        title = "🌊 沉細波形：波幅低扁，若有若無"
        color = '#9E9E9E'
    elif "數脈" in pulse_type:
        y = np.sin(2 * x)
        title = "🌊 數脈波形：頻率急促，波峰密集"
        color = '#FF9800'
    elif "虛脈" in pulse_type:
        noise = np.random.normal(0, 0.05, x.shape)
        y = 0.4 * np.sin(x) + noise
        title = "🌊 虛脈波形：浮散無力，波形不穩"
        color = '#90A4AE'
    else:
        y = np.sin(x)
        title = "正常波形"
        color = 'black'

    ax.plot(x, y, color=color, linewidth=2.5)
    
    # 關鍵修正：這裡不使用 fontname="Microsoft JhengHei"，而是使用 fontproperties
    if chinese_font:
        ax.set_title(title, fontproperties=chinese_font, fontsize=14)
    else:
        ax.set_title(title, fontsize=12) # 如果下載失敗，至少顯示亂碼但不會報錯
        
    return fig

# --- 4. 系統邏輯核心 (完全保留) ---
DIAGNOSIS_DB = {
    "弦脈 (Wiry) —— 手感：像按在琴弦上，緊繃有力": {
        "pattern": "肝氣鬱結 / 自律神經張力過高",
        "strategy": "疏肝理氣，解痙攣",
        "acupoints": [
            {"name": "太衝 (LR3)", "loc": "足背大拇趾與二趾縫後凹陷", "method": "瀉法 (逆時針重揉) 3分鐘"},
            {"name": "內關 (PC6)", "loc": "手腕橫紋上三指", "method": "平補平瀉 2分鐘"}
        ]
    },
    "滑脈 (Slippery) —— 手感：像珠子在盤子滾動，圓滑流利": {
        "pattern": "痰濕 / 食積 / 消化系統負載過重",
        "strategy": "健脾祛濕，化痰",
        "acupoints": [
            {"name": "豐隆 (ST40)", "loc": "小腿外側中點", "method": "重按 (強刺激) 3分鐘"},
            {"name": "中脘 (CV12)", "loc": "肚臍上四寸", "method": "溫灸或順時針揉 5分鐘"}
        ]
    },
    "沉細 (Deep & Thready) —— 手感：輕按摸不到，重按才有，細細一條": {
        "pattern": "腎氣不足 / 氣血兩虛 / 系統能量低",
        "strategy": "補益氣血，提升基礎代謝",
        "acupoints": [
            {"name": "足三里 (ST36)", "loc": "膝眼下四指", "method": "補法 (順時針輕揉/灸) 5分鐘"},
            {"name": "氣海 (CV6)", "loc": "肚臍下1.5寸", "method": "靜按或熱敷"}
        ]
    },
    "數脈 (Rapid) —— 手感：跳動頻率非常快 (急促)": {
        "pattern": "熱證 / 發炎反應 / 代謝亢進",
        "strategy": "清熱涼血，降低系統熵值",
        "acupoints": [
            {"name": "曲池 (LI11)", "loc": "手肘橫紋外側端", "method": "瀉法 (強刺激) 2分鐘"},
            {"name": "合谷 (LI4)", "loc": "虎口處", "method": "間歇點按"}
        ]
    },
    "虛脈 (Empty) —— 手感：按下去軟綿綿，沒什麼力氣": {
        "pattern": "氣血虧虛 / 循環動力不足",
        "strategy": "大補元氣，激活幫浦",
        "acupoints": [
            {"name": "百會 (GV20)", "loc": "頭頂正中", "method": "輕按 1分鐘"},
            {"name": "關元 (CV4)", "loc": "肚臍下三寸", "method": "長時間溫灸"}
        ]
    }
}

# --- 5. 登入系統邏輯 (完全保留) ---
def check_password():
    """驗證密碼函數"""
    def password_entered():
        if st.session_state["password"] == "1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Malikay 會員入口")
        st.markdown("### 請輸入訪問密碼")
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        st.info("ℹ️ 會員請向三一協會索取密碼")
        return False
    
    elif not st.session_state["password_correct"]:
        st.title("🔒 Malikay 會員入口")
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        st.error("❌ 密碼錯誤")
        st.info("ℹ️ 會員請向三一協會索取密碼")
        return False
    
    else:
        return True

# --- 6. 主程式介面 ---
if check_password():
    st.title("🌿 Malikay工作室")
    st.caption("生物邏輯共振助手 v2.5 (Font Fixed)")
    
    # 輸入區
    with st.expander("📝 第一步：建立病患檔案 (必填)", expanded=True):
        patient_name = st.text_input("病患姓名")
        main_complaint = st.text_area("主要症狀/訴求 (請詳細描述)", height=80)

    st.divider()

    # Step 1: 脈診輸入
    st.markdown("### 🔍 第二步：脈象輸入")
    
    pulse_options = ["請滑動選擇..."] + list(DIAGNOSIS_DB.keys())
    selected_pulse = st.selectbox(
        "請根據您的手感選擇最接近的描述：",
        options=pulse_options
    )

    # 按鈕邏輯區
    if st.button("⚡ 執行系統分析", type="primary", use_container_width=True):
        
        # --- 邏輯檢查閘門 ---
        if not patient_name or not main_complaint:
            st.warning("⚠️ 無法執行：請先回到第一步，填寫【病患姓名】與【主要症狀】。")
            st.stop()
            
        if selected_pulse == "請滑動選擇...":
            st.warning("⚠️ 無法執行：請在第二步選擇一個具體的【脈象】。")
            st.stop()
        # ----------------------------

        data = DIAGNOSIS_DB[selected_pulse]
        
        # Step 2: 系統診斷
        st.markdown("---")
        st.subheader("📊 診斷結果")
        
        # 顯示脈波圖
        st.markdown("**【脈波視覺化 (Pulse Visualization)】**")
        fig = draw_pulse_wave(selected_pulse)
        st.pyplot(fig) 
        
        st.info(f"**【系統狀態】**\n\n{data['pattern']}")
        st.success(f"**【調理策略】**\n\n{data['strategy']}")
            
        # Step 3: 穴位方案
        st.markdown("### 💆 第三步：穴位干預")
        
        for point in data['acupoints']:
            with st.container(border=True):
                col_icon, col_text = st.columns([1, 5])
                with col_icon:
                    st.markdown("# 📍") 
                with col_text:
                    st.markdown(f"**{point['name']}**")
                    st.caption(f"位置: {point['loc']}")
                    st.markdown(f"👉 **操作**: {point['method']}")

        # 產生病歷文本
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
{data['acupoints']}
========================================
"""
        st.markdown("---")
        st.download_button(
            label="💾 下載病歷記錄 (.txt)",
            data=report_text,
            file_name=f"Malikay_{patient_name}_{datetime.date.today()}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # 計時器工具
    st.markdown("---")
    with st.expander("⏱️ 按摩計時器工具"):
        timer_minutes = st.slider("設定時間 (分鐘)", 1, 10, 3)
        if st.button("▶ 開始計時", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_seconds = timer_minutes * 60
            
            for i in range(total_seconds):
                progress = (i + 1) / total_seconds
                progress_bar.progress(progress)
                remaining = total_seconds - i - 1
                mins, secs = divmod(remaining, 60)
                status_text.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                time.sleep(1)
            
            st.success("✅ 療程結束！")
            st.balloons()
