import csv
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from flask import Blueprint, send_file
from io import BytesIO
import os
import seaborn as sns
import locale


bp = Blueprint('graph', __name__, url_prefix='/graph')

# 한글 폰트 설정
plt.rcParams['font.family'] ='AppleGothic' # 나중에 Malgun Gothic 혹은 NanumGothic으로 설정
plt.rcParams['axes.unicode_minus'] =False


filename = os.path.join(os.path.dirname(__file__), 'case3.csv')
criminal_list = []

data = pd.read_csv(filename)

@bp.route("/bar")
def crime_frequency():
    # 두 번째 열의 데이터 가져오기 (0부터 시작하므로 1을 사용)
    target_column = data.iloc[:, 1]

    # "기사제목"이라는 단어를 제외한 데이터 추출
    target_column_without_title = target_column[target_column != '기사제목']

    # 중복된 단어 수 세기
    word_counts = target_column_without_title.value_counts()

    # 결과를 그래프로 표시
    plt.switch_backend('Agg')  # Agg 백엔드로 전환
    plt.clf()  # 현재 그림 초기화
    plt.figure(figsize=(10, 6))

    # Seaborn의 막대 그래프(barplot) 사용
    sns.barplot(x=word_counts.index, y=word_counts.values, palette="viridis")

    # 그래프에 라벨 추가
    plt.xlabel('범죄 종류')
    plt.ylabel('빈도수')
    plt.title('범죄가 발생하는 수')

    # x축 라벨 회전
    plt.xticks(rotation=45, ha='right')

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)

    return send_file(img, mimetype='image/png')


@bp.route('/pie')
def pie():
    # 원형 그래프
    # CSV 파일 읽기
    df = pd.read_csv(filename)

    # 2번째 열 선택
    keyword_column = df.iloc[:, 1]

    # 키워드 개수에 따라 파이 차트 그리기
    plt.switch_backend('Agg')  # Agg 백엔드로 전환
    plt.clf()  # 현재 그림 초기화
    plt.figure(figsize=(10, 6))  # 그래프 크기 조절

    # 각 키워드에 대한 파이 차트 그리기
    keyword_counts = keyword_column.value_counts()

    # 5% 미만인 부분은 퍼센트를 표시하지 않음
    def my_autopct(pct):
        return f'{pct:.1f}%' if pct >= 5 else ''

    keyword_counts.plot(kind='pie', autopct=my_autopct, startangle=90, counterclock=False, labeldistance=1.1, pctdistance=0.85)

    # 그래프 제목 설정
    plt.title('키워드 비율')

    img = BytesIO()

    plt.savefig(img, format='png', dpi=200)  # plt.saving 대신 plt.savefig 사용

    img.seek(0)

    return send_file(img, mimetype='image/png')

@bp.route("/area")
def investigation_area():
    # 특정 조건에 따라 데이터 필터링
    contains_high_official_crime_investigation = data[data.iloc[:, 1].str.contains('정치') &
                                                     data.iloc[:, 0].str.contains('고위공직자범죄수사처')]

    contains_prosecution_only = data[data.iloc[:, 1].str.contains('정치') &
                                      ~data.iloc[:, 0].str.contains('고위공직자범죄수사처') &
                                      data.iloc[:, 0].str.contains('검찰')]

    contains_national_assembly_only = data[data.iloc[:, 1].str.contains('정치') &
                                           ~data.iloc[:, 0].str.contains('고위공직자범죄수사처') &
                                           ~data.iloc[:, 0].str.contains('검찰') &
                                           data.iloc[:, 0].str.contains('국회')]

    not_contains_either = data[data.iloc[:, 1].str.contains('정치') &
                                ~data.iloc[:, 0].str.contains('고위공직자범죄수사처') &
                                ~data.iloc[:, 0].str.contains('검찰') &
                                ~data.iloc[:, 0].str.contains('국회')]

    # 결과를 그래프로 표시
    plt.switch_backend('Agg')  # Agg 백엔드로 전환
    plt.clf()  # 현재 그림 초기화
    plt.figure(figsize=(10, 6))

    # Combine the data into a single DataFrame with swapped positions of '기타' and ' 국회'
    plot_data = pd.DataFrame({
        '고위공직자범죄수사처': len(contains_high_official_crime_investigation),
        '검찰': len(contains_prosecution_only),
        '기타': len(not_contains_either),
        '국회': len(contains_national_assembly_only)
    }, index=[0])

    # Use seaborn pie chart to display the counts
    plt.pie(plot_data.values.flatten(), labels=plot_data.columns, autopct='%1.1f%%',
            startangle=140, colors=sns.color_palette('pastel'))

    # 그래프에 타이틀 추가
    plt.title('수사 구역')

    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)

    return send_file(img, mimetype='image/png')

@bp.route("/finance")
def finance_crime_chart():
    # 필요한 데이터 필터링
    contains_voice_phishing = data[data.iloc[:, 1].str.contains('금융') & data.iloc[:, 0].str.contains('보이스피싱')]
    contains_fraud_only = data[data.iloc[:, 1].str.contains('금융') & ~data.iloc[:, 0].str.contains('보이스피싱') & data.iloc[:, 0].str.contains('사기')]
    not_contains_either = data[data.iloc[:, 1].str.contains('금융') & ~data.iloc[:, 0].str.contains('보이스피싱') & ~data.iloc[:, 0].str.contains('사기')]

    # Combine the data into a single DataFrame
    plot_data = pd.DataFrame({
        '포함': [len(contains_voice_phishing), len(not_contains_either), len(contains_fraud_only)],
    }, index=['보이스 피싱', '기타', '사기'])

    matplotlib.use('Agg')

    # 결과를 둥근 그래프로 표시
    plt.figure(figsize=(10, 6))
    # Use seaborn pie chart to display the counts
    plt.pie(plot_data['포함'], labels=plot_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    # 그래프에 타이틀 추가
    plt.title('금융 범죄의 종류')

    # 이미지를 BytesIO로 저장하고 반환
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
    img.seek(0)

    return send_file(img, mimetype='image/png')