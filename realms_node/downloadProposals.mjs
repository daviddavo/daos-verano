const splGovernanceModule = await import('@solana/spl-governance');
import fs from 'fs';
const { getRealms, getAllProposals, getGovernanceAccounts, pubkeyFilter, VoteRecord } = splGovernanceModule;

const solanaWeb3 = await import('@solana/web3.js');
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

const programId = new PublicKey('GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw');

// make an output directory based on the date
const date = new Date();
const outputDir = `output_${date.getFullYear()}_${date.getMonth()}_${date.getDate()}`;
// make the output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

// get all realms from getRealms, save as a json file
var realms = await getRealms(connection, programId); // n=2162
console.log('REALMS', realms.length);
// save to json file in output directory
fs.writeFileSync(`${outputDir}/realms.json`, JSON.stringify(realms));

// get all the proposals for each realm
console.log('PROPOSALS...')
for (let i = 0; i < realms.length; i++) {
    var realm = realms[i];
    // if file already exists, skip
    if (fs.existsSync(`${outputDir}/realm_proposals_${realm.pubkey}.json`)) {
        console.log('skipping', i, 'of', realms.length, 'already exists');
        continue;
    }
    var realmPubKey = new PublicKey(realm.pubkey);
    var realmProposals = await getAllProposals(
        connection,
        programId,
        realmPubKey
    )

    // set proposal.account.votingCompletedAt to a date string instead of a BigNumber
    realmProposals.forEach(solanaGovernance => {
        // console.log(solanaGovernance)
        solanaGovernance.forEach(proposal => {
            if (proposal.account.votingCompletedAt) {
                proposal.account.votingCompletedAt = proposal.account.votingCompletedAt.toNumber();
            }
        });
    });

    fs.writeFileSync(`${outputDir}/realm_proposals_${realmPubKey.toString()}.json`, JSON.stringify(realmProposals));
    console.log('finished', i, 'of', realms.length);
    // random sleep to avoid rate limiting between 1 and 1.2 seconds
    var timeout = Math.floor(Math.random() * 1000) + 200;
    await new Promise(resolve => setTimeout(resolve, timeout));
}
