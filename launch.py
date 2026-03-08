import subprocess
import re
from core_util import get_rpc_connection


def run_script(script_name, args=None):
    print(f"Executing {script_name}...")
    cmd = ['python', script_name]
    if args:
        cmd.extend(args)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(f"Error in {script_name}: {result.stderr}")
    return result.stdout


def extract_txid(output, marker_text):
    pattern = rf"{re.escape(marker_text)}\s*([a-fA-F0-9]{{64}})"
    match = re.search(pattern, output)
    return match.group(1) if match else None


def main():
    print("========================================")
    print("STARTING AUTOMATED LAB WORKFLOW")
    print("========================================\n")

    verify_output = run_script("verify_environment.py")
    print(verify_output)

    p2_output = run_script("phase2_p2pkh.py")
    p2_parent = extract_txid(p2_output, "Transaction A -> B Broadcasted & Confirmed! TXID:")
    p2_child = extract_txid(p2_output, "Transaction B -> C Broadcasted & Confirmed! TXID:")

    p3_output = run_script("phase3_P2SH-SegWit.py")
    p3_parent = extract_txid(p3_output, "Transaction A' -> B' Broadcasted & Confirmed! TXID:")
    p3_child = extract_txid(p3_output, "Transaction B' -> C' Broadcasted & Confirmed! TXID:")

    rpc = get_rpc_connection(wallet_name="lab_wallet")

    def get_hex(txid):
        return rpc("gettransaction", [txid])["hex"]

    print("\n" + "=" * 80)
    print("AUTO-GENERATED BTCDEB COMMANDS (LIVE DATA)")
    print("=" * 80)

    if p2_parent and p2_child:
        print(f"\nPHASE 2 (LEGACY):")
        print(f"btcdeb --tx={get_hex(p2_child)} --txin={get_hex(p2_parent)}")
    else:
        print("\nFailed to capture Phase 2 TXIDs. Check your print statements.")

    if p3_parent and p3_child:
        print(f"\nPHASE 3 (SEGWIT):")
        print(f"btcdeb --tx={get_hex(p3_child)} --txin={get_hex(p3_parent)}")
    else:
        print("\nFailed to capture Phase 3 TXIDs. Check your print statements.")

    print("\n" + "=" * 80 + "\n")

    if p2_child and p3_child:
        size_output = run_script("compare_sizes.py", [p2_child, p3_child])
        print(size_output)
    else:
        print("Skipping size comparison due to missing TXIDs.")


if __name__ == "__main__":
    main()