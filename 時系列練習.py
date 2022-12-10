import pandas as pd
import datetime as dt
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import xlrd
import statsmodels.api as sm

wb=xlrd.open_workbook(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\Sample - Superstore.xls")
sheet=wb.sheet_by_name('superstore')

def get_list_2d_all(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]

lis=get_list_2d_all(sheet)

df=pd.DataFrame(lis[1:],columns=lis[0])

df['Order Date']=pd.to_timedelta(df['Order Date'],unit='D')+pd.to_datetime("1899/12/30")
df['Ship Date']=pd.to_timedelta(df['Ship Date'],unit='D')+pd.to_datetime("1899/12/30")

df_sort=df.sort_values(by="Order Date").reset_index()


df_sale=pd.DataFrame(df_sort[["Order Date","Sales"]])
df_sale=df_sale.set_index(df_sale["Order Date"])
df_sale=df_sale.resample("1D").sum()
"""日にちが複数にわたるものがあったのでそれを足し合わせる"""



fig=plt.figure()
ax=fig.add_subplot(2,1,1)
ax2=fig.add_subplot(2,1,2)
ax.plot(df_sale.index,df_sale["Sales"])
sm.graphics.tsa.plot_acf(df_sale["Sales"],lags=37)
plt.title("原系列のコレログラム",fontname="MS Gothic")
"""自己相関があることが分かるのでとりあえずARMAモデルを適用させる"""

train_y=df_sale.loc[:"2017-09-30","Sales"]
print(train_y)

sarima_model=sm.tsa.SARIMAX(train_y,order=(7,0,7),enforce_stationarity=True,
                                                enforce_invertibility=True)
sarima_results=sarima_model.fit()



'''aic_lis=[]
aic_error_lis=[]
for i in range(10):
    for j in range(10):
        sarima_model=sm.tsa.SARIMAX(train_y,order=(i,0,j),enforce_stationarity=True,
                                                        enforce_invertibility=True)
        """enforsce_stationarityはモデルを作るとき定常状態を保ったまま作るということ。定常状態は一つ式が増えるので
        縛りが増えることになる。"""
        try:
            sarima_results=sarima_model.fit()
            aic_lis.append([i,j,sarima_results.aic])
        except:
            aic_error_lis.append([i,j])
            print("UnexceptedError")


aic_lis=sorted(aic_lis,reverse=False,key=lambda x:x[2])
print(aic_lis)
print("------------------------")
print(aic_error_lis)
'''



