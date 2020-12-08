# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy.stats as stat
import tableone
import datetime

# +
df = pd.read_csv('T1_contents_final.csv')
df['event']=df['Value']>3
df['event']=df['event'].astype(int)
df['gender']=df['gender'].astype(str)

print(df.dtypes)
# -

# 그룹 지정 컬럼명
group_col = 'event'

# 통계 돌릴 컬럼 목록
#cols = df.columns.tolist()  # 전체 컬럼을 모두 지정
#cols.remove(group_col)
cols = ['age', 'gender', 'weight','height', 'Anetime','Optime']  # 내가 원하는 변수만 출력 순서를 지정

# 카테고리 변수인 컬럼을 찾아냄
categorical_cols = ['gender']  # 카테고리 변수 수동 지정
continuous_cols = ['age', 'weight','height', 'Anetime','Optime']  # 연속 변수 수동 지정
for c in cols:  # 카테고리 변수인지 자동으로 확인
    if c in categorical_cols:
        continue
    if c in continuous_cols:  # 사용자가 수기로 지정한 경우
        try:
            df[c] = df[c].astype(float)  # 숫자 형태로 변환해보고 에러나면 사용자에게 알림
        except:
            print('variable {} contains non-numeric value'.format(c))
            categorical_cols.append(c)
            continue
        continue
    try:
        df[c] = df[c].astype(float)  # 숫자 형태로 변환해보고 에러나면 카테고리 변수
    except:
        categorical_cols.append(c)
        continue
    # 숫자 형태인 경우라도
    if len(df[c].unique()) < 6: # 유일 값이 6개 미만이면 카테고리 변수
        categorical_cols.append(c)
for c in categorical_cols: # 카테고리 변수는 전부 문자열로 바꿈
    df[c] = df[c].astype(str)

# 비정규 분포인 컬럼을 찾아냄
non_normal_cols = []  # 전부 정규분포 --> 모수 통계
for c in cols:  # Shapiro-Wilk test 를 이용하여 각 변수가 정규 분포인지 확인
    if c in categorical_cols:
        continue
    if stat.shapiro(df[c])[1] < 0.05:
        non_normal_cols.append(c)

# 군간 비교 수행 
df_res = tableone.TableOne(df, columns=cols, categorical=categorical_cols, nonnormal=non_normal_cols, groupby=group_col, pval=True, htest_name=True)

print(non_normal_cols)

# 결과 저장
df_res.to_csv('result_final.csv')
