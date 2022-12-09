import pandas as pd
import glob



file_lists=glob.glob(r"C:\Users\masay\OneDrive\デスクトップ\福岡市ゴミのデータ\R1年度\一般家庭（可燃）搬入量\*xlsx")
print(file_lists)
df=pd.read_excel(r"C:\Users\masay\OneDrive\デスクトップ\福岡市ゴミのデータ\R1年度\一般家庭（可燃）搬入量\【一般家庭（可燃）搬入量】_201904.xlsx")
#---------------------------------------------------------

year_lists=["H30年度","R1年度","R2年度","R3年度"]
first_flag=True
for year_lis in year_lists:
    file_lists=glob.glob(r"C:\Users\masay\OneDrive\デスクトップ\福岡市ゴミのデータ\{year_lis}\一般家庭（可燃）搬入量\*xlsx".format(year_lis=year_lis))
    print(file_lists)
    for file_lis in file_lists:
        if first_flag:
            sum_df=pd.read_excel(file_lis)
            sum_df=sum_df.iloc[3:len(sum_df)-1,1:]
            first_flag=False
        else:
            add_df=pd.read_excel(file_lis)
            add_df=add_df.iloc[5:len(add_df)-1,1:]
            sum_df=pd.concat([sum_df,add_df])

sum_df=sum_df.reset_index(drop=True)


sum_df.to_excel(r"C:\Users\masay\OneDrive\デスクトップ\卒業論文\エクセルcsv\福岡市一日当たりの可燃ゴミ.xlsx")




























