import os
import pandas as pd

DIR_NAME = '1687365380'
ignore_files = ['deep_dao_organizations.csv']

directory_list = os.listdir(DIR_NAME)
directory_list = [x for x in directory_list if x not in ignore_files and x.endswith('.json')]
print(len(directory_list), 'directories found')

# read all csv files in the directory and compile them into one dataframe with an additional column for the organization name, from the filename
dfs = []
for file in directory_list:
    dfs.append(pd.read_json(f'{DIR_NAME}/{file}').assign(organizationId=file[:-5]))

# combine all dataframes into one
df = pd.concat(dfs)

# break the data column into separate columns
df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)

# sort by by organizationId and daoId
df = df.sort_values(by=['organizationId', 'daoId'])

# rename platform to platformId
df = df.rename(columns={'platform': 'platformId'})

# drop logo
df = df.drop(columns=['logo'])

# reorder columns
df = df[['name', 'platformTitle', 'platformId', 'website',
       'mostRecentProposalDate', 'aum']]

# save to csv based on the directory name
df.to_csv(f'{DIR_NAME}_deepdao_platforms.csv')

print(df.shape)
