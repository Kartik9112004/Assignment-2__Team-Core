from core_util import get_rpc_connection
import sys


def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    # ⚠️ REPLACE THESE with the exact TXIDs from your Phase3_Segqit.py terminal output!
    txid_funding = "3d93a5a1398fadf082a3d8026a36edec1725b0cc7c8b338285bdae1ac402dac3"  # Tx 1 (A' -> B')
    txid_spending = "98b5f6408b772dde47cf7f973f953a75a5a692bf896c1ed6232de7aa6ec4861c"  # Tx 2 (B' -> C')

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
        print(f"❌ Error fetching transactions. Did you paste the right TXIDs? Error: {e}")


if __name__ == "__main__":
    main()