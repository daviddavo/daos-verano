import fs from 'fs';

const splGovernanceModule = await import('@solana/spl-governance');
const solanaWeb3 = await import('@solana/web3.js');
const { getRealms } = splGovernanceModule;
const { Connection, PublicKey } = solanaWeb3;

const RPC_URL = 'http://realms-realms-c335.mainnet.rpcpool.com/258d3727-bb96-409d-abea-0b1b4c48af29/';
const connection = new Connection(RPC_URL, 'recent');

const getAllProgramProposals = async (connection, programIdString) => {
    var programId = new PublicKey(programIdString);
    // make an output directory based on the date
    const date = new Date();
    const outputDir = `output_deployments_${date.getFullYear()}_${date.getMonth()+1}_${date.getDate()}`;
    // make the output directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    // get all realms from getRealms, save as a json file
    var realms = await getRealms(connection, programId);
    console.log('REALMS', programId, realms.length);
    // save to json file in output directory
    fs.writeFileSync(`${outputDir}/${programId}_realms.json`, JSON.stringify(realms));
};

// read in lines from program_ids.txt
const programIds = fs.readFileSync('program_ids.txt', 'utf-8').split('\n');
console.log('got', programIds.length, 'program ids');

// run each
for (var i = 0; i < programIds.length; i++) {
    console.log('running', programIds[i], i)
    getAllProgramProposals(connection, programIds[i]);
}
