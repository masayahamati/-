from difflib import restore
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
import matplotlib.pyplot as plt
import statsmodels.api as sm
from matplotlib import dates as dates
import numpy as np
# グラフを横長にする
from matplotlib.pylab import rcParams




df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\事務所別月別ゴミ収集量.csv",encoding="Shift_JIS")
df=df.dropna(axis=1)
df.columns=["date","data"]
df["date"]=pd.to_datetime(df["date"])
df=df.set_index("date")
#df内に含まれるdf["date"]の部分を丸ごとindexに置き換えたデータフレームを作成している。

mod_local_level = sm.tsa.UnobservedComponents(df, 'local level')
"""ここでlocallevelモデルを文字列で指定している。これは
次の状態=前の状態+状態誤差
観測=状態+観測誤差で表せるもっとも単純なモデルである。
ローカルレベルモデルのパラメータはこれらの誤差で表されこれを決めることによって
状態と観測のモデルを作ることができる。"""
res_local_level = mod_local_level.fit()
"""ここで最適な誤差の分散のパラメータを決定している。
決定の手法は最尤法である。"""

rcParams['figure.figsize'] = 15, 15
fig = res_local_level.plot_components()

mod_trend = sm.tsa.UnobservedComponents(df,'local linear trend')
"""これはローカル線形トレンドモデルでトレンドがあると仮定した場合に
つかう物である。これはトレンドの項に含まれるものがパラメータとして追加される"""

res_trend = mod_trend.fit()
rcParams['figure.figsize'] = 15, 20
fig = res_trend.plot_components()


mod_season_local_level = sm.tsa.UnobservedComponents(df,'local level',seasonal=12)
res_season_local_level = mod_season_local_level.fit(
    method='bfgs', 
    maxiter=500, 
    start_params=mod_season_local_level.fit(method='nm', maxiter=500).params,
)

rcParams['figure.figsize'] = 15, 20
fig = res_trend.plot_components()


plt.show()

