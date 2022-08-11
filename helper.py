import numpy as np


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
        'Gold', ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].unique().tolist()
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


# now we need to work on the functions which actually make those filters work
def fetch_medal_tally(df, year, country):
    filtered_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = filtered_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = filtered_df[filtered_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = filtered_df[filtered_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = filtered_df[(filtered_df['region'] == country) & (filtered_df['Year'] == int(year))]

    if flag == 1:
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                          ascending=True).reset_index()
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                            ascending=False).reset_index()

    temp_df['total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df['Gold'] = temp_df['Gold'].astype('int')
    temp_df['Silver'] = temp_df['Silver'].astype('int')
    temp_df['Bronze'] = temp_df['Bronze'].astype('int')
    temp_df['total'] = temp_df['total'].astype('int')

    return temp_df


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)

    return nations_over_time


def most_successful(df, sport):
    # first we'll remove those rows where medal = NaN, as here we'll count medals. So no need to keep'em.
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df = \
        temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
            ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    temp_df.rename(columns={'index': 'Name', 'Name_x': 'No of medals'}, inplace=True)

    return temp_df


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_sport_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_country_wise(df, country):
    # first we'll remove those rows where medal = NaN, as here we'll count medals. So no need to keep'em.
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    temp_df = \
        temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
            ['index', 'Name_x', 'Sport']].drop_duplicates('index')

    temp_df.rename(columns={'index': 'Name', 'Name_x': 'No of medals'}, inplace=True)

    return temp_df


def weight_vs_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = men.merge(women, on='Year', how='left')
    final_df.rename(columns={"Name_x": 'Male', "Name_y": 'Female'}, inplace=True)
    final_df.fillna(0, inplace=True)

    return final_df


