from web3 import Web3
import config


PAYMENT_CONTRACT = "0xf0d643F0D5AA17e2764A9C1d4CaF3668f7165886"
TTN_CONTRACT = Web3.toChecksumAddress("0x722b7d4b9c830199F043eA210125fA13a91c64EF")

web3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/bsc_testnet_chapel")) # Creating Web3 Object
contract = web3.eth.contract(address=web3.toChecksumAddress(PAYMENT_CONTRACT), abi=config.PAYMENT_CONTRACT_ABI) # Creating Web3 Object
chain_id = web3.eth.chain_id

# if web3.eth.chain_id == 2000: tx_data['gas_price'] = 260000000000

build_tx = {
    'chainId': chain_id,

    'gasPrice': web3.eth.gas_price,
    'from': web3.toChecksumAddress("0xd302f9AA2a57eA2516835A6e36CC168ae0365B37")
} # Constructing TX Object

try:
    token_contract = web3.eth.contract(address=web3.toChecksumAddress(TTN_CONTRACT), abi=config.TTN_CONTRACT_ABI)
    # token_decimal = token_contract.functions.decimals().call()

    allowance = token_contract.functions.allowance(
        web3.toChecksumAddress("0xd302f9AA2a57eA2516835A6e36CC168ae0365B37"),
        web3.toChecksumAddress(PAYMENT_CONTRACT)
    ).call()
    
    print(allowance)
    
    if int(10 * 10 ** 9) > allowance:
        try:
            tx = token_contract.functions.increaseAllowance(web3.toChecksumAddress(PAYMENT_CONTRACT), 115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction(
                {
                    'chainId': chain_id,
                    # 'value': int(10 * 10 ** 9),
                    'gasPrice': web3.eth.gas_price,
                    'from': web3.toChecksumAddress("0xd302f9AA2a57eA2516835A6e36CC168ae0365B37")
                }
            )
        
            tx['gas'] = web3.eth.estimate_gas(tx)
            tx['nonce'] = web3.eth.get_transaction_count(web3.toChecksumAddress("0xd302f9AA2a57eA2516835A6e36CC168ae0365B37"))
            signed_tx = web3.eth.account.sign_transaction(tx, "775f08f93da3b54168891bab5e52ad737c0d64e4ad015c0e57cba8e6492f5e16")
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            web3.eth.wait_for_transaction_receipt(web3.toHex(tx_hash), timeout=10)
        except Exception as error:
            print(False, f"Error While Approving Token: {error}")


    tx = contract.functions.acceptPaymentTTN(
        web3.toChecksumAddress("0xFc6a14b99E9DB129A764877d98fB32446559ED81"),
        10000000000,
        "ORDER_TEST"
    ).buildTransaction(build_tx)

    tx['gas'] = web3.eth.estimate_gas(tx)
    tx['nonce'] = web3.eth.get_transaction_count(web3.toChecksumAddress("0xAad6a88877E6AB7FbC33fdAce672780A85Fc88a8"))

    signed_tx = web3.eth.account.sign_transaction(tx, "775f08f93da3b54168891bab5e52ad737c0d64e4ad015c0e57cba8e6492f5e16")
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(True, web3.toHex(tx_hash))
except Exception as error:
    print(False, str(error), "END")
