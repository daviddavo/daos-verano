we use the solana sdk, in js, to help scrape

once we have proposals, we clean them up into a csv in python and also save the proposal ids to a json for step two

in step two we take the cleaned proposal ids list and fetch all of the vote data

lastly, we shape the vote data into the desired csv format again in python.