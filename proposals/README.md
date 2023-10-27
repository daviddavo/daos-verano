## Schema

* platform
* platform_deployment_id
* proposal_id
* author
* date -- this should be as a pandas date, not as an epoch
* votes_count
* title
* description

## Platform notes

### Aragon

Aragon has information on DAO Analyzer. Updates July 20, 2023.

Aragon proposals are (confusingly) called "votes". We work with the `votes.csv` file.

The date we use is `startDate`.

### Snapshot

Downloaded from 23 June 2023 to 27 June 2023 using the window:

```
YEAR_AGO_EPOCH = 1656021600  # 2022-06-24 00:00:00
NOW_EPOCH =      1687557600  # 2023-06-24 00:00:00
```

We use `created` as the date.

### Daohaus

Daohaus has information on DAO Analyzer. Updates July 20, 2023.
`createdAt` date

### *Daostack

Daostack has information on DAO Analyzer. Updates July 20, 2023.

### Realms

Using the JS SDK, see specific notes.

### Tally

Using the Tally API
`timestamp` date