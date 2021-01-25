import pandas as pd

# Read
a = pd.read_csv("score_mid.csv", index_col=None)
b = pd.read_csv("score_fin.csv", index_col=None)
c = pd.read_csv("score_hw.csv", index_col=None)

# Make id same
a.iloc[:, 0] = a.iloc[:, 0].str.lower()
b.iloc[:, 0] = b.iloc[:, 0].str.lower()
c.iloc[:, 0] = c.iloc[:, 0].str.split("@").str[0]

# Rename column
a = a.add_prefix("mid_")
b = b.add_prefix("fin_")
c = c.add_prefix("hw_")

# first column as ID
a.rename(columns={a.columns[0]:"ID"}, inplace=True)
b.rename(columns={b.columns[0]:"ID"}, inplace=True)
c.rename(columns={c.columns[0]:"ID"}, inplace=True)

# Custom columns. Edit here. Make sure sum is at the last column")
a = a.iloc[:, [0, 1] + list(range(9, 23))]
b = b.iloc[:, [0, 1] + list(range(9, 19)) + [20]]
c = c.iloc[:, list(range(0, 14)) + [15, 14]]
c.iloc[:, 0] = c.iloc[:, 0].str.replace("b05502157", "r09522609")

# Check remove ID
a = a.loc[~a.loc[:, "ID"].isna()]
b = b.loc[~b.loc[:, "ID"].isna()]
c = c.loc[~c.loc[:, "ID"].isna()]
assert len(a) == len(set(a["ID"]) - set(["nan"]))
assert len(b) == len(set(b["ID"]) - set(["nan"]))
assert len(c) == len(set(c["ID"]) - set(["nan"]))

# Merge
m = a.merge(b, how="outer", on="ID", sort=True)\
     .merge(c, how="outer", on="ID", sort=True)
m = m.loc[~m.loc[:, "ID"].isna()]
print("Merged")
print(m)

# Calculate sum of scores
m['All'] = 0.3 * m.iloc[:, len(a.columns) - 1] \
         + 0.3 * m.iloc[:, len(a.columns) - 1 + len(b.columns) - 1] \
         + 0.4 * m.iloc[:, -1]
m = m.sort_values(by="All")

# save
m.to_csv("score_merge.csv", index=False, encoding="utf-8-sig")

# shrink the column
m = m.iloc[:, [0, 1, len(a.columns) - 1, len(a.columns) - 1 + len(b.columns) - 1, -2]]
m.columns = ["tmp_ID", "Name", "Midterm", "Final", "HW_average"]

# read and find user id
d = pd.read_csv("score_ntucool.csv", index_col=None)
d = d[d["Student"] != "測試學生"]
d["tmp_ID"] = d.loc[:, "SIS Login ID"].str.split("@").str[0]

# merge
d = d.merge(m, how="left", on="tmp_ID", sort=True)
d = d.drop(columns=["tmp_ID", "Name"])
print("Merge to NTUcool")
print(d)

# save
d.to_csv("score_merge_ntucool.csv", index=False, encoding="utf-8-sig")
