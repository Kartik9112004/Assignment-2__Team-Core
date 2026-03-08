from core_util import get_rpc_connection

def main():
    rpc = get_rpc_connection(wallet_name="lab_wallet")

    # Your exact TXIDs from Phase 2
    txid_funding = "f38faf40dff384fc673552481e702c3e364827402fcae693faabeaa637626c42" # Tx 1 (A->B)
    txid_spending = "da4f88a2e94570c84ec7946614f16d6f4ec1101ed55aed219e3878a6e95049a7" # Tx 2 (B->C)

    # Use 'gettransaction' instead. It queries the wallet database and returns a dictionary.
    txin_data = rpc("gettransaction", [txid_funding])
    tx_data = rpc("gettransaction", [txid_spending])

    # Extract the raw hex string from the response
    txin_hex = txin_data["hex"]
    tx_hex = tx_data["hex"]

    print("======================================================")
    print("Run this exact command in your terminal:")
    print("======================================================\n")
    print(f"btcdeb --tx={tx_hex} --txin={txin_hex}")
    print("\n======================================================")

if __name__ == "__main__":
    main()