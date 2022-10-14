from difflib import restore
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
import matplotlib.pyplot as plt
import statsmodels.api as sm
from matplotlib import dates as dates
import numpy as np


df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\事務所別月別ゴミ収集量.csv",encoding="Shift_JIS")
df=df.dropna(axis=1)
df.columns=["date","data"]
df["date"]=pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
train_y=df.iloc[:48,1:]


def root_mean_squared_error(y_true, y_pred,test_index):
    y_true=y_true[test_index:].to_numpy()
    y_pred=y_pred[test_index:].to_numpy()
    mse = np.power(y_true - y_pred, 2).mean()
    return np.sqrt(mse)

#原系列のコレログラム
sm.graphics.tsa.plot_acf(df.iloc[:,1],lags=37)
plt.title("原系列のコレログラム",fontname="MS Gothic")





ar_model=AutoReg(train_y,10)
results=ar_model.fit()
df["ar_pred"]=results.predict(start=0,end=60)
#データフレームに追加.predictは配列を返す
"""for i in range(11):
    ar_model=AutoReg(train_y,i)
    results=ar_model.fit()
    df["ar_pred"]=results.predict(start=0,end=60)
    print(f"lags={i}:aic={results.aic}")
    print(f"{root_mean_squared_error(df['data'],df['ar_pred'],48)}")


aic_lis=[]
aic_error_lis=[]
for i in range(11):
    for j in range(4):
        sarima_model=sm.tsa.SARIMAX(train_y,order=(i,0,0),seasonal_order=(j,0,0,12),enforce_stationarity=True)
        """"""enforsce_stationarityはモデルを作るとき定常状態を保ったまま作るということ。定常状態は一つ式が増えるので
        縛りが増えることになる。""""""
        try:
            sarima_results=sarima_model.fit()
            df["arima_pred"]=sarima_results.predict(start=0,end=60)
            print(f"lags={i},{j}:aic={sarima_results.aic}")
            aic_lis.append([i,j,sarima_results.aic,root_mean_squared_error(df['data'],df['arima_pred'],48)])
        except:
            aic_error_lis.append([i,j])
            print("UnexceptedError")


aic_lis=sorted(aic_lis,reverse=False,key=lambda x:x[2])
print(aic_lis)
print("------------------------")
print(aic_error_lis)
"""

"エラーでも処理を勧めてくれる機能。try exceptはfor文でエラーが出るときなどに有効"


fig = plt.figure(figsize=(16,9))
fig=results.plot_diagnostics(fig=fig, lags=37)
#arモデルの実装、グラフの描写
#fig.savefig("ar.png")
#pred=results.predict()




sarima_model=sm.tsa.SARIMAX(train_y,order=(7,0,0),seasonal_order=(1,0,0,12),enforce_stationarity=True)
sarima_results=sarima_model.fit()
print(sarima_results.aic)
df["arima_pred"]=sarima_results.predict(start=0,end=60)
#データフレームに追加.predictは配列を返す



sarima_fig = plt.figure(figsize=(16,9))
sarima_fig=sarima_results.plot_diagnostics(fig=sarima_fig,lags=37)
#sarimaモデルの実装、グラフの描写
#sarima_fig.savefig("sarima.png")



#↓ホワイトノイズの自己相関を表示する
fig_pred=plt.figure()
ax_ar=fig_pred.add_subplot(2,1,1)
ax_arima=fig_pred.add_subplot(2,1,2)

date_lis=[]
for i in range(60):
    if i%12==0:
        date_lis.append(df.iloc[i,0])
    else:
        date_lis.append("")
#グラフのx軸ラベルを分割するための処理ax_ar.set_xticklabels(date_lis)
#でリストを渡せば間隔をあけてx軸を書くことができる。
    

print(df)



ax_ar.plot(df.iloc[:,0],df.iloc[:,1],label="実測値")
ax_ar.plot(results.predict(start=0,end=48),"black",label="訓練データ")
ax_ar.plot(results.predict(start=47,end=60),"red",label="テストデータ")
ax_ar.set_ylim([190000,260000])
ax_ar.set_xticklabels(date_lis)
ax_ar.set_title("AR モデル", c="darkred", size="large",fontname="MS Gothic")
ax_ar.legend(prop={"family":"MS Gothic"})
#これは予測をする時に指定する必要があるもの.predict関数は予測するstart,endを指定する必要がある
#予測データは前の値を用いて出されるので、値がない部分のグラフは描かれない
#fontnameはmatplotlibで日本語表記するためのもの


ax_arima.plot(df.iloc[:,0],df.iloc[:,1],label="実測値")
ax_arima.plot(sarima_results.predict(start=0,end=48),"black",label="訓練データ")
ax_arima.plot(sarima_results.predict(start=47,end=60),"red",label="テストデータ")
ax_arima.set_ylim([190000,260000])
ax_arima.set_xticklabels(date_lis)
ax_arima.set_title("SAR モデル", c="darkred", size="large",fontname="MS Gothic")
ax_arima.legend(prop={"family":"MS Gothic"})




print(f"RMSEは{root_mean_squared_error(df['data'],df['ar_pred'],48)}")
print(f"RMSEは{root_mean_squared_error(df['data'],df['arima_pred'],48)}")





plt.show()
