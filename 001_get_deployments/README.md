Each type creates an output file w columns:

* `platform`
* `platform_id`
* `name` (may be nan)
* `website` (may be nan)
* `additional` (may contain website, social, etc. info, may be nan)

Types include:

* [Tally](https://www.tally.xyz/)
* [Realms](https://realms.today/)
* Snapshot
* Aragon (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))
* DAO Stack (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))

todo:
* DAO Haus (via [DAO Analyzer](https://www.kaggle.com/datasets/daviddavo/dao-analyzer?resource=download))


Limitations:

- only can download up to 15k deployments from Snapshot


DeepDAO platforms:

- Snapshot (n=2404, included)
- Aragon (n=84, included)
- Governor (n=62, NOT included: does not appear to have an API)
- Moloch / Daohaus (n=36, included)
- AssetsOnly (n=30, NOT included: cannot find online)
- Substrate (n=27, NOT included, has a [directory](https://substrate.io/ecosystem/projects/) but no API access, TODO: try w subgraph)
- Realms (n=18, included)
- DAOstack (n=12, included)
- OpenLaw (n=3, NOT included)
- Colony (n=2, NOT included)

Messari platforms:
- Aave - on chain voting platform for one organization
- Uniswap - on chain voting platform for one organization
- Compound Finance - on chain voting platform for one organization
- Tally
- Snapshot
