# Version 7 (2023-08-07)
- Update realms platform data to include all smart contracts on the platform
- This added rows to all tables

# Version 6 (2023-08-02)
- Remove `platform` from proposal (this is a deployment property, not a proposal propoerty)
- Make proposal date type a date, not a string, new schema:
```
id: string
deployment_id: string
platform_proposal_id: string
author: string
date: timestamp[s]
votes_count: int64
```
  - Note the date precision `s`
- Make vote date precision `s`, new schema:
```
id: string
proposal_id: string
deployment_id: string
platform_vote_id: string
voter: string
date: timestamp[s]
choice: string
weight: decimal128(38, 4)
```
# Version 5 (2023-07-28)
- Add Governor data to `deployments.parquet`, `proposals.parquet`, and `votes.parquet`
  - Update proposal votes count, corr:      `0.99999`
  - Update deployment votes count, corr:    `0.99999` 
  - Update deployment proposal count, corr: `0.88188`
    - (Note that this number is low because the proposals on the governor platform are
    a subset of the total number of proposals that Governor reports at a deployment level.)
  - Add corresponding UUIDs

# Version 4 (2023-07-26)

- Update proposal `votes_count` values to count from `votes.parquet`, correlation between old and new:           `0.99998`
- Update deployment `votes_count` values to count from `votes.parquet`, correlation between old and new:         `0.99868`
- Update deployment `proposals_count` values to count from `proposals.parquet`, correlation between old and new: `0.99996`
- No changes to `votes.parquet`

# Version 3 (2023-07-26)
- Add UUIDs to deployments, proposals, and votes
- Update deployment schema:
```
id: string
platform: string
platform_deployment_id: string
name: string
website: string
additional: string
votes_count: int64
proposals_count: int64
```
- Update proposal schema:
```
id: string
deployment_id: string
platform_proposal_id: string
author: string
date: string
votes_count: int64
platform: string
```
- Update vote schema:
```
id: string
proposal_id: string
deployment_id: string
platform_vote_id: string
voter: string
date: timestamp[us]
choice: string
weight: decimal128(38, 4)
```

# Version 2 (2023-07-26)

- Make vote weights `decimal128` instead of `decimal256`
- Remove duplicates in each of the three parquets
  - Removed 1167 rows from deployments
  - Removed 428 rows from proposals
  - Removed 250088 rows from votes (about 1%)


# Version 1 (2023-07-26)
- Initial upload to Kaggle