"""파이썬 시리얼 통신 master 코드입니다!"""
# 파이썬 라이브러리 => 특정 기능을 위해 만든 패키지
# 라이브러리를 가져오는 import를 통해 라이브러리를 사용 가능
# 기본 라이브러리를 제외한 라이브러리는 다운로드가 필요함 ex. pandas, serial(pyserial) ...
import serial # 시리얼 통신을 위한 라이브러리, 파이썬의 시리얼 데이터(센서 값 등)을 파이썬에서 사용 가능함
import matplotlib.pyplot as plt # 그래프를 그리기 위한 라이브러리
import matplotlib.animation as animation # 그래프를 실시간으로 업데이트
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
import pandas as pd #엑셀 파일로 데이터 저장을 위한 라이브러리
import os # 컴푸터 시스템 데이터에 접속

# 시리얼 포트 설정
# 아두이노가 받는 센서값이나 지정하여 나오는 값들(시리얼 데이터)을 Serial.print를 통해 시리얼 모니터로 열람할 수 있는데 그 데이터를 포트(연결선usb)를 통해 컴퓨터로 가져옴
ser = serial.Serial('/dev/cu.usbmodem1101', 9600) # /dev/cu.usbmodem1101 부분은 자기가 꼽은 아두이노 포트의 위치로 변경해야 함, 9600은 데이터 전송 속도(이 또한 아두이노의 전송속도에 맞춰야함)

# 데이터 저장 리스트 초기화
times = []
temperatures = []
humidities = []

last_saved_time = None

save_dir = '/Users/kangtaeryeong/Documents/4. python files/DB' # 파일을 저장할 위치를 지정

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

#그래프를 칸과 배치 설정
fig = plt.figure(figsize=(12, 10))

ax1 = plt.subplot2grid((4, 2), (0, 0), rowspan=2, colspan=2)
ax4 = ax1.twinx()

ax2 = plt.subplot2grid((4, 2), (2, 0), rowspan=1, colspan=1)
ax3 = plt.subplot2grid((4, 2), (2, 1), rowspan=1, colspan=1)

ax5 = plt.subplot2grid((4, 2), (3, 0), rowspan=1, colspan=1)
ax6 = plt.subplot2grid((4, 2), (3, 1), rowspan=1, colspan=1)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)
ax5.grid(True)
ax6.grid(True)

# 엑셀 저장 함수
def save_to_excel(times, temperatures, humidities, datetime_obj):
    hours = [t.hour for t in times]
    minutes = [t.minute for t in times]
    seconds = [t.second for t in times]
    
    df = pd.DataFrame({ # pandas 라이브러리 사용, 엑셀 데이터 저장에 주로 쓰이는 라이브러리이다
        'Hour': hours,
        'Minute': minutes,
        'Second': seconds,
        'Temperature (C)': temperatures,
        'Humidity (%)': humidities
    })

    filename = datetime_obj.strftime("%Y-%m-%d") + ".xlsx" # 파일 이름 지정 %Y(년) %m(월) %d(일) 2024-7-5 이런식으로 저장됨
    file_path = os.path.join(save_dir, filename)
    df.to_excel(file_path, index=False)

# 그래프 추가 설정 (색, 폰트사이즈 등 가시성을 높이기 위한 꾸미기용 코드)
def create_gauge(ax, value, max_value, label, color):
    data = [value, max_value - value]
    ax.clear()
    wedges, texts = ax.pie(data, startangle=90, colors=[color, "lightgray"], counterclock=False)
    ax.add_artist(plt.Circle((0, 0), 0.7, color='white'))
    ax.text(0, 0, f"{value:.2f}\n{label}", ha='center', va='center', fontsize=14)
    ax.set_aspect('equal')

