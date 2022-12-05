from web3 import Web3

# Crea un wallet
w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/78fdbf414c944b1298a39ebe9c9188a1'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address: {address}\nYour key: {privateKey}")