from core_util import get_rpc_connection
import json
import sys

def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    try:
        with open("tx_data.json", "r") as f:
            data = json.load(f)
            txid_funding = data["segwit_tx1"]
            txid_spending = data["segwit_tx2"]
    except (FileNotFoundError, KeyError):
        print("Error: Could not find SegWit TXIDs. Please run phase3_P2SH-SegWit.py first.")
        sys.exit(1)

    try:
        txin_data = rpc("gettransaction", [txid_funding])
        tx_data = rpc("gettransaction", [txid_spending])

        txin_hex = txin_data["hex"]
        tx_hex = tx_data["hex"]

        print("======================================================")
        print("Run this exact command in your terminal:")
        print("======================================================\n")
        print(f"btcdeb --tx={tx_hex} --txin={txin_hex}")
        print("\n======================================================")

    except Exception as e:
        print(f"Error fetching transactions: {e}")

if __name__ == "__main__":
    main()