import ecdsa, os
import miner

if not os.path.isfile('key.txt'):
  with open("key.txt", "w") as file:
    sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
    file.write(sk.to_string().hex())

with open("key.txt", "r") as file:
  sk = ecdsa.SigningKey.from_string(bytearray.fromhex(file.read()), ecdsa.SECP256k1)

wallet_address = sk.verifying_key.to_string().hex()
private_key = sk.to_string().hex()

chain = miner.Blockchain()
chain.mine_transactions(wallet_address)
chain.mine_transactions(wallet_address)
chain.print()
print(chain.get_balance(wallet_address))
chain.add_transaction(wallet_address, '0', 50, private_key)
chain.mine_transactions(wallet_address)
chain.print()
print(chain.get_balance(wallet_address))
