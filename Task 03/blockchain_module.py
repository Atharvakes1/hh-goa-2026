from web3 import Web3
import hashlib
import time

def verify_on_chain(image_path, social_url):
    print("\n[*] INITIATING BLOCKCHAIN VERIFICATION...")
    
    # 1. Connect to a lightning-fast local simulated blockchain
    w3 = Web3(Web3.EthereumTesterProvider())
    
    if not w3.is_connected():
        print("[-] Failed to connect to local blockchain.")
        return False
        
    print("[+] Connected to Local Simulated Ethereum Chain.")
    
    # Use the first auto-generated test account
    account = w3.eth.accounts[0]
    
    # 2. Create a secure Hash (Tamper-Evident Fingerprint)
    # We combine the image name and the matched URL
    raw_data = f"{image_path}::{social_url}"
    data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    print(f"[*] Generated SHA-256 Fingerprint: {data_hash}")
    
    # 3. Write the Hash to the Blockchain
    print("[*] Minting record to the blockchain...")
    
    # We embed the hash into the transaction's hex data
    tx_hash = w3.eth.send_transaction({
        'from': account,
        'to': account, # Sending to ourselves just to record the data
        'data': w3.to_bytes(text=data_hash),
        'gas': 100000
    })
    
    # 4. Confirm the transaction
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print("\n[+] SUCCESS! TAMPER-EVIDENT RECORD CREATED.")
    print(f"    -> Block Number: {receipt.blockNumber}")
    print(f"    -> Transaction Hash: {w3.to_hex(tx_hash)}")
    print(f"    -> Gas Used: {receipt.gasUsed}")
    
    return w3.to_hex(tx_hash)

# Test the module
if __name__ == "__main__":
    # We will pass a dummy URL for testing
    dummy_url = "https://www.facebook.com/WFMYNews2/videos/dummy-test"
    tx_record = verify_on_chain("test.jpg", dummy_url)
    
    if tx_record:
        print("\n[*] Module 3 is ready for the pipeline.")