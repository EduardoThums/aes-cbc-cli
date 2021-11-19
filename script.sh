#!/bin/bash

KEY_PAIR_NAME="eduardo"
FILE="/home/eduardothums/Downloads/file.txt"

echo "Generating key pair"
openssl genrsa -out $KEY_PAIR_NAME.pr 2048 2>/dev/null

echo "Extracting the public key from the private key"
openssl rsa -in $KEY_PAIR_NAME.pr -pubout -out $KEY_PAIR_NAME.pu 2>/dev/null


openssl rand -rand /dev/urandom 128 > K.txt
hexdump -n 16 -e '4/4 "%08X"' /dev/random > V.txt

echo "Encrypting the file"
openssl enc -nosalt -aes-256-cbc -in $FILE -out Y.txt -k K.txt -iv $(cat V.txt) -iter 1

echo "Encrypt pseudo random symmetric key and IV"
openssl rsautl -in K.txt -out EK.txt -inkey "eduardo.pu" -pubin -encrypt
openssl rsautl -in V.txt -out EV.txt -inkey "eduardo.pu" -pubin -encrypt
