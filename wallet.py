import ecdsa, os
import miner
from time import sleep

if not os.path.isfile('key.txt'):
  with open("key.txt", "w") as file:
    sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
    file.write(sk.to_string().hex())

with open("key.txt", "r") as file:
  sk = ecdsa.SigningKey.from_string(bytearray.fromhex(file.read()), ecdsa.SECP256k1)

wallet_address = sk.verifying_key.to_string().hex()
private_key = sk.to_string().hex()

chain = miner.Blockchain()

# https://www.geeksforgeeks.org/clear-screen-python/
def clear():
  
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
  

def menu():
  while True:
    clear()
    print(f"""Your wallet

      Your balance: {chain.get_balance(wallet_address)}
      Your address: {wallet_address[1:]}...

      1 -> Send Money
      2 -> Mine Transactions
      3 -> Exit
    """
    )

    action = input("> ")
    match action:
      case "1":
        send()
      case "2":
        print("Mining transactions...")
        chain.mine_transactions(wallet_address)
        print("Mining complete.")
        sleep(1)
      case "3":
        exit()

def send():
  clear()
  print(f"""Send Money

    Your balance: {chain.get_balance(wallet_address)}

  """
  )
  receiver = input("receiver address -> ")
  amount = int(input("amount -> "))

  if amount > chain.get_balance(wallet_address):
    print("Not enough funds.")
    return 
  
  chain.add_transaction(wallet_address, receiver, amount, private_key)

  print("Transaction complete...")

  sleep(2)

if __name__ == "main":
  menu()
