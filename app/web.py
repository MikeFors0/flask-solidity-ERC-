from web3 import Web3
import json
from eth_account.messages import encode_defunct

config = json.load(open('HardHat/artifacts/contracts/contract.sol/Contract.json'))
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract = w3.eth.contract(address=config['address'], abi=config['abi'])

if w3.is_connected():
    print("connect")
else:
    print("disconnect")

def func(name, args=None, operation=None):
    try:
        if operation != "transact":
            if args:
                res = contract.functions[name](*args).call()
            else:
                res = contract.functions[name]().call()
        else:
            if args:
                res = contract.functions[name](*args).transact()
            else:
                res = contract.functions[name]().transact()
        return res
    except Exception as e:
        return str(e)


def key_check(key):
    try:
        message = encode_defunct(text="hello")
        signed_message =  w3.eth.account.sign_message(message, private_key=key)
        recovered_address = w3.eth.account.recover_message(message, signature=signed_message.signature.hex())
        if recovered_address in w3.eth.accounts:
            w3.eth.default_account = w3.to_checksum_address(recovered_address)
            return func("Auth")
        return "Invalid key"
    except Exception as e:
        return str(e)


def buy(amount):
    try:
        function_name = 'Buy_Profi'
        function_params = [amount]
        eth = amount * func(name="price_profi_token")

        transaction = contract.functions[function_name](*function_params).transact({
            'to':config["address"],
            'gasPrice': w3.to_wei('50', 'gwei'),
            'value': eth,
            'gas': 200000
        })
        return transaction
    except Exception as e:
        return str(e)
    
