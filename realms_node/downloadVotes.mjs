import fs from 'fs';
const splGovernanceModule = await import('@solana/spl-governance');
const { getGovernanceAccounts, pubkeyFilter, VoteRecord } = splGovernanceModule;

const solanaWeb3 = await import('@solana/web3.js');
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

// make an output directory based on the date
const date = new Date();
const outputDir = `output_votes_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}`;
// make the output directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
}

const proposalsOutputDir = 'output_proposals_2023_8_3';
/*
open each group of proposals, get the proposal ids, and push to allProposals
allProposalIds is an array of objects with the form:
{
    pubkeyString: proposalPubKeyString,
    programString: programIdString
    realmIdString: realmIdString
}
*/

var allProposals = [];
var proposalFiles = fs.readdirSync(proposalsOutputDir);
for (let i = 0; i < proposalFiles.length; i++) {
    var proposalFile = proposalFiles[i];
    var proposalFilename = `${proposalsOutputDir}/${proposalFile}`;
    var proposalListOfLists = JSON.parse(fs.readFileSync(proposalFilename));
    for (let j = 0; j < proposalListOfLists.length; j++) {
        var proposalList = proposalListOfLists[j];
        for (let k = 0; k < proposalList.length; k++) {
            var proposal = proposalList[k];

            // break filename to get the realm id
            // form <programId>_<realmId>_proposals.json
            var filenameParts = proposalFile.split('_');
            var programId = filenameParts[0];
            var realmId = filenameParts[1];
            // assert that the programId and proposal.owner are the same
            if (programId != proposal.owner) {
                console.log('ERROR: programId != proposal.owner');
                process.exit(1);
            }

            if (proposal.account.votingCompletedAt != null) {
                allProposals.push({
                    pubkeyString: proposal.pubkey,
                    programString: proposal.owner,
                    realmIdString: realmId
                })
            }
        }
    }
}
console.log('allProposals with non null votingCompletedAt', allProposals.length);

const getVotesForProposal = async (
    connection,
    programIdAsString,
    proposalPublicKeyAsString,
    realmIdAsString,
) => {
    var proposalPk = new PublicKey(proposalPublicKeyAsString);
    var programId = new PublicKey(programIdAsString);

    var outFilename = `${outputDir}/${programId.toString()}_${realmIdAsString}_${proposalPk.toString()}_votes.json`;

    // if file already exists, skip
    if (fs.existsSync(outFilename)) {
        console.log('  skipping', proposalPk.toString());
        return;
    }

    // random timeout 1-20 seconds
    var timeout = Math.floor(Math.random() * 19_000) + 1000;
    await new Promise(resolve => setTimeout(resolve, timeout));

    // try this 5 times with an increasing timeout before giving up
    var numTries = 0;
    var timeout = 1000;
    var proposalVotes = null;
    while (numTries < 5) {
        try {
            proposalVotes = await getGovernanceAccounts(
                connection,
                programId,
                VoteRecord,
                [pubkeyFilter(1, proposalPk)] // filters
            )
            break;
        } catch (e) {
            console.log('error', e);
            numTries += 1;
            timeout *= 2;
            await new Promise(resolve => setTimeout(resolve, timeout));
        }
    }

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
    fs.writeFileSync(outFilename, JSON.stringify(proposalVotes));
    console.log('  done', proposalVotes.length, proposalPk.toString());
}

// for each proposal, get the votes
for (let i = 0; i < allProposals.length; i++) {
    var proposal = allProposals[i];
    console.log('getting votes for', i, '/', allProposals.length, proposal.pubkeyString);
    await getVotesForProposal(
        connection,
        proposal.programString,
        proposal.pubkeyString,
        proposal.realmIdString,
    );
}