# 실시간 그래프 동작을 위함 함수 설정
def animate(i, times, temperatures, humidities):
    global last_saved_time

    try:
        # 아두이노에서 시리얼 통신을 통해 데이터를 받아옴 8개 (년도,월,일,시,분,초,온도,습도)
        line = ser.readline().decode('utf-8').strip()
        # ,로 데이터를 나눔(스플릿) 년도[0] 월[1] 일[2] 시[3] 분[4] 초[5] 온도[6] 습도[7]
        data = line.split(',')

        if len(data) == 11:
            # 나눈 데이터를 각 변수에 저장
            year = int(data[0]) # 년도는 0번 (파이썬에서는 0번 부터 시작)
            month = int(data[1])
            day = int(data[2])
            hour = int(data[3])
            minute = int(data[4])
            second = int(data[5])
            temperature_in = float(data[6])
            humidity_in = float(data[7])
            temperature_ex = float(data[8])
            humidity_ex = float(data[9])
            cds = float(data[10])
            # 데이터 시리얼 데이터 추가시 순차적으로 번호를 매겨주시면 됩니다.

            # 년 월 일 시 분 초를 변수로 따로 묶어둠
            current_time = datetime(year, month, day, hour, minute, second)

            times.append(current_time)
            temperatures.append(temperature_in)
            humidities.append(humidity_in)

            # 현재 시간을 기준으로 하루가 지나면 데이터 저장
            if last_saved_time is None or current_time > last_saved_time + timedelta(days=1):
                if last_saved_time is not None:
                    save_to_excel(times, temperatures, humidities, last_saved_time)
                    times.clear()
                    temperatures.clear()
                    humidities.clear()

                last_saved_time = current_time

            fig.suptitle(current_time.strftime("%Y-%m-%d-%H")) #그래프 제목 설정

            ax1.clear()
            ax4.clear()

            ax1.plot(times, temperatures, label='Temperature (C)', color='red')
            ax4.plot(times, humidities, label='Humidity (%)', color='blue')
            ax1.set_ylabel('Temperature (C)')
            ax4.set_ylabel('Humidity (%)')
            ax4.yaxis.set_label_position('right')

            ax1.set_ylim(0, 50) # 실시간 꺾은선 그래프 범위 설정 (온도)
            ax4.set_ylim(0, 100) # (습도)

            ax1.set_xlabel('Time')

            ax1.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

            ax1.legend(loc='upper left')
            ax4.legend(loc='upper right')

            # 온습도 게이지
            create_gauge(ax5, temperature, 50, 'C', 'red')
            create_gauge(ax6, humidity, 100, '%', 'blue')

            # 개별 온도 그래프 그리기
            ax2.clear()
            ax2.plot(times, temperatures, label='Temperature (C)', color='green')
            ax2.set_ylabel('Temperature (C)')
            ax2.set_xlabel('Time')
            ax2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            ax2.legend(loc='upper left')

            # 개별 습도 그래프 그리기
            ax3.clear()
            ax3.plot(times, humidities, label='Humidity (%)', color='purple')
            ax3.set_ylabel('Humidity (%)')
            ax3.set_xlabel('Time')
            ax3.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            ax3.legend(loc='upper left')

            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            ax4.grid(True)
            ax5.grid(True)
            ax6.grid(True)

    except Exception as e:
        print(f"Error: {e}")
# (위)여기까지가 실시간 그래프 함수

# (밑)실시간 그래프 함수 호출
ani = animation.FuncAnimation(fig, animate, fargs=(times, temperatures, humidities), interval=1000)

plt.tight_layout()
plt.show() #그래프 보이기

ser.close()
# 그래프를 어떻게 그리냐 보다는 데이터를 어떻게 가져와서 이용하는가를 중점으로 보시면 됩니다!
# 시리얼 통신의 구조가 핵심입니다!
# 앞으로는 센서가 더 추가 되고 역으로 파이썬에서 아두이노로 데이터를 전송해야 하기 때문에 데이터의 양이 더 방대해지고 코드가 더 길어질 겁니다.
# pandas 라이브러리를 이용해 하루마다 저장한 데이터가 모이면 그게 데이터베이스(DB)가 됩니다.
# 최종적으로는 그 데이터들을 서버에 전달해 외부 기기들로 서버에 접속하여 데이터를 열람하는 것이 데이터 통신의 목표입니다!
