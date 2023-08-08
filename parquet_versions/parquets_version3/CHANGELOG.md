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