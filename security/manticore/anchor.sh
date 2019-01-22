#!/bin/bash

# We have to flatten the contract in order to compile it with manticore.
mkdir -p ./build/flattened
./node_modules/.bin/truffle-flattener ./contracts/gateway/Anchor.sol > ./build/flattened/Anchor.sol
./node_modules/.bin/truffle-flattener ./contracts/lib/Organization.sol > ./build/flattened/Organization.sol

# Run manticore inside a docker container.
# Use  mount to bind-mount the host directory that contains the smart contracts.
# That way, manticore inside the container has access to the smart contracts and
# ABI.
# ulimit as per recommendation from trail of bits.
# `:master` tag to enable solidity 0.5.0 support.
docker run --rm -it \
--mount type=bind,source="$(pwd)",target=/home/manticore/manticore/mosaic-contracts \
--ulimit stack=100000000:100000000 \
trailofbits/manticore:master \
/bin/sh -c 'cd /home/manticore/manticore/mosaic-contracts; python3 security/manticore/anchor.py'

# Clean up the results directory.
# rm -r mcore*
