Each type creates an output file w columns:

* `platform`
* `platform_id`
* `name` (may be nan)
* `website` (may be nan)
* `additional` (may contain website, social, etc. info, may be nan)
* `votes_count` (the number of unique votes in the deployment)
  - snapshot reports the sum of the votes in the deployment
  - tally reports the number of deployment token-holders who have ever voted
* `proposals_count` (the number of proposals in the deployment)

Types include:

* [Tally](https://www.tally.xyz/)
* [Realms](https://realms.today/)
* [Snapshot](https://snapshot.org/#/)
* Aragon (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))
* DAO Stack (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))
* DAO Haus (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))

TODO: explore viability of aave, uniswap and compound finance

Limitations:

- only can download up to 15k deployments from Snapshot, though we pull the "most important" ones based on Snapshot's internal ranking

DeepDAO platforms (by count, descending):

- Snapshot (n=2404, included)
- Aragon (n=84, included)
- **Governor (n=62, NOT included: does not appear to have an API)**
- Moloch / Daohaus (n=36, included)
- AssetsOnly (n=30, NOT included: cannot find online)
- **Substrate (n=27, NOT included, has a [directory](https://substrate.io/ecosystem/projects/) but no API access, TODO: try w subgraph)**
- Realms (n=18, included)
- DAOstack (n=12, included)
- **OpenLaw (n=3, NOT included, n<10)**
- **Colony (n=2, NOT included, n<10)**

Messari platforms:
- Tally
- Snapshot
- **Aave - on chain voting platform for one organization**
  - not clear if they have a way to pull proposals, etc?
- **Uniswap - on chain voting platform for one organization**
  - [governance portal](https://app.uniswap.org/#/vote)
  - maybe we can get this info via the subgraph?
- **Compound Finance - on chain voting platform for one organization**

Note that the Messari data is much messier and includes forum discussions, Notion pages, etc.
