# CS 216: Bitcoin Transaction Lab Assignment

## Team Members
* **Kartik Budhani** - [Insert Roll Number]
* **[Team Member 2 Name]** - [Insert Roll Number]
* **[Team Member 3 Name]** - [Insert Roll Number]

## Project Overview
This repository contains the Python scripts and documentation for the CS 216 Bitcoin Transaction Lab. The goal is to programmatically create, broadcast, and validate Bitcoin transactions using Legacy (P2PKH) and SegWit (P2SH-P2WPKH) address formats via the Bitcoin Core RPC interface.

## Project Structure
* `launch.py`: An automated script that executes the entire lab workflow. It verifies the node, runs both transaction chains, compares their sizes, and outputs the exact `btcdeb` commands needed for debugging.
* `phase2_p2pkh.py`: Executes Part 1. Generates Legacy addresses, funds them, and chains transactions (A -> B -> C).
* `phase3_P2SH-SegWit.py`: Executes Part 2. Generates SegWit addresses, funds them, and chains transactions (A' -> B' -> C').
* `compare_sizes.py`: Executes Part 3. Compares the size, virtual size (vbytes), and weight of Legacy vs. SegWit transactions.
* `core_util.py`: A helper module for establishing a secure RPC connection to the local `bitcoind` node.

## Prerequisites
1. **Bitcoin Core (`bitcoind`)**: Running locally in `regtest` mode.
2. **Python 3.x**
3. **Required Packages**: 
   ```bash
   pip install requests