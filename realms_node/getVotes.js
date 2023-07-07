const splGovernanceModule = await import('@solana/spl-governance');
const { getRealm, getRealms, getProposalsByGovernance, getVoteRecord, getAllProposals, getVoteRecordsByVoter, getGovernanceAccounts, pubkeyFilter, VoteRecord } = splGovernanceModule;

const solanaWeb3 = await import('@solana/web3.js');
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

const realmPubKey = new PublicKey('DGnx2hbyT16bBMQFsVuHJJnnoRSucdreyG5egVJXqk8z');
const programId = new PublicKey('GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw');

const proposalPk = new PublicKey('DQaTJ4u4krRQYYq67qS7o7ujEHzk5DE1LMsm7NtZX8Fb');

votes = await getGovernanceAccounts(
    connection,
    programId,
    VoteRecord,
    [pubkeyFilter(1, proposalPk)] // filters
)

