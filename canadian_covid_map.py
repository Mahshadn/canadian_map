import pandas as pd
import plotly_express as px
import json

df = pd.read_csv("ca_pr_day_comp.csv")
df['category'] = ''

#categorizing the number of cases and assign each category to each row
def set_cat(row):
    if row['cases'] == 0:
        return '0'
    if row['cases'] > 0 and row['cases'] < 1001:
        return '1 - 1,000'
    if row['cases'] > 1001 and row['cases'] < 5001:
        return '1,001 - 5,000'
    if row['cases'] > 5001 and row['cases'] < 10001:
        return '5,001 - 10,000'
    if row['cases'] > 10001 and row['cases'] < 30001:
        return '10,001 - 30,000'
    if row['cases'] > 30001 and row['cases'] < 50001:
        return '30,001 - 50,000'
    if row['cases'] > 50001:
        return '50,001 and higher'

df = df.assign(category=df.apply(set_cat, axis=1))

# Adds all available categories to each time frame
catg = df['category'].unique()
dts = df['timeframe'].unique()

for tf in dts:
    for i in catg:
        df = df.append({
            'timeframe' : tf,
            'cases' : 'N',
            'cartodb_id' : '0',
            'category' : i
        }, ignore_index=True)

# assign mp to the geojson data
with open("canada_provinces.geojson", "r") as geo:
    mp = json.load(geo)

# Create choropleth map
fig = px.choropleth(df,
                    locations="cartodb_id",
                    geojson=mp,
                    featureidkey="properties.cartodb_id",
                    color="category",
                    color_discrete_map={
                        '0': '#fffcfc',
                        '1 - 1,000' : '#ffdbdb',
                        '1,001 - 5,000' : '#ffbaba',
                        '5,001 - 10,000' : '#ff9e9e',
                        '10,001 - 30,000' : '#ff7373',
                        '30,001 - 50,000' : '#ff4d4d',
                        '50,001 and higher' : '#ff0d0d'},
                    category_orders={
                      'category' : [
                          '0',
                          '1 - 1,000',
                          '1,001 - 5,000',
                          '5,001 - 10,000',
                          '10,001 - 30,000',
                          '30,001 - 50,000',
                          '50,001 and higher'
                      ]
                    },
                    animation_frame="timeframe",
                    scope='north america',
                    title='<b>COVID-19 cases in Canadian provinces</b>',
                    labels={'cases' : 'Number of Cases',
                            'category' : 'Category'},
                    hover_name='province',
                    hover_data={
                        'cases' : True,
                        'cartodb_id' : False
                    },
                    # height=900,
                    locationmode='geojson-id',
                    )

# Adjust map layout stylings
fig.update_layout(
    showlegend=True,
    legend_title_text='<b>Total Number of Cases</b>',
    font={"size": 16, "color": "#808080", "family" : "calibri"},
    margin={"r":0,"t":40,"l":0,"b":0},
    legend=dict(orientation='v'),
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#e0fffe')
)

# Adjust map geo options
fig.update_geos(showcountries=False, showcoastlines=False,
                showland=False, fitbounds="locations",
                subunitcolor='white')
fig.show()
