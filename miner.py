import hashlib, pickle
from datetime import datetime

class Transaction:
  def __init__(self, from_address, to_address, amount):
    self.from_address = from_address
    self.to_address = to_address
    self.amount = amount


class Block:
  def __init__(self, timestamp: datetime, transactions: list, prevHash: str):
    self.timestamp = timestamp
    self.transactions = transactions
    self.prevHash = prevHash
    self.nonce = 0
    self.hash = self.calculate_hash()
  
  def calculate_hash(self) -> str:
    hash = hashlib.sha256()
    hash.update(format(self.timestamp, "b").encode())
    hash.update(pickle.dumps(self.transactions))             # FIX
    hash.update(self.prevHash.encode())
    hash.update(format(self.nonce, "b").encode())
    return hash.hexdigest()

  def mine(self, difficulty):
    while self.hash[:difficulty] != "0" * difficulty:
      self.nonce += 1
      self.hash = self.calculate_hash()
    

class Blockchain:
  def __init__(self):
    self.chain = [Block(datetime.now(), "", "")]
    self.pending_transactions = []
    self.difficulty = 4
    self.mine_reward = 1
  
  def last_block(self) -> Block:
    return self.chain[-1]

  def mine_transactions(self, miner_address):
    # create new block and mine it
    block = Block(datetime.now(), self.pending_transactions, self.last_block().hash) 
    block.mine(self.difficulty)
    self.chain.append(block)

    # reset pending transactions and add reward
    self.pending_transactions = [Transaction(None, miner_address, self.mine_reward)]
  
  def add_transaction(self, transaction: Transaction):
    self.pending_transactions.append(transaction)

  def get_balance(self, address) -> int:
    balance = 0

    for block in self.chain:
      for transaction in block.transactions:
        # if it is the sender
        if transaction.from_address == address:
          balance -= transaction.amount

        # if it is the receiver
        elif transaction.to_address == address:
          balance += transaction.amount

    return balance

  def validation_check(self) -> bool:
    for block in self.chain[1:]:
      # check if hash is valid
      if block.hash != block.calculate_hash():
        return False
      
      # check if previous hash is valid
      if block.prevHash != self.chain[self.chain.index(block) - 1].hash:
        return False
    
    return True

  def print(self):
    for block in self.chain:
      print("---")
      print(f"index: {self.chain.index(block)}")
      print(f"time: {block.timestamp}")
      print(f"transactions: {block.transactions}")
      print(f"prevHash: {block.prevHash}")
      print(f"nonce: {block.nonce}")
      print(f"hash: {block.hash}")
    print("---")
    print(f"Is valid? {self.validation_check()}")

coin = Blockchain()
coin.add_transaction(Transaction(504, 505, 50))
coin.add_transaction(Transaction(505, 506, 20))
coin.mine_transactions(507)
coin.print()

print(f'504: {coin.get_balance(504)}')
print(f'505: {coin.get_balance(505)}')
print(f'506: {coin.get_balance(506)}')
print(f'507: {coin.get_balance(507)}')
