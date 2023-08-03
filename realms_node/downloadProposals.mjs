const splGovernanceModule = await import('@solana/spl-governance');
import fs from 'fs';
const { getAllProposals } = splGovernanceModule;

const solanaWeb3 = await import('@solana/web3.js');
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

// make an output directory based on the date
const date = new Date();
const outputDir = `output_proposals_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}`;
// make the output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

const getProposalsForRealm = async (
    connection,
    programIdAsString,
    realmPublicKeyAsString
) => {
    var programId = new PublicKey(programIdAsString);
    var realmPubKey = new PublicKey(realmPublicKeyAsString);

    var filename = `${outputDir}/${programId}_${realmPubKey}_proposals.json`;
    // if file already exists, skip
    if (fs.existsSync(filename)) {
    // console.log('PROPOSALS...', programId.toString(), realmPubKey.toString());
        console.log('  skipping', programId.toString(), realmPubKey.toString());
        return;
    }
    // try this 5 times with an increasing timeout before giving up
    var numTries = 0;
    var timeout = 1000;
    var realmProposals = null;
    while (numTries < 5) {
        try {
            realmProposals = await getAllProposals(
                connection,
                programId,
                realmPubKey
            )
            break;
        } catch (e) {
            console.log('error', e);
            numTries += 1;
            timeout *= 2;
            await new Promise(resolve => setTimeout(resolve, timeout));
        }
    }

    // set proposal.account.votingCompletedAt to a date string
    // instead of a BigNumber
    realmProposals.forEach(solanaGovernance => {
        solanaGovernance.forEach(proposal => {
            if (proposal.account.votingCompletedAt) {
                var completedAtNumber = proposal.account.votingCompletedAt.toNumber();
                proposal.account.votingCompletedAt = completedAtNumber;
            }
        });
    });

    // write to file
    fs.writeFileSync(filename, JSON.stringify(realmProposals));


    console.log('  finished', programId.toString(), realmPubKey.toString());
}


// 1. get all of the program ids from program_ids.txt
const programIds = fs.readFileSync('program_ids.txt', 'utf-8').split('\n');

// 2. get all of the realms for each program id from the output dir
const allRealms = [];
const deployments_output_dir = 'output_deployments_2023_8_3';
for (let i = 0; i < programIds.length; i++) {
    var programId = programIds[i];
    var filename = `${deployments_output_dir}/${programId}_realms.json`;
    var programRealms = JSON.parse(fs.readFileSync(filename, 'utf-8'));
    // append to realms
    allRealms.push(...programRealms);
}
console.log('got', allRealms.length, 'realms in total');

// 3. get all of the proposals for each realm async
for (let i = 0; i < allRealms.length; i++) {
    var realm = allRealms[i];
    var programId = realm.owner;
    var realmPubKeyString = realm.pubkey;
    console.log('running', programId, realmPubKeyString, i);
    await getProposalsForRealm(
        connection,
        programId,
        realmPubKeyString
    );
}
