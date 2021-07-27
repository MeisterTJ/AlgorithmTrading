import numpy as np
from pandas import DataFrame

data = {'빗썸': [100, 100, 100],
        '코빗' : [90, 100, 120]}      # 빗썸, 코빗은 행들의 대표 라벨, 뒤에는 각 행에 들어가는 값들

df = DataFrame(data)

# DataFrame에 최저가를 추가하고 각 행에 어떤 것이 더 작은지 넣는다.
df['최저가'] = np.where(df['빗썸'] < df['코빗'], '빗썸', '코빗')
df.to_excel("거래소.xlsx")