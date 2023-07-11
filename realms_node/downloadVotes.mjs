const splGovernanceModule = await import('@solana/spl-governance');
import fs from 'fs';
const { getGovernanceAccounts, pubkeyFilter, VoteRecord } = splGovernanceModule;

const solanaWeb3 = await import('@solana/web3.js');
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

const programId = new PublicKey('GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw');

var proposalIds = JSON.parse(fs.readFileSync('../002_get_proposals/realms/proposal_ids.json', 'utf8'));

// make an output directory based on the date
const date = new Date();
const outputDir = `output_votes_${date.getFullYear()}_${date.getMonth()}_${date.getDate()}`;
// make the output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

// get all votes, save to json files
console.log('PROPOSALS', proposalIds.length);

console.log('VOTES...')
for (let i = 0; i < proposalIds.length; i++) {
    var proposalPk = new PublicKey(proposalIds[i]);
    // if file already exists, skip
    if (fs.existsSync(`${outputDir}/proposal_votes_${proposalPk.toString()}.json`)) {
        console.log('skipping', i, 'of', proposalIds.length, 'already exists');
        continue;
    }
    var proposalVotes = await getGovernanceAccounts(
        connection,
        programId,
        VoteRecord,
        [pubkeyFilter(1, proposalPk)] // filters
    )

    // for vote in proposalVotes, set voterWeight to a number instead of a BigNumber
    proposalVotes.forEach(vote => {
        // if the voterWeight key is present
        if (vote.account.voterWeight) {
            vote.account.voterWeight = vote.account.voterWeight.toString();
            // continue to next
            return;
        }
        // if the voteWeight key is present
        if (vote.account.voteWeight) {
            // this is another type of vote, with key voteWeight instead of voterWeight
            // if voteWeight is an object, set the values of every key to a number instead of a BigNumber
            Object.keys(vote.account.voteWeight).forEach(key => {
                // if not undefined
                if (vote.account.voteWeight[key]) {
                    vote.account.voteWeight[key] = vote.account.voteWeight[key].toString();
                }
            })
            return;
        }
        console.log('voterWeight or voteWeight not found in vote', vote)
        throw new Error('voterWeight or voteWeight not found in vote');
    });

    // write to file
    fs.writeFileSync(`${outputDir}/proposal_votes_${proposalPk.toString()}.json`, JSON.stringify(proposalVotes));
    console.log('wrote', i, 'of', proposalIds.length);

    // random sleep to avoid rate limiting between 1 and 1.2 seconds
    var timeout = Math.floor(Math.random() * 1000) + 200;
    await new Promise(resolve => setTimeout(resolve, timeout));
}