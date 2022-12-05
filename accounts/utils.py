from web3 import Web3

# Funzione per mandare la transazione alla chain
def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider(
        'https://goerli.infura.io/v3/78fdbf414c944b1298a39ebe9c9188a1'))
    address = '0x9D13C3C58B2B60638986763A83B671bE616458DF'
    privateKey = '0x797c455a6804272375a86912af07cc63927e73121701b00b44495725acad3af9'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId