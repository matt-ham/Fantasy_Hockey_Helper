import pandas as pd
from database import conn
pd.options.mode.chained_assignment = None  # default='warn'

def fixUp(dataframe):

    dataframe = dataframe.loc[:, dataframe.columns[[0,1,2,3,4,5,6,9,11,12,13,14,15,16]]]
    dataframe.insert(7,'PPP',0)
    dataframe.insert(8,'SHP',0)
    dataframe.insert(7,'PtsPerG',0.0)
    dataframe.insert(8,'fPts',0.0)
    dataframe.insert(9,'fPtsPerG',0.0)
    dataframe.rename(columns = {'Games':'GP','Player Name': 'Player','G.1':'PPG','A.1':'PPA','G.2':'SHG','A.2':'SHA'}, inplace = True)
    
    for i in range(len(dataframe)):
        dataframe['PPP'][i] = dataframe['PPG'][i]+dataframe['PPA'][i]
        dataframe['SHP'][i]  = dataframe['SHG'][i]+dataframe['SHA'][i]

        if dataframe['Pos'][i] != 'D':
            dataframe['Pos'][i] = 'F'
        
        if dataframe['GP'][i]<10 or dataframe['Pts'][i]<3:
            dataframe = dataframe.drop(i)
        else:
            dataframe['PtsPerG'][i] = round((int(dataframe['Pts'][i]) / int(dataframe['GP'][i])),2)
            name = dataframe['Player'][i]
            dataframe['fPts'][i] = fantasyPtsPer82(name,dataframe)
            dataframe['fPtsPerG'][i] = round((int(dataframe['fPts'][i]) / int(dataframe['GP'][i])),1)


    dataframe = dataframe.drop(columns=['PPG', 'PPA','SHG','SHA'])


    return dataframe

def fantasyPtsPer82(name,df):
  
   
    g = int(df[df['Player']==name]['G'].values)
    a = int(df[df['Player']==name]['A'].values)
    s = int(df[df['Player']==name]['SOG'].values)
    h = int(df[df['Player']==name]['Hits'].values)
    b = int(df[df['Player']==name]['BS'].values)
    ppp = int(df[df['Player']==name]['PPP'].values)
    shp = int(df[df['Player']==name]['SHP'].values)


    pts = round(((2*g)+(a)+(0.1*s)+(0.1*h)+(0.5*b))+((ppp*0.5)+(shp*0.5)),2)
    return pts
def calculate_avg_per_game(df, column):
    return ((df[f'{column}_x'].fillna(0) + df[f'{column}_y'].fillna(0) + df[column].fillna(0)) / df['GP']) * 82

def calculate_averages(df):
    df['GP'] = df['GP_x'].fillna(0) + df['GP_y'].fillna(0) + df['GP'].fillna(0)
    df['G'] = calculate_avg_per_game(df, 'G')
    df['A'] = calculate_avg_per_game(df, 'A')
    df['Pts'] = df['G'] + df['A']
    df['PtsPerG'] = df['Pts'] / 82
    df['PPP'] = calculate_avg_per_game(df, 'PPP')
    df['fPts'] = calculate_avg_per_game(df, 'fPts')
    df['SHP'] = calculate_avg_per_game(df, 'SHP')
    df['SOG'] = calculate_avg_per_game(df, 'SOG')
    df['fPtsPerG'] = df['fPts'] / 82
    df['Hits'] = calculate_avg_per_game(df, 'Hits')
    df['BS'] = calculate_avg_per_game(df, 'BS')
    df['GP'] = 82
    df = df.loc[:, df.columns[[0, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]]]
    df = df.round(1)
    return df

## Clean all csv's

stats_20 = pd.read_csv("csv/2020-2021.csv")
stats_20 = fixUp(stats_20)

stats_21 = pd.read_csv("csv/2021-2022.csv")
stats_21 = fixUp(stats_21)

stats_22 = pd.read_csv("csv/2022-2023.csv")
stats_22 = fixUp(stats_22)

stats_20.to_csv('csv/cleaned/20-21.csv', encoding='utf-8', index=False)
stats_21.to_csv('csv/cleaned/21-22.csv', encoding='utf-8', index=False)
stats_22.to_csv('csv/cleaned/22-23.csv', encoding='utf-8', index=False)

average_df = pd.merge(stats_20, stats_21, on='Player', how='outer')
average_df = pd.merge(average_df,stats_22,on='Player', how='outer')
average_df = calculate_averages(average_df)

stats_20 = stats_20.assign(Drafted=False)
stats_21 = stats_21.assign(Drafted=False)
stats_22 = stats_22.assign(Drafted=False)
average_df = average_df.assign(Drafted=False)


## Populate database

stats_20.to_sql('stats2020',conn, if_exists='replace', index=False)
stats_21.to_sql('stats2021',conn, if_exists='replace', index=False)
stats_22.to_sql('stats2022',conn, if_exists='replace', index=False)
average_df.to_sql('statsAverage',conn, if_exists='replace', index=False)