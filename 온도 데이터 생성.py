import numpy as np
import pandas as pd

# 설정 기간: 2024년 5월 1일부터 8월 31일까지
date_range = pd.date_range(start="2024-05-01", end="2024-08-31")

# 임의 데이터 생성 기준
np.random.seed(42)  # 재현 가능성

# 외부 평균 온도 (20°C ~ 30°C)
external_avg_temp = np.random.uniform(20, 30, len(date_range))
# 외부 최고 온도 (평균 + 2~7°C)
external_max_temp = external_avg_temp + np.random.uniform(2, 7, len(date_range))
# 외부 최저 온도 (평균 - 3~8°C)
external_min_temp = external_avg_temp - np.random.uniform(3, 8, len(date_range))

# 온실 평균 온도 (22 + 1~3°C)
greenhouse_avg_temp = 22 + np.random.uniform(1, 3, len(date_range))
# 온실 최고 온도 (온실 평균 + 1~2°C)
greenhouse_max_temp = greenhouse_avg_temp + np.random.uniform(1, 2, len(date_range))
# 온실 최저 온도 (온실 평균 - 1~2°C)
greenhouse_min_temp = greenhouse_avg_temp - np.random.uniform(1, 2, len(date_range))

# 데이터프레임 생성
temperature_data = pd.DataFrame({
    "Date": date_range,
    "External Avg Temp (°C)": external_avg_temp,
    "External Max Temp (°C)": external_max_temp,
    "External Min Temp (°C)": external_min_temp,
    "Greenhouse Avg Temp (°C)": greenhouse_avg_temp,
    "Greenhouse Max Temp (°C)": greenhouse_max_temp,
    "Greenhouse Min Temp (°C)": greenhouse_min_temp
})

# 외부 온도 데이터 저장
external_temps = temperature_data[["Date", "External Avg Temp (°C)", "External Max Temp (°C)", "External Min Temp (°C)"]]
external_temps.to_excel("external_temperatures.xlsx", index=False)

# 내부 온도 데이터 저장
greenhouse_temps = temperature_data[["Date", "Greenhouse Avg Temp (°C)", "Greenhouse Max Temp (°C)", "Greenhouse Min Temp (°C)"]]
greenhouse_temps.to_excel("greenhouse_temperatures.xlsx", index=False)

print("파일이 성공적으로 저장되었습니다.")
