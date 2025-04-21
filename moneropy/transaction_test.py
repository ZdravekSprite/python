from monero.backends.jsonrpc.daemon import JSONRPCDaemon
import json
from monero.transaction import Transaction

def get_block(block_no:int,daemon = JSONRPCDaemon()):
    block = daemon.get_block(height=block_no)
    return block

def get_block_json(block_no:int):
    return get_block(block_no)['json']

def get_transaction(tx_hash,daemon = JSONRPCDaemon()):
    return daemon.get_transactions([tx_hash],decode_as_json=True)

def get_transactions(tx_hashes,daemon = JSONRPCDaemon()):
    return daemon.get_transactions(tx_hashes,decode_as_json=True)

def parse_json(json_str:str):
    dict = json.loads(json_str)
    for key in dict.keys():
        if key == 'miner_tx':
            print('\n\tminer_tx')
            for _key in dict[key].keys():
                print(f'\t{_key}:',dict[key][_key])
        elif key == 'tx_hashes':
            for t in get_transactions(dict[key])['txs']:
                #print(t)
                print('\n\ttx_hash',t['tx_hash'])
                parse_json(t['as_json'])
        else:
            print(f'\t{key}:',dict[key])

if __name__ == '__main__':
    print(__file__)

    #tx_hash 948a7ce9971d05e99a43f35e11e4c6a346e7d2b71758bed5cb4f9fc175f7bb5f
    t = Transaction(hash='948a7ce9971d05e99a43f35e11e4c6a346e7d2b71758bed5cb4f9fc175f7bb5f')
    print(t)
    '''
    block_no = 834157
    print('\n\tblock:',block_no,'\n')

    block=get_block_json(block_no)
    parse_json(block)

    for tx in json.loads(block)['tx_hashes']:
        print('\n\ttx_hash',tx,'\n')
        for t in get_transaction(tx)['txs']:
            parse_json(t['as_json'])
    '''
