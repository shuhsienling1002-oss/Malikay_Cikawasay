import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

class BioLogicTherapyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("生物邏輯共振助手 (Bio-Logic Therapy Assistant) v1.0")
        self.root.geometry("1000x750")
        
        # --- 數據庫：脈象與穴位邏輯 (Logic Kernel) ---
        # 這是系統的「大腦」，定義了 輸入 -> 狀態 -> 輸出的映射關係
        self.diagnosis_db = {
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

        # --- GUI 介面佈局 ---
        self.create_widgets()

    def create_widgets(self):
        # 1. 頂部標題與病患資訊區
        header_frame = ttk.LabelFrame(self.root, text="Step 1: 病患檔案與脈診輸入", padding=15)
        header_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(header_frame, text="病患姓名:").grid(row=0, column=0, padx=5, sticky="w")
        self.name_entry = ttk.Entry(header_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(header_frame, text="主要訴求:").grid(row=0, column=2, padx=5, sticky="w")
        self.complaint_entry = ttk.Entry(header_frame, width=40)
        self.complaint_entry.grid(row=0, column=3, padx=5)

        # 脈象選擇
        ttk.Label(header_frame, text="脈象特徵 (Monitor):").grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.pulse_var = tk.StringVar()
        self.pulse_combo = ttk.Combobox(header_frame, textvariable=self.pulse_var, state="readonly", width=18)
        self.pulse_combo['values'] = list(self.diagnosis_db.keys())
        self.pulse_combo.current(0)
        self.pulse_combo.grid(row=1, column=1, padx=5, pady=10)

        # 分析按鈕
        self.analyze_btn = ttk.Button(header_frame, text="⚡ 執行系統分析 (Analyze)", command=self.run_diagnosis)
        self.analyze_btn.grid(row=1, column=3, padx=5, sticky="e")

        # 2. 診斷與邏輯顯示區
        self.logic_frame = ttk.LabelFrame(self.root, text="Step 2: 系統邏輯與臟腑辨證", padding=15)
        self.logic_frame.pack(fill="x", padx=10, pady=5)
        
        self.diagnosis_text = tk.Text(self.logic_frame, height=4, font=("Consolas", 10), bg="#f0f0f0")
        self.diagnosis_text.pack(fill="x")

        # 3. 穴位處方區
        self.action_frame = ttk.LabelFrame(self.root, text="Step 3: 穴位干預方案 (Action Protocol)", padding=15)
        self.action_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 這裡用 Treeview 來顯示穴位列表
        self.tree = ttk.Treeview(self.action_frame, columns=("point", "loc", "method"), show="headings", height=8)
        self.tree.heading("point", text="穴位名稱 (Node)")
        self.tree.heading("loc", text="物理位置 (Coordinates)")
        self.tree.heading("method", text="操作指令 (Operation)")
        
        self.tree.column("point", width=150)
        self.tree.column("loc", width=300)
        self.tree.column("method", width=300)
        self.tree.pack(fill="both", expand=True)

        # 4. 底部操作區 (計時與記錄)
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(fill="x")

        self.timer_label = ttk.Label(bottom_frame, text="00:00", font=("Helvetica", 24, "bold"))
        self.timer_label.pack(side="left", padx=20)
        
        self.start_timer_btn = ttk.Button(bottom_frame, text="▶ 開始按摩計時", command=self.start_timer)
        self.start_timer_btn.pack(side="left", padx=5)

        self.save_btn = ttk.Button(bottom_frame, text="💾 導出病歷記錄", command=self.save_record)
        self.save_btn.pack(side="right", padx=10)

        # 狀態變數
        self.timer_running = False
        self.time_left = 0

    def run_diagnosis(self):
        """核心運算：將脈象輸入映射到治療方案"""
        pulse = self.pulse_var.get()
        data = self.diagnosis_db.get(pulse)

        if not data:
            return

        # 1. 更新診斷顯示
        diag_content = f"【輸入脈象】：{pulse}\n"
        diag_content += f"【系統狀態】：{data['pattern']}\n"
        diag_content += f"【調理策略】：{data['strategy']}"
        
        self.diagnosis_text.delete(1.0, tk.END)
        self.diagnosis_text.insert(tk.END, diag_content)

        # 2. 更新穴位列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for point in data['acupoints']:
            self.tree.insert("", "end", values=(point['name'], point['loc'], point['method']))

    def start_timer(self):
        """簡單的倒數計時器"""
        if not self.timer_running:
            self.time_left = 180 # 預設 3 分鐘
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            self.timer_label.config(text="00:00")
            messagebox.showinfo("完成", "按摩療程結束！請進行後測脈象。")

    def save_record(self):
        """將本次療程記錄到TXT檔"""
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("錯誤", "請輸入病患姓名")
            return

        pulse = self.pulse_var.get()
        logic = self.diagnosis_text.get(1.0, tk.END).strip()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = f"""
========================================
時間: {timestamp}
病患: {name}
主訴: {self.complaint_entry.get()}
----------------------------------------
{logic}
----------------------------------------
[執行記錄] 穴位干預已完成
========================================
"""
        filename = f"therapy_log_{datetime.date.today()}.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(record)
        
        messagebox.showinfo("成功", f"記錄已保存至 {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    # 設定一些樣式
    style = ttk.Style()
    style.theme_use('clam')
    app = BioLogicTherapyApp(root)
    root.mainloop()