import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from matplotlib import dates as dates
import numpy as np

df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\事務所別月別ゴミ収集量.csv",encoding="Shift_JIS")
df=df.dropna(axis=1)
df.columns=["date","data"]
df["date"]=pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
print(df)