from core_util import get_rpc_connection
import json
import sys

def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    try:
        with open("tx_data.json", "r") as f:
            data = json.load(f)
            txid_funding = data["legacy_tx1"]
            txid_spending = data["legacy_tx2"]
    except (FileNotFoundError, KeyError):
        print("Error: Could not find legacy TXIDs. Please run phase2_p2pkh.py first.")
        sys.exit(1)

    txin_data = rpc("gettransaction", [txid_funding])
    tx_data = rpc("gettransaction", [txid_spending])

    txin_hex = txin_data["hex"]
    tx_hex = tx_data["hex"]

    print("======================================================")
    print("Run this exact command in your terminal:")
    print("======================================================\n")
    print(f"btcdeb --tx={tx_hex} --txin={txin_hex}")
    print("\n======================================================")

if __name__ == "__main__":
    main()