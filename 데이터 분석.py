import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap

# 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 파일 경로
greenhouse_file = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 온실 온도 데이터.xlsx'
external_file = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB/5~8월 외부 온도 데이터.xlsx'
output_path = '/Users/kangtaeryeong/Documents/4. python files/학술회/DB'

# 엑셀 파일 불러오기
greenhouse_df = pd.read_excel(greenhouse_file)
external_df = pd.read_excel(external_file)

# 날짜 열을 datetime 형식으로 변환
greenhouse_df['날짜'] = pd.to_datetime(greenhouse_df['날짜'])
external_df['날짜'] = pd.to_datetime(external_df['날짜'])

# 시그모이드 함수 정의
def growth_probability(temp_avg, temp_max, temp_min, drop_factor=0.5):
    optimal_temp = 22.5
    lower_bound = 18
    upper_bound = 30
    
    # 기본 생장 확률 계산
    avg_component = 1 / (1 + np.exp(-0.3 * (temp_avg - optimal_temp)))
    max_component = 1 / (1 + np.exp(-0.3 * (temp_max - optimal_temp)))
    min_component = 1 / (1 + np.exp(-0.3 * (temp_min - optimal_temp)))
    
    overall_prob = (avg_component + max_component + min_component) / 3
    
    # 온도 조건에 따른 생장 확률 감소 적용
    if temp_max > upper_bound or temp_min < lower_bound:
        overall_prob -= drop_factor * (abs(temp_max - upper_bound) + abs(temp_min - lower_bound)) / 20  # 감소량 조절
    
    scaled_prob = 2 * (overall_prob - 0.5)  # -1 ~ 1로 변환
    return max(-1, min(1, scaled_prob))  # 범위를 -1 ~ 1로 제한

# 데이터프레임에 생장확률 컬럼 추가
greenhouse_df['생장확률'] = greenhouse_df.apply(lambda row: growth_probability(row[1], row[2], row[3]), axis=1)
external_df['생장확률'] = external_df.apply(lambda row: growth_probability(row[1], row[2], row[3]), axis=1)

# 사용자 정의 컬러맵 생성
custom_cmap_g = LinearSegmentedColormap.from_list('custom_cmap_g', ['yellow', 'purple', 'yellow'])  # 온실: 노란색 → 보라색 → 노란색
custom_cmap_e = LinearSegmentedColormap.from_list('custom_cmap_e', ['orange', 'green', 'orange'])  # 외부: 주황색 → 초록색 → 주황색

# 산점도 그리기
def plot_growth_probability_combined(greenhouse_df, external_df, output_filename):
    fig, axes = plt.subplots(1, 2, figsize=(28, 10), sharey=True)

    # 온실 환경 그래프
    scatter_g = axes[0].scatter(
        greenhouse_df['날짜'].dt.month,  # 월을 x축으로 사용
        greenhouse_df['날짜'].dt.day,
        c=greenhouse_df['생장확률'],
        cmap=custom_cmap_g,
        s=300 * (1 - np.abs(greenhouse_df['생장확률'])),  # 생장 확률이 0에 가까울수록 점 크기 증가
        norm=Normalize(vmin=-1, vmax=1),
        alpha=0.7
    )
    
    axes[0].set_title('온실 환경의 파프리카 생장 확률')
    axes[0].set_xlabel('월')
    axes[0].set_xticks([5, 6, 7, 8])
    axes[0].set_ylabel('일')
    axes[0].set_yticks(range(1, 32))
    axes[0].grid(True)

    # 외부 환경 그래프
    scatter_e = axes[1].scatter(
        external_df['날짜'].dt.month,  # 월을 x축으로 사용
        external_df['날짜'].dt.day,
        c=external_df['생장확률'],
        cmap=custom_cmap_e,
        s=300 * (1 - np.abs(external_df['생장확률'])),  # 생장 확률이 0에 가까울수록 점 크기 증가
        norm=Normalize(vmin=-1, vmax=1),
        alpha=0.7
    )

    axes[1].set_title('외부 환경의 파프리카 생장 확률')
    axes[1].set_xlabel('월')
    axes[1].set_xticks([5, 6, 7, 8])
    axes[1].set_ylabel('일')
    axes[1].set_yticks(range(1, 32))
    axes[1].grid(True)

    # 각각의 컬러바 추가
    cbar_g = fig.colorbar(scatter_g, ax=axes[0], shrink=0.95)
    cbar_g.set_label
    
    cbar_e = fig.colorbar(scatter_e, ax=axes[1], shrink=0.95)
    cbar_e.set_label

    plt.savefig(f"{output_path}/{output_filename}", dpi=300)
    plt.show()

# 두 그래프를 하나의 창에 표시
plot_growth_probability_combined(greenhouse_df, external_df, '생장확률 산점도.png')

print("png saved.")
