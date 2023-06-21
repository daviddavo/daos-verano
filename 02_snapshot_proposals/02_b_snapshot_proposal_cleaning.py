import os
import pandas as pd

DIR_NAME = '1687359310'

directory_list = os.listdir(DIR_NAME)
directory_list = [x for x in directory_list if x.endswith('.csv')]
print(len(directory_list), 'directories found')

# read all csv files in the directory and compile them into one dataframe with an additional column for the organization name, from the filename
dfs = []
for file in directory_list:
    dfs.append(pd.read_csv(f'{DIR_NAME}/{file}').assign(deepdaoDaoId=file.replace('.csv', '')))

# combine all dataframes into one
df = pd.concat(dfs)

# make datetimes from a epoch timestamps
df['created'] = pd.to_datetime(df['created'], unit='s')
df['start'] = pd.to_datetime(df['start'], unit='s')
df['end'] = pd.to_datetime(df['end'], unit='s')
df['scores_updated'] = pd.to_datetime(df['scores_updated'], unit='s')

# index id, then order by deepdao dao ids
df = df.set_index('id')
df = df.sort_values(by=['deepdaoDaoId'])

# save as snapshot_platforms with the datetime as a prefix
df.to_csv(f'{DIR_NAME}_snapshot_dao_proposals.csv')

print(df.shape)
