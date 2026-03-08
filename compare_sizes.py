from core_util import get_rpc_connection
import json
import sys

def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    try:
        with open("tx_data.json", "r") as f:
            data = json.load(f)
            legacy_txid = data["legacy_tx2"]
            segwit_txid = data["segwit_tx2"]
    except (FileNotFoundError, KeyError):
        print("Error: Could not find TXIDs. Please run Phase 2 and Phase 3 scripts first.")
        sys.exit(1)

    print("======================================================")
    print("PART 3: TRANSACTION SIZE COMPARISON")
    print("======================================================\n")

    try:
        legacy_tx = rpc("gettransaction", [legacy_txid])
        legacy_decoded = rpc("decoderawtransaction", [legacy_tx["hex"]])

        segwit_tx = rpc("gettransaction", [segwit_txid])
        segwit_decoded = rpc("decoderawtransaction", [segwit_tx["hex"]])

        print("--- LEGACY (P2PKH) ---")
        print(f"Size:   {legacy_decoded['size']} bytes")
        print(f"Vsize:  {legacy_decoded['vsize']} vbytes")
        print(f"Weight: {legacy_decoded['weight']} WU (Weight Units)\n")

        print("--- SEGWIT (P2SH-P2WPKH) ---")
        print(f"Size:   {segwit_decoded['size']} bytes")
        print(f"Vsize:  {segwit_decoded['vsize']} vbytes")
        print(f"Weight: {segwit_decoded['weight']} WU (Weight Units)\n")

        print("======================================================")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()