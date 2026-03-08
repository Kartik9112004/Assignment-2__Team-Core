from core_util import get_rpc_connection


def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    # ⚠️ Paste your actual TXIDs here (Use the B -> C transactions for a fair comparison)
    legacy_txid = "da4f88a2e94570c84ec7946614f16d6f4ec1101ed55aed219e3878a6e95049a7"  # Your Legacy Tx2
    segwit_txid = "98b5f6408b772dde47cf7f973f953a75a5a692bf896c1ed6232de7aa6ec4861c"  # Your SegWit Tx2

    print("======================================================")
    print("📊 PART 3: TRANSACTION SIZE COMPARISON")
    print("======================================================\n")

    try:
        # Fetch and decode the Legacy transaction
        legacy_tx = rpc("gettransaction", [legacy_txid])
        legacy_decoded = rpc("decoderawtransaction", [legacy_tx["hex"]])

        # Fetch and decode the SegWit transaction
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