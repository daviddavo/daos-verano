Let's get all of the votes.

## Schema

* platform
* platform_deployment_id
* proposal_id
* vote_id
* voter -- the id of the person who made the vote
* date -- this should be as a pandas date, not as an epoch
* choice -- this should be a string as this is not always true/false
* weight -- the vote weight

## Platform notes

### Aragon

Aragon has information on DAO Analyzer. We used information as of July 12, 2023.

Aragon votes are (confusingly) called "casts". We work with the `casts.csv` file.

Using `createdAt` date.


### Daohaus

Daohaus has information on DAO Analyzer. We used information as of July 12, 2023.
Using `createdAt` date


### Daostack

Daostack has information on DAO Analyzer. We used information as of July 12, 2023.
Using `createdAt` date


### Realms

Using the JS SDK, downloaded on July 12 2023.

We include [relinquished votes](https://github.com/solana-labs/solana-program-library/blob/master/governance/README.md)
TODO: remove relinquished votes from the proposals table.

We use voterWeight for the weights.

`choice` is not present for all vals.


### Tally

Using the Tally API
`timestamp` date
Collected July 18, 2023.

-------------


### **Snapshot

Downloaded from 23 June 2023 to 27 June 2023 using the window:

```
YEAR_AGO_EPOCH = 1656021600  # 2022-06-24 00:00:00
NOW_EPOCH =      1687557600  # 2023-06-24 00:00:00
```

We use `created` as the date.
