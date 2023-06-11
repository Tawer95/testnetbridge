import time
from termcolor import cprint
import random
from tqdm import tqdm
from web3 import Account
from bridge.eth_bridge import check_gas_in_eth
from arb_and_op_bridge import arbitrum, optimism
from settings import *



def main(tr):
    with open('keys.txt', 'r') as keys_file:
        accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
        
        # count = what a cycle now
        count = 0
        for _ in range(0, tr):

            count += 1
            cprint(f'\n=============== start :  {count} round ===============', 'white')

            # number = what a wallet now
            number = 0
            for account in accounts:
                while True:
                    gas = check_gas_in_eth()
                    # check gas before transation
                    if gas > MAX_GAS:
                        print(f'Gas over {MAX_GAS}. Now = {gas}', end='\r')
                        time.sleep(1)
                    else:
                        break
                
                value_transfer = round(random.uniform(AMOUNT_MIN, AMOUNT_MAX), 6)

                wait_time_beetwen_wallets = round(random.uniform(MIN_WAIT, MAX_WAIT))
                number += 1
                cprint(f'\n=============== start {number} wallet : {account.address}  ===============', 'white')
                
                if ARBITRUM_DO == 'YES':

                    arbitrum(account, value_transfer)
                    for _ in tqdm(range(wait_time_beetwen_wallets), desc='Sleeping for the next account ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
                        time.sleep(1)

                if OPTIMISM_DO == 'YES':

                    optimism(account, value_transfer)
                    for _ in tqdm(range(wait_time_beetwen_wallets), desc='Sleeping for the next account ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
                        time.sleep(1)

            print(f"Sleeping {WAIT_BETWEEN_CYCLES} seconds for the next cycle")
            time.sleep(WAIT_BETWEEN_CYCLES)


if __name__ == '__main__':
    
    cprint(f'\n============================================= Crypto-Selkie ===================================================', 'cyan')
    cprint(f'\n ------------------------------------- subscribe : https://t.me/tawer_crypt -----------------------------------', 'yellow')

    main(TOTAL_ROUNDS)
    
    cprint(f'\n ------------------------------------- subscribe : https://t.me/tawer_crypt -----------------------------------', 'yellow')
    cprint(f'\n================================================== DONE =======================================================', 'green')