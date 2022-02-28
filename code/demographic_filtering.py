import pandas as pd
import numpy as np
df1 = pd.read_csv('articles.csv')
def find_total_events(df1_row):
  total_likes = df1[(df1_row["contentId"])].shape[0]
  total_views = df1[df1_row["contentId"]].shape[0]
  total_bookmarks = df1[df1_row["contentId"]].shape[0]
  total_follows = df1[df1_row["contentId"]].shape[0]
  total_comments = df1[df1_row["contentId"]].shape[0]
  return total_likes + total_views + total_bookmarks + total_follows + total_comments

df1["total_events"] = df1.apply(find_total_events, axis=1)

output = df1.head(20).values.tolist()

