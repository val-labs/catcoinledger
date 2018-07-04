Architecture
==============

Component Parts
---------------

1) Data Store / Verifier
  a. Consists of passive data store
  b. Indexed by blockid and block number
  c. store/forward model.
2) Pub/Sub Network
  a. Runs locally
  b. Is the plumbing to the larger peer2peer network
  c. Once Data Store positively verifies blocks, punts here.
  
Current Implementation
----------------------

1) Data Store = The file system.
  a. Probably not scalable for long term
  b. . . . But it'll get us by for now.
  c. "search" consists of GETs
    i. blockid is one way to search
    ii. a search for block numbers >> list of block ids
    iii. you can also just search for the "last" block.
    iv. asking for the last block also uses the verifier to resolve any ambiguity if there are multiple chains of hte same length to choose from.
  d. writing consist of PUTs
2) Verifier
  a. Uses the datastore directly.
  b. asking for the last block
    i. also uses the verifier to resolve any ambiguity
    ii. needed if multiple chains are the same length
  c. Could just be a freeloader.  Might just accept it anyway.
  d. May put up some cans of food for processing the transaction.
    i. verifier makes sure these can of food are "real".
    ii. when you can some food, you sign it
      a. slap the public part of the sig on it
      b. keep the private part to yourself.
      c. you sign the "spend" part of the transaction
      d. anyone can grab the entire transaction and include it
      e. but if anything changes, the signature won't match.
3) Pub/Sub network
  a. let's just use peer2peer from PyPi for now
  b. `pip install peer2peer` will install
4) Combining transactions
  a. Individual transactions are actually single record blocks.
  b. Probably has super-low difficulty.
  c. Meant to be "stolen" and processed.
  d. If no one "picks up" your can of food
    i. After 5 minutes, you get the food back.
    ii. Of course, your transaction may not go through.
  e. If someone grabs your food
    i. your block's ignored
    ii. but the transaction gets rolled into a new block
    iii. whomever mints the new block gets the food
    iv. it's possible THAT block will get overwritten too
    v. in that case, your transaction may not go through.
    vi. Retry if no one processes your transaction after 5 minutes
