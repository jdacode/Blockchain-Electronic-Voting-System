# Blockchain E-Voting System
*`[1][2]`*
<p align="center">
  <img src="/static/github/octocat.png" alt="octocat" width="150" height="150"/>
  <img src="/static/github/python.png" alt="python" width="150" height="150"/>
</p>

<br><br>
## Demo 

![demo](/static/github/demo.gif)
<br><br>
## Overview

Blockchain voting system was designed as a didactic software to learn about Blockchain and its properties, some of the features used in this project was:

- **Python**.
- **Blockchain**.
- **Cryptography**.
- **PyCrypto [pycryptodome]**.
- **Cryptographic hash SHA256**.
- **Asymmetric Private-Public-key encryption algorithm RSA**.
- **Asymmetric digital signatures RSASSA-PKCS1-v1_5**.

<br><br>
## BLOCKCHAIN *`[3]`* 

<br>

## Blockchain fundamentals:

<br>

Blockchain is a shared, immutable ledger that facilitates the process of recording transactions and tracking assets in a business network. 

An asset can be:
- Tangible (a house, a car, cash, land)
- Intangible (intellectual property, patents, copyrights, branding). 

Virtually anything of value can be tracked and traded on a blockchain network, reducing risk and cutting costs for all involved.

<br><br>

## Structure *`[4]`* 
<br>
A blockchain is a decentralized, distributed, and oftentimes public, digital ledger consisting of records called blocks that is used to record transactions across many computers so that any involved block cannot be altered retroactively, without the alteration of all subsequent blocks. This allows the participants to verify and audit transactions independently and relatively inexpensively. 

.

- It confirms that each unit of value was transferred only once, solving the long-standing problem of double spending.

- A blockchain has been described as a value-exchange protocol. 

- A blockchain can maintain title rights because, when properly set up to detail the exchange agreement, it provides a record that compels offer and acceptance. 


![blockchain3](/static/img/blockchain3.png)
<br><br>

## Blocks

Blocks hold batches of valid transactions that are hashed and encoded into a Merkle tree. Each block includes the cryptographic hash of the prior block in the blockchain, linking the two. The linked blocks form a chain. This iterative process confirms the integrity of the previous block, all the way back to the original genesis block.

![blockchain1](/static/img/blockchain1.png)
<br><br>


## Privacy and blockchain *`[5]`* 

A blockchain is a shared database that records transactions between two parties in an immutable ledger. Blockchains document and confirm pseudonymous ownership of all existing coins within a cryptocurrency ecosystem at any given time through cryptography.

> After a transaction is validated and cryptographically verified by other participants or nodes in the network, it is made into a "block" on the blockchain. 

A block contains information about the time the transaction occurred, previous transactions, and details about the transaction. Once recorded as a block, transactions are ordered chronologically and cannot be altered


![bcsecurity2](/static/img/bcsecurity2.png)
<br><br>


## Private and public keys


- A key aspect of privacy in blockchains is the use of private and public keys. Blockchain systems use asymmetric cryptography to secure transactions between users. In these systems, each user has a public and private key. 

- These keys are random strings of numbers and are cryptographically related. It is mathematically impossible for a user to guess another user's private key from their public key. This provides an increase in security and protects from hackers. 

> Public keys can be shared with other users in the network because they give away no personal data. Each user has an address that is derived from the public key using a hash function. 

- These addresses are used to send and receive assets on the blockchain, such as cryptocurrency. Because blockchain networks are shared to all participants, users can view past transactions and activity that has occurred on the blockchain.

- Senders and receivers of past transactions are represented and signified by their addresses; users' identities are not revealed. Public addresses do not reveal personal information or identification; rather, they act as pseudonymous identities. 

> It is suggested that users do not use a public address more than once; this tactic avoids the possibility of a malicious user tracing a particular address' past transactions in an attempt to reveal information. Private keys are used to protect user identity and security through digital signatures. 

- Private keys are used to access funds and personal wallets on the blockchain; they add a layer of identity authentication. 

```When individuals wish to send money to other users, they must provide a digital signature that is produced when provided with the private key. This process protects against theft of funds.```


![bcsecurity1](/static/img/bcsecurity1.png)
<br>


## PyCrypto *`[6]`* 

### Random number generation

Here is the current list of known random number generation issues/bugs that have been found in previous versions of PyCrypto:

  -  ```In versions prior to v2.6.1, Crypto.Random was insecure when using fork() in some cases. See the advisory for CVE-2013-1445 for more information. It is recommended that users upgrade to PyCrypto v2.6.1 or later.```
    
   - ```In versions prior to v2.1.0, Crypto.Util.randpool.RandomPool was unsafe as commonly used. It was not thread-safe or fork-safe at all, and it was not always properly seeded with entropy. This was by design, but most application developers simply read from it without any further thought, resulting in insecure applications. See this thread for more information. It is now is deprecated, and will be removed in a future release; Use Crypto.Random or os.urandom instead.```

> Keeping an entropy pool in a user-space program is complex and error-prone. It is especially difficult to do reliably in a generic crypto library, and it is quite common for mistakes to be made. Hopefully, operating systems will one day provide random number generation facilities that are sufficiently fast, trustworthy, and reliable that they can completely replace the multitude of user-space random number generators that currently plague our software.


<br><br>

| PyCrypto Package                                   | Module       | Description       |
|--------------------------------------------|--------------------------|--------------------------|
| **Crypto.Hash** | Module SHA256 | - SHA-256 cryptographic hash algorithm. <br> - SHA-256 belongs to the SHA-2 family of cryptographic hashes. It produces the 256 bit digest of a message. |
| **Crypto.PublicKey** | Module RSA | -RSA public-key cryptography algorithm (signature and encryption). <br> - RSA is the most widespread and used public key algorithm. |
| **Crypto.Signature** | Module PKCS1_v1_5 | -RSA digital signature protocol according to PKCS#1 v1.5 <br> -This scheme is more properly called RSASSA-PKCS1-v1_5. |

<br>

> **Note**: When using RSA encrypt with PKCS1_AOEP padding, DeprecationWarnings are thrown. Prerequisites: an RSA private key in mykey.pem


> **Note**: PyCrypto library has been deprecated and one shouldswitch to pycryptodome for an API-compatible, updated lib, or to cryptographyio for a more modern API.

<br><br>
## Screenshots

![screenshot1](/static/github/Screenshot_1.png)
![screenshot2](/static/github/Screenshot_2.png)
![screenshot3](/static/github/Screenshot_3.png)
![screenshot4](/static/github/Screenshot_4.png)
<br><br>
## References

[1] <https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/200px-Python-logo-notext.svg.png>

[2] <https://octodex.github.com/repo/>

[3] <https://www.ibm.com/blockchain/what-is-blockchain>

[4] <https://en.wikipedia.org/wiki/Blockchain>

[5] <https://en.wikipedia.org/wiki/Privacy_and_blockchain>

[6] <https://www.dlitz.net/software/pycrypto/>

<br><br>

## License

> Licensed under the [MIT](license) license.
