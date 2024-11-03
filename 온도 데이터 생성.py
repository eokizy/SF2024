import numpy as np
import pandas as pd

# 설정 기간: 2024년 5월 1일부터 8월 31일까지
date_range = pd.date_range(start="2024-05-01", end="2024-08-31")
num_days = len(date_range)

# 임의 데이터 생성 기준
np.random.seed(42)  # 재현 가능성

# 기본적인 상승 경향성을 위한 선형 증가값 (5월 20°C, 8월 30°C)
trend = np.linspace(20, 30, num_days)

# 외부 평균 온도 (기본 경향성 + 랜덤 변동성)
external_avg_temp = trend + np.random.uniform(-2, 2, num_days)
# 외부 최고 온도 (평균 + 2~7°C)
external_max_temp = external_avg_temp + np.random.uniform(2, 7, num_days)
# 외부 최저 온도 (평균 - 3~8°C)
external_min_temp = external_avg_temp - np.random.uniform(3, 8, num_days)

# 온실 평균 온도 (22.5 + 변동성)
greenhouse_avg_temp = 22.5 + np.random.uniform(1, 3, num_days)
# 온실 최고 온도 (온실 평균 + 1~2°C)
greenhouse_max_temp = greenhouse_avg_temp + np.random.uniform(1, 2, num_days)
# 온실 최저 온도 (온실 평균 - 1~2°C)
greenhouse_min_temp = greenhouse_avg_temp - np.random.uniform(1, 2, num_days)

# 데이터프레임 생성
temperature_data = pd.DataFrame({
    "날짜": date_range.strftime("%Y-%m-%d"),
    "외부 평균기온": external_avg_temp,
    "외부 최고기온": external_max_temp,
    "외부 최저기온": external_min_temp,
    "온실 평균기온": greenhouse_avg_temp,
    "온실 최고기온": greenhouse_max_temp,
    "온실 최저기온": greenhouse_min_temp
})

# 소숫점 한 자리로 반올림
temperature_data = temperature_data.round(1)

# 저장 경로 설정 (파일명 포함)
save_path_external = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 외부 온도 데이터.xlsx'
save_path_greenhouse = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 온실 온도 데이터.xlsx'

# 외부 온도 데이터 저장
external_temps = temperature_data[["날짜", "외부 평균기온", "외부 최고기온", "외부 최저기온"]]
external_temps.to_excel(save_path_external, index=False)

# 내부 온도 데이터 저장
greenhouse_temps = temperature_data[["날짜", "온실 평균기온", "온실 최고기온", "온실 최저기온"]]
greenhouse_temps.to_excel(save_path_greenhouse, index=False)

print("파일이 성공적으로 저장되었습니다.")
