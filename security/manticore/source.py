import subprocess


def read_contract(path):
    result = subprocess.run(
        ['./node_modules/.bin/truffle-flattener', path],
        stdout=subprocess.PIPE,
    )

    return result.stdout.decode('utf-8')
