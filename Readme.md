# CS 216: Bitcoin Transaction Lab Assignment

## Team Members
* **Kartik Budhani** - 240005022
* **Krishnam Digga** - 240003043
* **Rishan Gobse** - 240008023
* **Arjun Dhamdhere** - 240005011

---

## 📖 Project Overview
This repository contains the complete Python codebase and documentation for the CS 216 Bitcoin Transaction Lab. 

The primary objective of this assignment is to programmatically interact with a local Bitcoin node (`bitcoind`) via RPC to create, broadcast, and analyze Bitcoin transactions. Specifically, the project demonstrates:
1. **Legacy Transactions (P2PKH):** Generating addresses, funding them, and chaining transactions (A → B → C).
2. **SegWit Transactions (P2SH-P2WPKH):** Generating SegWit addresses, funding them, and chaining transactions (A' → B' → C').
3. **Script Extraction:** Programmatically extracting and decoding Locking Scripts (`scriptPubKey`), Unlocking Scripts (`scriptSig`), and Witness data.
4. **Size Analysis:** Comparing the raw bytes, virtual bytes (vbytes), and weight units (WU) between Legacy and SegWit transactions to demonstrate the efficiency of SegWit.

---

## 🗂️ Repository Structure

* `launch.py`: **[MASTER SCRIPT]** An automated orchestrator that runs the entire lab workflow from start to finish. It extracts transaction IDs dynamically, passes them between scripts, and generates exact terminal commands for debugging.
* `phase2_p2pkh.py`: Executes Part 1. Handles the creation and signing of the Legacy (P2PKH) transaction chain.
* `phase3_P2SH-SegWit.py`: Executes Part 2. Handles the creation and signing of the P2SH-SegWit transaction chain.
* `compare_sizes.py`: Executes Part 3. Takes specific TXIDs and outputs a comparative analysis of their sizes.
* `core_util.py`: A robust utility module that establishes a secure RPC connection to the local `bitcoind` node, handling authentication and error reporting.
* `verify_environment.py`: A lightweight script used to ensure the Bitcoin node is responsive before running the heavy transactions.

---

## ⚙️ Prerequisites & Environment Setup

### 1. Software Requirements
* **Bitcoin Core (`bitcoind`)**: Must be installed and running locally in `regtest` mode.
* **Python 3.x**: Ensure Python is installed and added to your system PATH.
* **btcdeb**: The Bitcoin Script Debugger must be installed on your system for final validation.

### 2. Python Dependencies
Install the required HTTP library for RPC calls:
```bash
pip install requests