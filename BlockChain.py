from time import time
import json
import hashlib
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from flask import Flask

class BlockChain (object):
    def __init__(self):
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        #how difficult it is to mine a block
        self.difficulty = 4
        #currency reward to miner
        self.minerReward = 50
        #how many transactions per block
        self.blockSize = 10

    def addTransaction (self, sender, receiver, amt, keyString, senderKey):
        keyByte = keyString.encode("ASCII")
        senderKeyByte = senderKey.encode("ASCII")

        key = RSA.import_key(keyByte)
        senderKey = RSA.import_key(senderKeyByte)

        if not sender or not receiver or not amt:
            print ("transaction error")
            return False

        transaction = Transaction(sender, receiver, amt)

        transaction.signTransaction(key, senderKey)

        if not transaction.isValidTransaction():
            print("transaction error: invalid")
            return False
        self.pendingTransactions.append(transaction)
        return len(self.chain) + 1

    def getLastBlock(self):
        return self.chain[-1]

    # def addBlock(self, block):
    #     if (len(self.chain) > 0):
    #         block.prev = self.getLastBlock().hash
    #     else:
    #         self.addGenesisBlock()
    #     self.chain.append(block)

    #add first empty block
    def addGenesisBlock(self):
        tArr = []
        tArr.append(Transaction("me", "hue Jazz", 10))
        genesis = Block(tArr, time(), 0)
        genesis.prevHash = "none"
        return genesis

    def chainJSONencode(self):
        blockArrJSON = []
        for block in self.chain:
            blockJSON = {}
            blockJSON['hash'] = block.hash
            #blockJSON['index'] = block.index
            blockJSON['prev'] = block.prevHash
            #blockJSON['time'] = block.time
            #blockJSON['nonse'] = block.nonse
            #blockJSON['gym'] = block.gym


            transactionsJSON = []
            tJSON = {}
            for transaction in block.transactions:
                tJSON['time'] = transaction.time
                tJSON['sender'] = transaction.sender
                tJSON['receiver'] = transaction.receiver
                tJSON['amt'] = transaction.amt
                tJSON['hash'] = transaction.hash
                transactionsJSON.append(tJSON)

            blockJSON['transactions'] = transactionsJSON

            blockArrJSON.append(blockJSON)

        return blockArrJSON

    def generateKeys (self):
        key = RSA.generate(2048)
        privateKey = key.export_key()
        file_out = open("private.pem", 'wb')
        file_out.write(privateKey)

        publicKey = key.publickey().export_key()
        file_out = open("receiver.pem", 'wb')
        file_out.write(publicKey)

        return key.publickey().export_key().decode('ASCII')



    def minePendingTransactions(self, miner):
        #just gets length of pending transations list and check if there is a pending transaction
        lenPT = len(self.pendingTransactions)
        if (lenPT < 1):
            print("cannot mine, no transactions to write to a block")
            return False

        else:
            for i in range(0, lenPT, self.blockSize):

                end = i + self.blockSize
                
                if i >= lenPT:
                    end = lenPT
                
                transactionSlice = self.pendingTransactions[i:end]

                newBlock = Block(transactionSlice, datetime.now().strftime("%m/%d/%y, %H:%M:%S"), len(self.chain))
                prevHash = self.getLastBlock().hash
                newBlock.prevHash = prevHash
                newBlock.mineBlock(self.difficulty)
                self.chain.append(newBlock)
            print("mining transactions worked!")
            payMiner = Transaction("Miner Rewards", miner, self.minerReward)
            self.pendingTransactions = [payMiner]
        return True
        

class Block (object):
    def __init__(self, transactions, time, index):
        self.transactions = transactions #data list
        self.time = time # time block is created
        self.nonce = 0
        self.index = index # block number
        self.prevHash = '' # previous hash
        self.hash = self.calculateHash() #function to implement later gets hash of this block

    def calculateHash(self):
        # create a string containing all transactions in the block
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash

        # Create a string with all transations and metadata
        hashString = str(self.time) + hashTransactions + self.prevHash + str(self.nonce)
        # make it JSON
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        #encode it
        return hashlib.sha256(hashEncoded).hexdigest()

    def mineBlock(self, difficulty):
        # create goal hash 
        #an array that is [o,1,2,3...difficulty]
        arr = []
        for i in range(0,difficulty):
            arr.append(i)
        
        #turn that array into a string of 01234---difficulty
        arrStr = map(str, arr)
        hashPuzzle = ''.join(arrStr)

        #while our brute forced hash is not equal to the goal hash
        while self.hash[0:difficulty] != hashPuzzle:
            self.nonce += 1
            self.hash = self.calculateHash()
        #     print("nonce: ", self.nonce)
        #     print("hash Attempt: \t", self.hash)
        #     print("goal hash: \t", hashPuzzle, "...\n")
        # print("")
        print("Block Mined!")
        print("Nonce is: ", self.nonce)
        return True


class Transaction (object):
    def __init__(self, sender, receiver, amt):
        self.sender = sender
        self.receiver = receiver
        self.amt = amt # amount in transaction
        self.time = time()
        self.hash = self.calculateHash()

    def signTransaction(self, key, senderKey):
        if (self.hash != self.calculateHash()):
            print("transaction tamper error")
            return False
        if (str(key.publickey().export_key()) != str(senderKey.publickey().export_key())):
            print("transaction attempted to be signed from another wallet")
            return False

        pkcs1_15.new(key)

        self.signature = "made"
        print ("made signature!")
        return True

    def isValidTransaction(self):
        if(self.hash != self.calculateHash()):
            return False
        if(self.sender == self.receiver):
            return False
        if not self.signature or len(self.signature) ==0:
            print("No Signature!")
            return False
        return True


    def calculateHash (self):
        # create a string from all incoming data
        hashString = self.sender + self.receiver + str(self.amt) + str(self.time)
        # JSON the string
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        # Use Sha 256 to encode the json
        return hashlib.sha256(hashEncoded).hexdigest()
