from manticore.ethereum import ManticoreEVM


# Feedback from @Disconnect3d on the manticore slack (empirehacking.slack.com):
# My original question:
# I tried setting the working directory to the contracts directory of truffle, but that did not help, unfortunately. Which working directory should I set?
#
# His reply:
# @Martin The `contracts` directory
# There is also a catch here

# If you invoke:
# ```m.solidity_create_contract(source, working_dir=full_contracts_dir_path, ....)```
# Then Manticore will copy the source to a temp directory and won't really copy other files from working dir and so the import won't work (edited)
# This has to be done instead:
# ```with open(contract_path) as f:
#     m.solidity_create_contract(f, working_dir=full_contracts_dir_path, ...)```
# here, `solidity_create_contract` will take the contract path and working dir, and create a `relative_path` which will be passed to `solc` compilation and `working_dir` which will be passed to `Popen` so `solc` will be executed the same way as if you would have been in working_dir and passing relative contract path to it
# See https://github.com/trailofbits/manticore/blob/master/manticore/ethereum/manticore.py#L242-L262

with open('./build/flattened/Anchor.sol') as f:
    anchor_source_code = f.read()
with open('./build/flattened/Organization.sol') as f:
    organization_source_code = f.read()


m = ManticoreEVM()

user_account = m.create_account(balance=1000)

organization_contract = m.solidity_create_contract(
    organization_source_code,
    owner=user_account,
    contract_name='Organization',
    args=[user_account, user_account, [], 0],
)

anchor_contract = m.solidity_create_contract(
    anchor_source_code,
    owner=user_account,
    contract_name='Anchor',
    args=[
        1,
        0,
        bytearray(b'\x01' * 32),
        100,
        organization_contract.address,
    ],
)


anchor_contract.anchorStateRoot(1, bytearray(b'\x11' * 32))


# print(f"[+] There are {m.count_terminated_states()} reverted states now")
# print(f"[+] There are {m.count_running_states()} alive states now")

# print(f"[+] Global coverage: {anchor_contract.address:x}")
# print(m.global_coverage(anchor_contract))

m.finalize()
