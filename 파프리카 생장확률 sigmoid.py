import numpy as np
import matplotlib.pyplot as plt
# 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 온도 범위 설정
temperature_range = np.linspace(0, 40, 400)  # 0도부터 40도까지

# 변형된 시그모이드 함수 정의 (-1부터 1까지)
def scaled_sigmoid(x, x0=22.5, k=0.4):
    return 2 / (1 + np.exp(-k * (x - x0))) - 1

# 파프리카의 생장확률 계산
growth_probability = scaled_sigmoid(temperature_range)

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(temperature_range, growth_probability, color='green')
plt.axvline(20, color='blue', linestyle='--', label='생육 적정 기준 온도(20°C ~ 25°C)')
plt.axvline(25, color='blue', linestyle='--')
plt.axvline(18, color='red', linestyle='--', label='생육 장해 기준 온도 (18°C, 30°C)')
plt.axvline(30, color='red', linestyle='--')

plt.title('파프리카 생장확률 sigmoid')
plt.xlabel('온도 (°C)')
plt.ylabel('생장확률')
plt.legend()
plt.grid(True)
plt.show()
