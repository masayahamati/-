import openpyxl
import pandas as pd
import matplotlib.pyplot as plt 


wb=openpyxl.load_workbook(r"C:\Users\masay\Downloads\21432_KSD0002_税抜_日単一市場.xlsx",data_only=True)
ws=wb["実績推移"]


df=pd.DataFrame(ws.values)
amount_df=df.iloc[32:36,2:45]
amount_df.index=amount_df.loc[:,2]
amount_df=amount_df.loc[:,3:45]
pd.to_datetime(amount_df.iloc[0,:])
#データフレームを成型した。日付けをdate型に変換

#print(amount_df.loc[32,:])
#注意このデータフレームはindexとカラム名が数字でなので数字で指定する必要がある。名前で指定しているので数字だがlocでOK



fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot_date(amount_df.iloc[0,:],amount_df.iloc[1,:], label='kakou', linestyle='solid')
ax.plot_date(amount_df.iloc[0,:],amount_df.iloc[2,:], label='seisen', linestyle='solid')
ax.plot_date(amount_df.iloc[0,:],amount_df.iloc[3,:], label='kasi', linestyle='solid')
ax.legend()




import statsmodels.graphics.api as smg
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(amount_df.iloc[1,:],lags=29)

plt.show()








