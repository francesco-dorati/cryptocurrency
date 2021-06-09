import hashlib, pickle, ecdsa
from types import WrapperDescriptorType
from datetime import datetime

from ecdsa.ecdsa import Signature

class Transaction:
  def __init__(self, index: int, sender: str, receiver: str, amount: int):
    self.index = index
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    self.signature = None

  
  def calculate_hash(self) -> str:
    hash = hashlib.sha256()
    hash.update(format(self.index, "b").encode()) # index
    hash.update(self.sender.encode()) # sender
    hash.update(self.receiver.encode()) # receiver
    hash.update(format(self.amount, "b").encode()) # amount
    return hash.hexdigest()

  def sign(self, private_key: str):
    sk = ecdsa.SigningKey.from_string(bytearray.fromhex(private_key), ecdsa.SECP256k1)
    public_key: str = sk.verifying_key.to_string().hex()

    # check if the user owns that wallet
    if self.sender != public_key:
      raise Exception("Cannot sign transactions from wallet you don't own.")
    
    self.signature = sk.sign(self.calculate_hash().encode()) # .encode()


  def verify(self):
    # if mine reward
    if not self.sender and not self.signature:
      return True

    # if invalid transaction
    if not self.sender  or not self.receiver or not self.amount or not self.signature:
      return False

    # verify signature
    vk = ecdsa.VerifyingKey.from_string(bytearray.fromhex(self.sender), ecdsa.SECP256k1)
    return vk.verify(self.signature, self.calculate_hash().encode())

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
    hash.update(pickle.dumps(self.transactions))
    hash.update(self.prevHash.encode())
    hash.update(format(self.nonce, "b").encode())
    return hash.hexdigest()

  def mine(self, difficulty):
    while self.hash[:difficulty] != "0" * difficulty:
      self.nonce += 1
      self.hash = self.calculate_hash()
  
  def verify_transactions(self):
    for transaction in self.transactions:
      if not transaction.verify():
        return False
    
    return True
    

class Blockchain:
  def __init__(self):
    self.DIFFICULTY = 4
    self.MINE_REWARD = 500

    self.chain = [Block(datetime.now(), [], "")]
    self.pending_transactions = []
  
  def last_block(self) -> Block:
    return self.chain[-1]

  def mine_transactions(self, miner_address):
    # create new block and mine it
    block = Block(datetime.now(), self.pending_transactions, self.last_block().hash) 
    block.mine(self.DIFFICULTY)
    self.chain.append(block)

    # reset pending transactions and add reward
    self.pending_transactions = [Transaction(0, None, miner_address, self.MINE_REWARD)]

  
  def add_transaction(self, sender: str, receiver: str, amount: int, private_key: str = None):
    # check for double spending
    index = self.pending_transactions[-1].index + 1

    # if mining reward
    if sender == None and private_key == None:
      self.pending_transactions.append(Transaction(index, None, receiver, amount))
      return

    if not private_key:
      raise Exception("Private key necessary.")

    # check for double spending
    if amount > self.get_balance(sender):
      raise Exception("Not enough funds.")

    # create transaction
    transaction = Transaction(index, sender, receiver, amount)
    transaction.sign(private_key)

    # if is valid
    if not transaction.verify():
      raise Exception("Invalid transaction.")

    # push to the blockchain
    self.pending_transactions.append(transaction) 

  def get_balance(self, address) -> int:
    balance = 0

    for block in self.chain:
      for transaction in block.transactions:
        # if it is the sender
        if transaction.sender == address:
          balance -= transaction.amount

        # if it is the receiver
        elif transaction.receiver == address:
          balance += transaction.amount

    return balance

  def validation_check(self) -> bool:
    for block in self.chain[1:]:
      # check if has valid transactions
      if not block.verify_transactions:
        return False

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
