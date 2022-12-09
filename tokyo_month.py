import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from matplotlib import mlab

df=pd.read_excel(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\事務所別月別ごみ収集量.xlsx")

df=df.iloc[35:96,[1,2]].reset_index(drop=True)
df.columns=["month","amount"]
df["month"]=pd.to_datetime(df['month'],format='%Y年%m月')

gavege_df=df


df2=pd.read_excel(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\2019販売個数.xlsx")

print(gavege_df["month"][24:])


df2=df2.iloc[16:19,1:].reset_index(drop=True)
df2.index=["加工食品",
            "生鮮食品",
            "菓子類"]
df2.columns=gavege_df["month"][24:]

product_df=df2.T
product_df=product_df.reset_index()
print(product_df)


gavege_df=gavege_df.iloc[24:,:].reset_index(drop=True)

mix_df=pd.merge(gavege_df,product_df)
mix_df=mix_df.iloc[1:,:]

print(mix_df)


scaler = StandardScaler()
df_sca= scaler.fit_transform(mix_df.loc[:,["amount","加工食品","生鮮食品","菓子類"]])



mix_df["amount"]=df_sca[:,0]
mix_df["加工食品"]=df_sca[:,1]
mix_df["生鮮食品"]=df_sca[:,2]
mix_df["菓子類"]=df_sca[:,3]


fig=plt.figure()
ax=fig.add_subplot(3,1,1)
ax2=fig.add_subplot(3,1,2)
ax3=fig.add_subplot(3,1,3)

ax.xcorr(mix_df['amount'], 
        mix_df['加工食品'],
        detrend=mlab.detrend_none, 
        maxlags=12,
        label="kakou")

ax2.xcorr(mix_df['amount'], 
        mix_df['生鮮食品'],
        detrend=mlab.detrend_none, 
        maxlags=12,
        label="seisen")

ax3.xcorr(mix_df['amount'], 
        mix_df['菓子類'],
        detrend=mlab.detrend_none, 
         maxlags=12,
         label="kasirui")

ax.legend()
ax2.legend()
ax3.legend()

plt.show()



