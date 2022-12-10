import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from matplotlib import mlab
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import numpy as np

sarima_aic_lis=[]


garvege_df=pd.read_excel(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\福岡市一日当たりの可燃ゴミ.xlsx")

garvege_df=garvege_df.iloc[2:,1:]
garvege_df.columns=["日付","曜日","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]
garvege_df["日付"]=pd.to_datetime(garvege_df['日付'])



kasi_df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\マーチェンダイズ福岡の加工データ\kasi.csv",encoding="SHIFT-JIS")
kakou_df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\マーチェンダイズ福岡の加工データ\kakou.csv",encoding="SHIFT-JIS")
seisen_df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\マーチェンダイズ福岡の加工データ\seisen.csv",encoding="SHIFT-JIS")


kasi_df=kasi_df.loc[:,["日付","数量"]]
kakou_df=kakou_df.loc[:,["日付","数量"]]
seisen_df=seisen_df.loc[:,["日付","数量"]]

kasi_df["日付"]=pd.to_datetime(kasi_df['日付'])
kakou_df["日付"]=pd.to_datetime(kakou_df['日付'])
seisen_df["日付"]=pd.to_datetime(seisen_df['日付'])


kasi_and_garvege_df=pd.merge(kasi_df,garvege_df,how="inner",on="日付")
kakou_and_garvege_df=pd.merge(kakou_df,garvege_df,how="inner",on="日付")
seisen_and_garvege_df=pd.merge(seisen_df,garvege_df,how="inner",on="日付")


scaler = StandardScaler()
kasi_gar_scr= scaler.fit_transform(kasi_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]])
kakou_gar_scr= scaler.fit_transform(kakou_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]])
seisen_gar_scr= scaler.fit_transform(seisen_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]])



kasi_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]]=kasi_gar_scr
kakou_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]]=kakou_gar_scr
seisen_and_garvege_df.loc[:,["数量","東部工場(重量)","西部工場(重量)","臨海工場(重量)","南部工場(重量)"]]=seisen_gar_scr


fig1=plt.figure()
ax=fig1.add_subplot(4,1,1)
ax2=fig1.add_subplot(4,1,2)
ax3=fig1.add_subplot(4,1,3)
ax4=fig1.add_subplot(4,1,4)

ax.xcorr(kasi_and_garvege_df['数量'], 
        kasi_and_garvege_df['東部工場(重量)'],
        detrend=mlab.detrend_none, 
        maxlags=14,
        label="kasi")

ax2.xcorr(kakou_and_garvege_df['数量'], 
        kakou_and_garvege_df['東部工場(重量)'],
        detrend=mlab.detrend_none, 
        maxlags=14,
        label="kakou")

ax3.xcorr(seisen_and_garvege_df['数量'], 
        seisen_and_garvege_df['東部工場(重量)'],
        detrend=mlab.detrend_none, 
         maxlags=14,
         label="seisen")

ax.legend()
ax2.legend()
ax3.legend()



fig,ax = plt.subplots(2,1,figsize=(12,8))
fig = sm.graphics.tsa.plot_acf(garvege_df["東部工場(重量)"], lags=14, ax=ax[0], color="darkgoldenrod")
fig = sm.graphics.tsa.plot_pacf(garvege_df["東部工場(重量)"], lags=14, ax=ax[1], color="darkgoldenrod")

#ゴミのデータは一週間周期で動いているようなデータである。

plt.show()




#10か月分のデータなので一週間に直すと約43週分ある。




x_train, x_test, y_train, y_test = train_test_split(kasi_and_garvege_df[["数量"]],
                                                    kasi_and_garvege_df[["東部工場(重量)"]],
                                                    shuffle=False,
                                                    train_size=0.7)




"""
aic_lis=[]
aic_error_lis=[]
for i in range(10):
    for j in range(10):
        sarima_model=sm.tsa.SARIMAX(y_train,exog=x_train,order=(i,0,j),enforce_stationarity=True,
                                                        enforce_invertibility=True)
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

"""


sarima_model=sm.tsa.SARIMAX(y_train,exog=x_train,order=(8,0,4),enforce_stationarity=True,
                                                        enforce_invertibility=True)

sarima_results=sarima_model.fit()





#303のデータがある

print(kasi_and_garvege_df.iloc[212:303,2])
#説明変数の時系列データをpredictするとき渡す必要がある。


print(sarima_results.predict())
print(sarima_results.predict(start=212,end=302,exog=x_test))



lis1=list(sarima_results.predict())
lis2=list(sarima_results.predict(start=212,end=302,exog=x_test))

graph_df=pd.DataFrame(data=lis1+lis2,
                      columns=["東部工場(重量)"])

print(graph_df)




fig=plt.figure()
ax=fig.add_subplot(1,1,1)



ax.plot(kasi_and_garvege_df["日付"],kasi_and_garvege_df["東部工場(重量)"],label="実測値")
ax.plot(kasi_and_garvege_df["日付"],graph_df["東部工場(重量)"],label="予測値")
ax.set_title("ARIMAX モデル", c="darkred", size="large",fontname="MS Gothic")
ax.legend(prop={"family":"MS Gothic"})



plot = sarima_results.plot_diagnostics()
plt.show()


sarima_aic_lis.append(sarima_results.aic)


print(sarima_results.summary())

#===============================================================================================================





new_kasi_and_garvege_df=kasi_and_garvege_df
new_kasi_and_garvege_df["lag2"]=kasi_and_garvege_df["数量"].shift(2)
new_kasi_and_garvege_df=new_kasi_and_garvege_df.dropna(axis=0).reset_index(drop=True)


x_train, x_test, y_train, y_test = train_test_split(new_kasi_and_garvege_df[["lag2"]],
                                                    new_kasi_and_garvege_df[["東部工場(重量)"]],
                                                    shuffle=False,
                                                    train_size=0.7)


print(x_test,x_train)

sarima_model=sm.tsa.SARIMAX(y_train,exog=x_train,order=(8,0,4),enforce_stationarity=True,
                                                        enforce_invertibility=True)

sarima_results=sarima_model.fit()

lis1=list(sarima_results.predict())
lis2=list(sarima_results.predict(start=210,end=300,exog=x_test))

graph_df=pd.DataFrame(data=lis1+lis2,
                      columns=["東部工場(重量)"])

print(graph_df)




fig=plt.figure()
ax=fig.add_subplot(1,1,1)



ax.plot(new_kasi_and_garvege_df["日付"],new_kasi_and_garvege_df["東部工場(重量)"],label="実測値")
ax.plot(new_kasi_and_garvege_df["日付"],graph_df["東部工場(重量)"],label="予測値")
ax.set_title("ARIMAX モデル", c="darkred", size="large",fontname="MS Gothic")
ax.legend(prop={"family":"MS Gothic"})



plot = sarima_results.plot_diagnostics()
plt.show()


sarima_aic_lis.append(sarima_results.aic)


print(sarima_aic_lis)



