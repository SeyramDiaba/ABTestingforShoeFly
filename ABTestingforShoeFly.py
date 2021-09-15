import codecademylib
import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')

# Analysing first few rows of 'ad_clicks'
print ad_clicks.head()

# Which platform is generating the most views
most_views = ad_clicks.groupby('utm_source').user_id.count().reset_index()

# Was the ad clicked or not
ad_clicks['is_click']= ~ad_clicks\
   .ad_click_timestamp.isnull()
print ad_clicks.is_click

#Percentage of people who click on ads from each source
clicks_by_source= ad_clicks.groupby(['utm_source','is_click'])['user_id'].count().reset_index()

#now lets pivot the data
clicks_pivot = clicks_by_source.pivot(
  columns = 'is_click',
  index = 'utm_source',
  values = 'user_id'
).reset_index()
print clicks_pivot

#percent of users who clicked on each source
clicks_pivot['percent_clicked']= (clicks_pivot[True]/(clicks_pivot[True] + clicks_pivot[False])) * 100
print clicks_pivot['percent_clicked']
# Was Ad A & B shown to the same number of people
experiment = ad_clicks.groupby('experimental_group').user_id.count().reset_index()

print ad_clicks.head()
#checking for greater ad view percentage by A or B
greater_ad_view = ad_clicks.groupby(['is_click','experimental_group']).user_id.count().reset_index()
greater_ad_view_pivot = greater_ad_view.pivot(
  columns = 'is_click',
  index = 'experimental_group',
  values = 'user_id'
).reset_index()
print greater_ad_view_pivot

#DataFrames for A and B ads
a_clicks = ad_clicks[ad_clicks['experimental_group'] == 'A']
b_clicks = ad_clicks[ad_clicks['experimental_group'] == 'B']


# Clicks by day
clicks_by_day_a= a_clicks.groupby(['is_click','day']).user_id.count().reset_index().pivot(
  columns = 'is_click',
  index = 'day',
  values = 'user_id'
)
print clicks_by_day_a

clicks_by_day_b= b_clicks.groupby(['is_click','day']).user_id.count().reset_index().pivot(
  columns = 'is_click',
  index = 'day',
  values = 'user_id'
)
print clicks_by_day_b

#percentage of clicks by day
clicks_by_day_a['percentage_a'] = ((clicks_by_day_a[True]/(clicks_by_day_a[True]+clicks_by_day_a[False])) * 100)


clicks_by_day_b['percentage_b'] = ((clicks_by_day_b[True]/(clicks_by_day_b[True]+clicks_by_day_b[False])) * 100)

print clicks_by_day_a['percentage_a']
print clicks_by_day_b['percentage_b']

#comparing results for A and B
#i will find the average of each to determine which of the ads to recommend
rec_a = clicks_by_day_a['percentage_a'].mean()
rec_b = clicks_by_day_b['percentage_b'].mean()
print(rec_a,rec_b)
#Ad A is highly recommended 