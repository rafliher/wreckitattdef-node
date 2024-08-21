# blinkpdf

## Author

[wondPing](https://github.com/fixxall)

## Description

Lately, I have been studying signature algorithms. However, that's not enough, so I tried to make some modifications. Next, I attempted to implement it for signing a PDF document. You need the credentials user:user to Login.
attachment: https://drive.google.com/drive/folders/1u05M-eq50ZJjO7Ww4EHWBYeHJH6zyFCC?usp=sharing

## Tags

- DSA
- ECDSA
- LLL

## Exploit

This challenge contains two Attack Vector

1. Biased nonce attack on modified ECDSA
Just Login as user -> attack on sign phase -> get privatekey -> getting the flag.
solver: /solution/solver1.py
2. Biased nonce attack on DSA with waiting Flag (slow time)
Bypass Session. That was leak from token. Just generate Encrypted Flag with minimum dataset is 7*5 tick. The Basis use is 2**16. Cost time estimately (>= 35 minutes).
solver: /solution/solver2.py
