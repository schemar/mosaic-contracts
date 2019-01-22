import json


def load(contract_name):
    with open('./build/contracts/' + contract_name + '.json') as f:
        contract_file = f.read()

    contract = json.loads(contract_file)

    return bytearray(contract['bytecode'], 'utf8')
