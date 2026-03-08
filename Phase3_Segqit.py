from core_util import get_rpc_connection
import sys


def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    print("======================================================")
    print("⛓️  PART 2: P2SH-SEGWIT TRANSACTION CHAIN (A' -> B' -> C')")
    print("======================================================\n")

    # 1. Create/Load Wallet without swallowing errors
    try:
        rpc("loadwallet", ["lab_wallet"], use_base=True)
        print("✅ Loaded existing wallet: lab_wallet")
    except Exception as e:
        if "already loaded" in str(e).lower() or "duplicate" in str(e).lower():
            print("✅ Wallet lab_wallet is already loaded.")
        else:
            try:
                rpc("createwallet", ["lab_wallet"], use_base=True)
                print("✅ Created new wallet: lab_wallet")
            except Exception as e2:
                print(f"❌ Failed to create or load wallet: {e2}")
                sys.exit(1)

    # 2. Generate P2SH-SegWit Addresses
    print("\n-> Generating Addresses A', B', and C'...")
    addr_A = rpc("getnewaddress", ["Address_A_Segwit", "p2sh-segwit"])
    addr_B = rpc("getnewaddress", ["Address_B_Segwit", "p2sh-segwit"])
    addr_C = rpc("getnewaddress", ["Address_C_Segwit", "p2sh-segwit"])
    print(f"   Address A': {addr_A}")
    print(f"   Address B': {addr_B}")
    print(f"   Address C': {addr_C}\n")

    # 3. Fund Address A'
    print("-> Mining 101 blocks to mature coinbase rewards...")
    dummy_addr = rpc("getnewaddress", ["Miner", "p2sh-segwit"])
    rpc("generatetoaddress", [101, dummy_addr])

    print("-> Funding Address A' with 10 BTC using 'sendtoaddress'...")
    txid_fund_A = rpc("sendtoaddress", [addr_A, 10.0])
    rpc("generatetoaddress", [1, dummy_addr])
    print(f"   Funding TXID: {txid_fund_A}\n")

    # ==========================================
    # TRANSACTION 1: ADDRESS A' -> ADDRESS B'
    # ==========================================
    print("======================================================")
    print("💸 TRANSACTION 1: A' -> B'")

    unspent_A = rpc("listunspent", [1, 9999999, [addr_A]])[0]
    print(f"-> Selected UTXO for Address A': {unspent_A['txid']} (Vout: {unspent_A['vout']})")

    fee = 0.0001
    send_amount_B = unspent_A['amount'] - fee
    inputs_1 = [{"txid": unspent_A['txid'], "vout": unspent_A['vout']}]
    outputs_1 = {addr_B: send_amount_B}

    raw_tx_1 = rpc("createrawtransaction", [inputs_1, outputs_1])

    decoded_raw_1 = rpc("decoderawtransaction", [raw_tx_1])
    scriptPubKey_B = decoded_raw_1['vout'][0]['scriptPubKey']['asm']
    print(f"-> Extracted ScriptPubKey (Challenge Script) for Address B':")
    print(f"   [CHALLENGE B']: {scriptPubKey_B}")

    signed_tx_1 = rpc("signrawtransactionwithwallet", [raw_tx_1])
    txid_1 = rpc("sendrawtransaction", [signed_tx_1['hex']])
    rpc("generatetoaddress", [1, dummy_addr])
    print(f"✅ Transaction A' -> B' Broadcasted & Confirmed! TXID: {txid_1}\n")

    # ==========================================
    # TRANSACTION 2: ADDRESS B' -> ADDRESS C'
    # ==========================================
    print("======================================================")
    print("💸 TRANSACTION 2: B' -> C'")

    unspent_B = rpc("listunspent", [1, 9999999, [addr_B]])[0]
    print(f"-> Selected UTXO for Address B': {unspent_B['txid']} (Vout: {unspent_B['vout']})")

    send_amount_C = unspent_B['amount'] - fee
    inputs_2 = [{"txid": unspent_B['txid'], "vout": unspent_B['vout']}]
    outputs_2 = {addr_C: send_amount_C}

    raw_tx_2 = rpc("createrawtransaction", [inputs_2, outputs_2])

    decoded_raw_2 = rpc("decoderawtransaction", [raw_tx_2])
    scriptPubKey_C = decoded_raw_2['vout'][0]['scriptPubKey']['asm']
    print(f"-> Extracted ScriptPubKey (Challenge Script) for Address C':")
    print(f"   [CHALLENGE C']: {scriptPubKey_C}")

    signed_tx_2 = rpc("signrawtransactionwithwallet", [raw_tx_2])
    txid_2 = rpc("sendrawtransaction", [signed_tx_2['hex']])
    rpc("generatetoaddress", [1, dummy_addr])
    print(f"✅ Transaction B' -> C' Broadcasted & Confirmed! TXID: {txid_2}\n")

    # Extract SegWit Responses
    decoded_signed_2 = rpc("decoderawtransaction", [signed_tx_2['hex']])
    scriptSig_B = decoded_signed_2['vin'][0]['scriptSig']['hex']
    txinwitness_B = decoded_signed_2['vin'][0].get('txinwitness', [])

    print(f"-> Extracted Unlocking Data (Response) from Address B':")
    print(f"   [scriptSig (Redeem Script Hash)]: {scriptSig_B}")
    print(f"   [txinwitness (Witness Data)]: {txinwitness_B}")

    print("\n🎉 PART 2 (SEGWIT) COMPLETE! You have successfully chained two SegWit transactions.")


if __name__ == "__main__":
    main()