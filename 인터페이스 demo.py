#연암대 스마트팜 제작 프로젝트 복합환경관리 인터페이스입니다.
#현재 랜덤 값으로 환경 설정되어있고, 추후 센서 Serial 데이터로 교체할 예정입니다.
#데이터 로그 데이터는 pandas로 엑셀파일 저장할 수 있게 업데이트 필요합니다. 현재 log_entries 리스트에 1000개 까지 저장됩니다.

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading
from datetime import datetime

# 초기값 설정
manual_temp = 25.0  # 수동 설정 온도
current_humidity = 50.0
current_weight = 2000  # 초기 무게 (2000g)
led_status = "OFF"
pump_status = "OFF"
log_entries = []  # 전체 로그 저장 리스트

# 실시간 데이터를 업데이트하는 함수
def update_graph():
    global manual_temp, current_humidity, adjusted_temp
    while True:
        # 설정된 온도를 기준으로 편차를 적용한 온도 생성
        adjusted_temp = manual_temp + random.uniform(-0.2, 0.2)
        temp_data.append(adjusted_temp)
        current_humidity = current_humidity + random.uniform(-1, 1)
        current_humidity = max(0, min(100, current_humidity))  # 습도 범위 제한
        humidity_data.append(current_humidity)

        if len(temp_data) > 50:  # 그래프에 표시할 데이터 길이 제한
            temp_data.pop(0)
            humidity_data.pop(0)

        # 그래프 업데이트
        ax1.clear()
        ax2.clear()
        ax3.clear()

        # 온도+습도 그래프
        ax1.plot(temp_data, label="Temperature (°C)", color="red")
        ax1.plot(humidity_data, label="Humidity (%)", color="blue")
        ax1.legend(loc="upper left")
        ax1.set_title("Temperature and Humidity Combined")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Value")

        # 개별 그래프
        ax2.plot(temp_data, color="red")
        ax2.set_title("Temperature (°C)")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Temperature")

        ax3.plot(humidity_data, color="blue")
        ax3.set_title("Humidity (%)")
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Humidity")

        canvas.draw()
        time.sleep(1)  # 1초 간격으로 업데이트

# LED, PUMP 상태 변경 함수
def toggle_led():
    global led_status
    led_status = "ON" if led_status == "OFF" else "OFF"
    led_button.config(text=f"LED: {led_status}")

def toggle_pump():
    global pump_status
    pump_status = "ON" if pump_status == "OFF" else "OFF"
    pump_button.config(text=f"PUMP: {pump_status}")

# 데이터 로그 업데이트 함수
def update_log():
    global adjusted_temp, current_humidity, current_weight, led_status, pump_status
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")  # 현재 시간 (시:분:초)
        co2 = random.randint(400, 600)
        lux = random.randint(300, 700) if led_status == "ON" else random.randint(10, 50)
        current_weight += random.uniform(-5, 5)
        current_weight = max(1990, min(2010, current_weight))  # 무게 범위 제한
        log_entry = (f"[{current_time}] Temp: {adjusted_temp:.1f}°C, "
                     f"Humidity: {current_humidity:.2f}%, "
                     f"CO2: {co2}ppm, "
                     f"Lux: {lux}, "
                     f"Weight: {current_weight:.1f}g, "
                     f"LED: {led_status}, "
                     f"PUMP: {pump_status}")
        log_entries.append(log_entry)
        if len(log_entries) > 1000:  # 로그 기록 제한
            log_entries.pop(0)
        log_text.insert("end", log_entry + "\n")
        log_text.see("end")
        time.sleep(2)

# 로그 검색 함수
def search_logs():
    query = search_entry.get().strip()
    search_results.delete("1.0", "end")
    if not query:
        search_results.insert("end", "Please enter a search query.\n")
        return

    results = [log for log in log_entries if query in log]
    if results:
        search_results.insert("end", "\n".join(results) + "\n")
    else:
        search_results.insert("end", "No data found for the given query.\n")

# Tkinter 창 생성
root = tk.Tk()
root.title("Smart Farm Interface")
root.geometry("1200x800")

# Notebook 생성 (탭 인터페이스)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# 실시간 그래프 탭
graph_tab = ttk.Frame(notebook)
notebook.add(graph_tab, text="Real-time Graph")

# Matplotlib 그래프 생성
temp_data = []
humidity_data = []

fig = Figure(figsize=(10, 6), dpi=100)
ax1 = fig.add_subplot(211)  # 온도+습도
ax2 = fig.add_subplot(223)  # 온도 개별
ax3 = fig.add_subplot(224)  # 습도 개별
canvas = FigureCanvasTkAgg(fig, master=graph_tab)
canvas.get_tk_widget().pack(fill="both", expand=True)

# 장치 제어 탭
control_tab = ttk.Frame(notebook)
notebook.add(control_tab, text="Device Control")

control_label = tk.Label(control_tab, text="Device Control Panel", font=("Arial", 16))
control_label.pack(pady=10)

# 수동 온도 조절 기능
def increase_temp():
    global manual_temp
    manual_temp += 0.1
    temp_spinbox_var.set(f"{manual_temp:.1f}")

def decrease_temp():
    global manual_temp
    manual_temp -= 0.1
    temp_spinbox_var.set(f"{manual_temp:.1f}")

temp_spinbox_var = tk.StringVar(value=f"{manual_temp:.1f}")
temp_control_frame = ttk.LabelFrame(control_tab, text="Manual Temperature Control")
temp_control_frame.pack(pady=10)

temp_label = tk.Label(temp_control_frame, text="Set Temperature (°C):")
temp_label.pack(side="left", padx=5)

temp_spinbox = tk.Entry(temp_control_frame, textvariable=temp_spinbox_var, width=6)
temp_spinbox.pack(side="left", padx=5)

up_button = tk.Button(temp_control_frame, text="▲", command=increase_temp)
up_button.pack(side="left", padx=5)

down_button = tk.Button(temp_control_frame, text="▼", command=decrease_temp)
down_button.pack(side="left", padx=5)

# 장치 상태 제어 버튼 추가
device_control_frame = ttk.LabelFrame(control_tab, text="Device Control")
device_control_frame.pack(pady=10)

led_button = tk.Button(device_control_frame, text=f"LED: {led_status}", command=toggle_led)
led_button.pack(padx=10, pady=5)

pump_button = tk.Button(device_control_frame, text=f"PUMP: {pump_status}", command=toggle_pump)
pump_button.pack(padx=10, pady=5)

# 데이터 로그 탭
log_tab = ttk.Frame(notebook)
notebook.add(log_tab, text="Data Log")

log_label = tk.Label(log_tab, text="Data Log", font=("Arial", 16))
log_label.pack(pady=10)

log_frame = ttk.Frame(log_tab)
log_frame.pack(fill="both", expand=True, pady=10)

log_text = tk.Text(log_frame, wrap="word", height=20, width=60)
log_text.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side="left", fill="y")
log_text.config(yscrollcommand=scrollbar.set)

# 로그 검색 창
search_frame = ttk.LabelFrame(log_tab, text="Search Logs")
search_frame.pack(fill="both", expand=True, pady=10)

search_entry = tk.Entry(search_frame, width=20)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_logs)
search_button.pack(side="left", padx=5)

search_results = tk.Text(search_frame, wrap="word", height=10, width=80)
search_results.pack(side="left", fill="both", expand=True)

# 백그라운드 스레드 실행
threading.Thread(target=update_graph, daemon=True).start()
threading.Thread(target=update_log, daemon=True).start()

# Tkinter 이벤트 루프 실행
root.mainloop()
