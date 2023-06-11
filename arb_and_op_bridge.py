import time
from termcolor import cprint
from web3 import  Web3
from bridge.eth_bridge import bridge_arbitrum_goerli, get_balance_eth_arbitrum, get_balance_eth_optimism, bridge_optimism_goerli
from settings import *



def arbitrum(account, value_transfer):
    balance = get_balance_eth_arbitrum(account.address)

    if balance < Web3.to_wei(0.002, 'ether'):
        cprint("Not enough balance", 'red')
        return
    try:
        cprint("Bridging ETH from Arbitrum to Goerli...", 'yellow')
        arbitrum_to_goerli_txs_hash = bridge_arbitrum_goerli(account=account, amount=Web3.to_wei(value_transfer, 'ether'))
        print("Waiting for the bridge to complete...")
        time.sleep(15)
        cprint(f"Transaction: https://arbiscan.io/tx/{arbitrum_to_goerli_txs_hash.hex()}", 'green')
    except Exception as err:
        cprint(err, 'red')
    

def optimism(account, value_transfer):
    balance = get_balance_eth_optimism(account.address)

    if balance < Web3.to_wei(0.002, 'ether'):
        cprint("Not enough balance", 'red')
        return
    try:
        cprint("Bridging ETH from Optimism to Goerli...", 'yellow')
        optimism_to_goerli_txs_hash = bridge_optimism_goerli(account=account, amount=Web3.to_wei(value_transfer, 'ether'))
        print("Waiting for the bridge to complete...")
        time.sleep(15)
        cprint(f"Transaction: https://optimistic.etherscan.io//tx/{optimism_to_goerli_txs_hash.hex()}", 'green')
    except Exception as err:
        cprint(err, 'red')
