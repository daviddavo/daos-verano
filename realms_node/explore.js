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





/////


// this gets the proposals only for the realm, grouped by organization
allProposals = await getAllProposals(connection, programId, realmPubKey);
allProposalsFlat = allProposals.reduce((acc, val) => acc.concat(val), []);

console.log(allProposalsFlat.length);



















// /////////

// here we can get the vote record for each proposal in the entire program
govaccounts = await getGovernanceAccounts(connection, programId, VoteRecord, []);

// count the govaccounts by the frequency of the .account.proposal
proposalVoteCounts = govaccounts.reduce((acc, val) => acc.concat(val), []).map(x => x.account.proposal
).reduce((acc, val) => {
    acc[val] = (acc[val] || 0) + 1;
    return acc;
}, {});

// save to json
const fs = require('fs');
fs.writeFileSync('proposalVoteCounts.json', JSON.stringify(proposalVoteCounts));

// save allproposalflat to json
fs.writeFileSync('allProposalsFlat.json', JSON.stringify(allProposalsFlat));

// voteAccounts = await connection.getVoteAccounts(programId) // these are for the entire program, not this realm
// voteRecord = getVoteRecord(connection, programId);

// https://github.com/solana-labs/oyster/blob/main/packages/governance-sdk/src/governance/api.ts