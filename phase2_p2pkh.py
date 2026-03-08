import requests
import json
import sys
import time

CONF_FILE_PATH = "bitcoin-data/bitcoin.conf"


def read_bitcoin_conf(filepath):
    config = {"rpcbind": "127.0.0.1", "rpcport": "18443"}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('['): continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"❌ Error: Could not find {filepath}.")
        sys.exit(1)


def main():
    config = read_bitcoin_conf(CONF_FILE_PATH)
    rpc_user = config.get("rpcuser")
    rpc_password = config.get("rpcpassword")

    # We will connect directly to the wallet endpoint
    url = f"http://{config.get('rpcbind', '127.0.0.1')}:{config.get('rpcport', '18443')}/wallet/lab_wallet"
    base_url = f"http://{config.get('rpcbind', '127.0.0.1')}:{config.get('rpcport', '18443')}/"
    headers = {'content-type': 'application/json'}

    def rpc(method, params=[], use_base=False):
        endpoint = base_url if use_base else url
        payload = {"method": method, "params": params, "jsonrpc": "2.0", "id": "part1"}
        response = requests.post(endpoint, data=json.dumps(payload), headers=headers, auth=(rpc_user, rpc_password))
        response.raise_for_status()
        return response.json()['result']

    print("======================================================")
    print("⛓️  PHASE 2: LEGACY P2PKH TRANSACTION CHAIN (A -> B -> C)")
    print("======================================================\n")

    # 1. Create/Load Wallet
    try:
        rpc("createwallet", ["lab_wallet"], use_base=True)
    except Exception:
        pass  # Wallet already exists, which is fine

    # 2. Generate Legacy Addresses
    print("-> Generating Addresses A, B, and C...")
    addr_A = rpc("getnewaddress", ["Address_A", "legacy"])
    addr_B = rpc("getnewaddress", ["Address_B", "legacy"])
    addr_C = rpc("getnewaddress", ["Address_C", "legacy"])
    print(f"   Address A: {addr_A}")
    print(f"   Address B: {addr_B}")
    print(f"   Address C: {addr_C}\n")

    # 3. Fund Address A
    print("-> Mining 101 blocks to mature coinbase rewards...")
    dummy_addr = rpc("getnewaddress")
    rpc("generatetoaddress", [101, dummy_addr])

    print("-> Funding Address A with 10 BTC using 'sendtoaddress'...")
    txid_fund_A = rpc("sendtoaddress", [addr_A, 10.0])
    rpc("generatetoaddress", [1, dummy_addr])  # Mine 1 block to confirm funding
    print(f"   Funding TXID: {txid_fund_A}\n")

    # ==========================================
    # TRANSACTION 1: ADDRESS A -> ADDRESS B
    # ==========================================
    print("======================================================")
    print("💸 TRANSACTION 1: A -> B")

    # Get UTXO for A
    unspent_A = rpc("listunspent", [1, 9999999, [addr_A]])[0]
    print(f"-> Selected UTXO for Address A: {unspent_A['txid']} (Vout: {unspent_A['vout']})")

    # Create Raw Transaction
    fee = 0.0001
    send_amount_B = unspent_A['amount'] - fee
    inputs_1 = [{"txid": unspent_A['txid'], "vout": unspent_A['vout']}]
    outputs_1 = {addr_B: send_amount_B}

    raw_tx_1 = rpc("createrawtransaction", [inputs_1, outputs_1])

    # Decode to extract ScriptPubKey (The Challenge)
    decoded_raw_1 = rpc("decoderawtransaction", [raw_tx_1])
    scriptPubKey_B = decoded_raw_1['vout'][0]['scriptPubKey']['asm']
    print(f"-> Extracted ScriptPubKey (Locking Script) for Address B:")
    print(f"   [CHALLENGE]: {scriptPubKey_B}")

    # Sign and Broadcast
    signed_tx_1 = rpc("signrawtransactionwithwallet", [raw_tx_1])
    txid_1 = rpc("sendrawtransaction", [signed_tx_1['hex']])
    rpc("generatetoaddress", [1, dummy_addr])  # Mine block to confirm TX 1
    print(f"✅ Transaction A -> B Broadcasted & Confirmed! TXID: {txid_1}\n")

    # ==========================================
    # TRANSACTION 2: ADDRESS B -> ADDRESS C
    # ==========================================
    print("======================================================")
    print("💸 TRANSACTION 2: B -> C")

    # Get UTXO for B
    unspent_B = rpc("listunspent", [1, 9999999, [addr_B]])[0]
    print(f"-> Selected UTXO for Address B: {unspent_B['txid']} (Vout: {unspent_B['vout']})")

    # Create Raw Transaction
    send_amount_C = unspent_B['amount'] - fee
    inputs_2 = [{"txid": unspent_B['txid'], "vout": unspent_B['vout']}]
    outputs_2 = {addr_C: send_amount_C}

    raw_tx_2 = rpc("createrawtransaction", [inputs_2, outputs_2])

    # Sign and Broadcast
    signed_tx_2 = rpc("signrawtransactionwithwallet", [raw_tx_2])
    txid_2 = rpc("sendrawtransaction", [signed_tx_2['hex']])
    rpc("generatetoaddress", [1, dummy_addr])  # Mine block to confirm TX 2
    print(f"✅ Transaction B -> C Broadcasted & Confirmed! TXID: {txid_2}\n")

    # Decode SIGNED transaction to extract ScriptSig (The Response)
    decoded_signed_2 = rpc("decoderawtransaction", [signed_tx_2['hex']])
    scriptSig_B = decoded_signed_2['vin'][0]['scriptSig']['asm']
    print(f"-> Extracted ScriptSig (Unlocking Script) from Address B:")
    print(f"   [RESPONSE]: {scriptSig_B[:60]}... (truncated for readability)")
    print("\n🎉 PHASE 2 COMPLETE! You have successfully chained two legacy transactions.")


if __name__ == "__main__":
    main()