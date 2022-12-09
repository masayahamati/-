import pandas as pd
import glob

df=pd.read_csv(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\マーチェンダイズ福岡の売り上げデータ\202212091730570471_KSD0002.csv",encoding="SHIFT-JIS")

print(df)

df_kakou=pd.DataFrame(columns=df.columns)
df_seisen=pd.DataFrame(columns=df.columns)
df_kasi=pd.DataFrame(columns=df.columns)

file_lists=glob.glob(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\マーチェンダイズ福岡の売り上げデータ\*csv")


for file_lis in file_lists:
    df=pd.read_csv(file_lis,encoding="SHIFT-JIS")
    for i in range(len(df)):
        if i%3==0:
            df_kakou=pd.concat([df_kakou,df.iloc[[i],:]],axis=0)
        if i%3==1:
            df_seisen=pd.concat([df_seisen,df.iloc[[i],:]],axis=0)
        if i%3==2:
            df_kasi=pd.concat([df_kasi,df.iloc[[i],:]],axis=0)
    #ilocにするときデータフレームとしてとりだしたいので[i]で指定する。



"""
for i in range(len(df)):
    if i%3==0:
        df_kakou=pd.concat([df_kakou,df.iloc[[i],:]],axis=0)
    if i%3==1:
        df_seisen=pd.concat([df_seisen,df.iloc[[i],:]],axis=0)
    if i%3==2:
        df_kasi=pd.concat([df_kasi,df.iloc[[i],:]],axis=0)
#ilocにするときデータフレームとしてとりだしたいので[i]で指定する。
"""









