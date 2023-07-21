TOTAL_VOTES = 2765849
MASSIVE_PROPOSAL_ID = '0xda4f201a37ea08cf1892418e7b9e88f5687a68dbdc96c3ab22abaa1c7244648e'

# glob get files in large_proposal_votes_2023_07_21
import glob
all_files = glob.glob(f"large_proposal_votes_2023_07_21/{MASSIVE_PROPOSAL_ID}/*.json")

print(len(all_files), 'files downloaded /', len(all_files) * 1000, 'votes downloaded')
print('total votes', TOTAL_VOTES)
print('percent downloaded', len(all_files) * 1000 / TOTAL_VOTES * 100, '%')
