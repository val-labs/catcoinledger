# API

What are "valid" transactions or blocks?

valid blocks are either the longest chain +/- 15 minutes
  - or 30 days old
  - or any newer blocks on any chains of the old chains
  - if any transactions are older than 60 days, they can't be reclaimed
  
batching up existing transactions is valid to get you credits for mining.
  - posting one transaction costs the network
  - two transactions is probably about equal

eventually, once traffic goes up, this can be tighted to something like
a 5-15 minute window.  Or even a 15-45 second window?

## Authentication

 - Create Public/Private Key pair
 
 - Sign Message

 - Verify Message

 - Encrypt Message

 - Decrypt Message

## Network

 + Connect 
   - `network_connect()`

 + Listen to Chatter 
   - `network_listen()`

 + Disconnect
   - `network_disconnect()`

## Blocks (blk)

+ Get BlockIDs
 +  `get_block_ids()`

+ Get Block 
 + `get_block()`

+ Verify Block
 +  `verify_block()`

+ Mine Block
 +  `mine_block()`

## Transactions (xtn)

##### qwe`rt`

here's some reular text

###### sdfsdf`dfgdfg`

- List Block Transactions
 - `list_blk_xtns()`

- Create Transaction
 - `create_xtn()`

- Read Transaction
 - `read_xtn()`

- Write Transaction
 - `write_xtn()`

- Verify Transactions
 - `verify_xtn()`

- Sign Transaction
 - `sign_xtn()`

- Announce Transaction
 - `announce_xtn()`
