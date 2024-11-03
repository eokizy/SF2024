import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 불러오기 (온실 온도 데이터)
greenhouse_file_path = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 온실 온도 데이터.xlsx'
greenhouse_data = pd.read_excel(greenhouse_file_path)

# 데이터 불러오기 (외부 온도 데이터)
external_file_path = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 외부 온도 데이터.xlsx'
external_data = pd.read_excel(external_file_path)

# 날짜 데이터를 '월'과 '일'로 분리 (온실 데이터)
greenhouse_data['월'] = pd.to_datetime(greenhouse_data['날짜']).dt.month
greenhouse_data['일'] = pd.to_datetime(greenhouse_data['날짜']).dt.day

# 날짜 데이터를 '월'과 '일'로 분리 (외부 데이터)
external_data['월'] = pd.to_datetime(external_data['날짜']).dt.month
external_data['일'] = pd.to_datetime(external_data['날짜']).dt.day

# 생장 확률 계산을 위한 시그모이드 함수
def sigmoid(x, k=1, x0=22.5):
    return 1 / (1 + np.exp(-k * (x - x0)))

# 생장 확률 계산 함수
def calculate_growth_probability(avg_temp, min_temp, max_temp):
    if min_temp < 18:
        drop_factor = (18 - min_temp) * 0.1
        return max(0, sigmoid(avg_temp) - drop_factor)
    elif max_temp > 30:
        drop_factor = (max_temp - 30) * 0.05
        return max(0, sigmoid(avg_temp) - drop_factor)
    else:
        return sigmoid(avg_temp)

# 평균 기온을 기준으로 생장 확률 계산 (온실 데이터)
greenhouse_data['생장확률'] = greenhouse_data.apply(
    lambda row: calculate_growth_probability(row['온실 평균기온'], row['온실 최저기온'], row['온실 최고기온']),
    axis=1
)

# 평균 기온을 기준으로 생장 확률 계산 (외부 데이터)
external_data['생장확률'] = external_data.apply(
    lambda row: calculate_growth_probability(row['외부 평균기온'], row['외부 최저기온'], row['외부 최고기온']),
    axis=1
)

# 그래프 크기 설정
fig, axs = plt.subplots(1, 2, figsize=(14,6))
plt.subplots_adjust(hspace=0.4)  # 그래프 간격 조정

# 온실 데이터 산점도 그리기
scatter1 = axs[0].scatter(
    greenhouse_data['월'],
    greenhouse_data['일'],
    c=greenhouse_data['생장확률'],
    s=greenhouse_data['생장확률'] * 150 + 20,
    cmap='viridis',
    alpha=0.75
)

# 컬러바 추가
cbar1 = plt.colorbar(scatter1, ax=axs[0])
cbar1.set_label('생장 확률 (%)')

axs[0].set_xlabel('월')
axs[0].set_ylabel('일')
axs[0].set_title('2024년 5월~8월 온실 생장 확률')
axs[0].set_xticks([5, 6, 7, 8])
axs[0].set_yticks(range(1, 32))
axs[0].grid(True, linestyle='--', alpha=0.3)

# 외부 데이터 산점도 그리기
scatter2 = axs[1].scatter(
    external_data['월'],
    external_data['일'],
    c=external_data['생장확률'],
    s=external_data['생장확률'] * 150 + 20,
    cmap='plasma',
    alpha=0.75
)

# 컬러바 추가
cbar2 = plt.colorbar(scatter2, ax=axs[1])
cbar2.set_label('생장 확률 (%)')

axs[1].set_xlabel('월')
axs[1].set_ylabel('일')
axs[1].set_title('2024년 5월~8월 외부 생장 확률')
axs[1].set_xticks([5, 6, 7, 8])
axs[1].set_yticks(range(1, 32))
axs[1].grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()

# 시그모이드 함수 그래프 저장하기
temp_range = np.linspace(10, 35, 100)
growth_probs = sigmoid(temp_range) * 100  # 생장 확률을 퍼센트로 변환

# 시그모이드 함수 그래프 그리기
plt.figure(figsize=(12, 4))
plt.plot(temp_range, growth_probs, color='red', label='생장 확률', linewidth=2)
plt.xlabel('온도 (°C)')
plt.ylabel('생장 확률 (%)')
plt.title('온도별 생장 확률 시그모이드')
plt.grid(True, linestyle='--', alpha=0.3)
plt.axhline(0, color='black', lw=1)
plt.axvline(18, color='grey', linestyle='--', lw=0.8)
plt.axvline(30, color='grey', linestyle='--', lw=0.8)
plt.legend()

# 이미지 파일로 저장
sigmoid_file_path = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/온도별 생장 확률 시그모이드.png'
try:
    plt.savefig(sigmoid_file_path, bbox_inches='tight')
    print(f"Sigmoid graph saved as '{sigmoid_file_path}'.")
except Exception as e:
    print(f"Error saving sigmoid graph: {e}")

plt.close()  # 현재 플롯 닫기



# '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 온실 온도 데이터.xlsx'