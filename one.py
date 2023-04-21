from pathlib import Path
from multiversx_sdk_core import Address, TokenPayment
from multiversx_sdk_network_providers import ApiNetworkProvider
from multiversx_sdk_wallet import UserSigner
from multiversx_sdk_core.transaction_builders import EGLDTransferBuilder
from multiversx_sdk_core import Transaction


provider = ApiNetworkProvider("https://api.multiversx.com")

from_wallet = Address.from_bech32("erd1uyq7m99cw2fuwewcrje4exdvem862tc7ps6n67l2j3d0y5ypp2fqyun8k3")
to_wallet = Address.from_bech32("erd1qtev8s0fh84cf8v8a9esjvxc9d7z5wlv2t52c40zap3ep53y3clqnfy4qt")
key_file_path = Path("./wallet/erd1uyq7m99cw2fuwewcrje4exdvem862tc7ps6n67l2j3d0y5ypp2fqyun8k3.json")
password = "Xenakyle1995@"

# Get the wallet balance
account_on_network = provider.get_account(from_wallet)
nonce = account_on_network.nonce
balance = account_on_network.balance

print("Nonce:", nonce)
print("Balance:", balance)

# Get the gas price
config = provider.get_network_config()
chain_id = config.chain_id
gas = config.min_gas_price
config.gas_limit_per_byte=2

print("Chain ID:", chain_id)
print("Min gas price:", gas)

totalGas=(config.gas_limit_per_byte*gas)
sendBalance=(balance-totalGas)

print("totalGas", totalGas)
print("Available balance",sendBalance)


# Define the transaction information
send = (from_wallet)
to = (to_wallet)
payment = TokenPayment.egld_from_amount(sendBalance)

if (sendBalance>0):

    builder = EGLDTransferBuilder(

    config=config,
    sender=send,
    receiver=to,
    payment=payment,
    data="",
    nonce=nonce
    )

    tx = builder.build()

    from multiversx_sdk_wallet import UserSigner

    signer = UserSigner.from_wallet(Path(key_file_path),password)
    tx.signature = signer.sign(tx)


    print("Transaction:", tx.to_dictionary())
    print("Transaction data:", tx.data)
    print("Signature:", tx.signature.hex())

    hash = provider.send_transaction(tx)
    print("Transaction hash:", hash)
else:
    print("Low  balance.....")