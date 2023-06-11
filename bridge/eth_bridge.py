import json
from web3 import Web3
from bridge.RPCs import *
# enter slippage as shown => 1 = 0.1%, 5 = 0.5%, 50 = 5%
SLIPPAGE = 50

# RPCs
arbitrum_rpc_url = ARB_RPC
optimism_rpc_url = OPT_RPC

arbitrum_w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))
optimism_w3 = Web3(Web3.HTTPProvider(optimism_rpc_url))

# Testnet Router
t_bridge_arbitrum_address = arbitrum_w3.to_checksum_address('0x0A9f824C05A74F577A536A8A0c673183a872Dff4')
OFT_arbitrum = arbitrum_w3.to_checksum_address('0xdD69DB25F6D620A7baD3023c5d32761D353D3De9')

t_bridge_optimism_address = optimism_w3.to_checksum_address('0x0A9f824C05A74F577A536A8A0c673183a872Dff4')
OFT_optimism = optimism_w3.to_checksum_address('0xdD69DB25F6D620A7baD3023c5d32761D353D3De9')



# ABIs
t_bridge_arbi_router_abi = json.load(open('abis/router_abi_arbi.json'))
l0_OFT_arbi_abi = json.load(open('abis/endpoint_arbi_l0.json'))

t_bridge_opti_router_abi = json.load(open('abis/router_abi_opti.json'))
l0_OFT_opti_abi = json.load(open('abis/endpoint_opti_l0.json'))

# Init contracts
t_bridge_arbitrum_router_contract = arbitrum_w3.eth.contract(address=t_bridge_arbitrum_address, abi=t_bridge_arbi_router_abi)
l0_arbitrum_router_contract = arbitrum_w3.eth.contract(address=OFT_arbitrum, abi=l0_OFT_arbi_abi)

t_bridge_opti_router_contract = optimism_w3.eth.contract(address=t_bridge_optimism_address, abi=t_bridge_opti_router_abi)
l0_opti_router_contract = optimism_w3.eth.contract(address=OFT_optimism, abi=l0_OFT_opti_abi)



def check_gas_in_eth():
    rpc_eth = ETH_RPC
    w3 = Web3(Web3.HTTPProvider(rpc_eth))

    gas = round(w3.eth.gas_price / 10 ** 9, 1)
    return gas


def get_balance_eth_arbitrum(address):
    return arbitrum_w3.eth.get_balance(address)


def get_balance_eth_optimism(address):
    return optimism_w3.eth.get_balance(address)


def bridge_arbitrum_goerli(account, amount):
    
    address = arbitrum_w3.to_checksum_address(account.address)
    nonce = arbitrum_w3.eth.get_transaction_count(address)
    gas_price = arbitrum_w3.eth.gas_price * 1.1 # some more gwei for tx than default
    fees = l0_arbitrum_router_contract.functions.estimateSendFee( 154,
                                                                  address,
                                                                  amount,
                                                                  False,
                                                                  '0x',
                                                                  ).call()
    fee = fees[0]


    # Testnetbridge tx
    chainId = 154
    refund_address = account.address
    amountIn = amount
    amountOutMin = amount - (amount * SLIPPAGE) // 1000
    to = account.address
    zroPaymentsAddress = '0x0000000000000000000000000000000000000000'
    data = '0x'

    gas = t_bridge_arbitrum_router_contract.functions.swapAndBridge(
        amountIn, amountOutMin, chainId, to, refund_address, zroPaymentsAddress, data
    ).estimate_gas({'from': address, 'value': amount + fee,  'nonce': nonce})

    gas = gas * 1.1
    txCost =  gas * gas_price
    txCostInEther = arbitrum_w3.from_wei(txCost, "ether")

    swap_txn = t_bridge_arbitrum_router_contract.functions.swapAndBridge(
        amountIn, amountOutMin, chainId, to, refund_address, zroPaymentsAddress, data
    ).build_transaction({
        'from': address,
        'value': amount + fee,
        'gas': 5000000,
        'gasPrice': int(gas_price),
        'nonce': nonce,
    })

    signed_swap_txn = arbitrum_w3.eth.account.sign_transaction(swap_txn, account.key)
    swap_txn_hash = arbitrum_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
    return swap_txn_hash


def bridge_optimism_goerli(account, amount):
    
    address = optimism_w3.to_checksum_address(account.address)
    nonce = optimism_w3.eth.get_transaction_count(address)
    gas_price = optimism_w3.eth.gas_price * 1.2 # some more gwei for tx than default
    fees = l0_opti_router_contract.functions.estimateSendFee(  154,
                                                               address,
                                                               amount,
                                                               False,
                                                               '0x',
                                                               ).call()
    fee = fees[0]


    # Testnetbridge tx
    chainId = 154
    refund_address = account.address
    amountIn = amount
    amountOutMin = amount - (amount * SLIPPAGE) // 1000
    to = account.address
    zroPaymentsAddress = '0x0000000000000000000000000000000000000000'
    data = '0x'

    gas = t_bridge_opti_router_contract.functions.swapAndBridge(
        amountIn, amountOutMin, chainId, to, refund_address, zroPaymentsAddress, data
    ).estimate_gas({'from': address, 'value': amount + fee,  'nonce': nonce})
    txCost =  gas * gas_price
    txCostInEther = arbitrum_w3.from_wei(txCost, "ether")

    swap_txn = t_bridge_opti_router_contract.functions.swapAndBridge(
        amountIn, amountOutMin, chainId, to, refund_address, zroPaymentsAddress, data
    ).build_transaction({
        'from': address,
        'value': amount + fee,
        'gas': 1000000,
        'gasPrice': int(gas_price),
        'nonce': nonce,
    })

    signed_swap_txn = optimism_w3.eth.account.sign_transaction(swap_txn, account.key)
    swap_txn_hash = optimism_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
    return swap_txn_hash