import pandas as pd

filename = "test.csv"

df = pd.read_csv(filename, encoding="gbk")

df_modified = df[df.columns[:-1]]
df_modified.columns = df.columns[1:]
df = df_modified

# print(df.to_html(classes=['table', 'table-striped']))
