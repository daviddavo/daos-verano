## Process
1. run `downloadProposals.mjs` in the `realms_node` dir - this downloads the proposals from the solana SDK in js
2. run the `get_realms_proposals` notebook - this formats the downloaded data into a csv with all of the columns **except** `votes_count`.
3. run `downloadVotes.mjs` in the `realms_node` dir - this downloads the votes from the solana SDK in js
4. run the `get_realms_proposals_votes_count` notebook - this adds the votes information to the previously generated table

This is complicated because (1) the best way to download the solana data is on JS and (2) because the Solana proposals data does not automatically include a count of the votes.
