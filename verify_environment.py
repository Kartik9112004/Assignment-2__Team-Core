import requests
import json
import sys

CONF_FILE_PATH = "bitcoin-data/bitcoin.conf"

def read_bitcoin_conf(filepath):
    config = {
        "rpcbind": "127.0.0.1",
        "rpcport": "18443",
    }
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('['):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}. Make sure you are running this script from the TeamCore directory.")
        sys.exit(1)

def main():
    print("========================================")
    print("Verifying Phase 1 Environment & Setup")
    print("========================================\n")

    print("Reading configuration from bitcoin.conf...")
    config = read_bitcoin_conf(CONF_FILE_PATH)

    rpc_user = config.get("rpcuser")
    rpc_password = config.get("rpcpassword")
    rpc_host = config.get("rpcbind", "127.0.0.1")
    rpc_port = config.get("rpcport", "18443")

    if not rpc_user or not rpc_password:
        print("Error: rpcuser or rpcpassword not found in bitcoin.conf.")
        sys.exit(1)

    url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}/"
    headers = {'content-type': 'application/json'}

    def rpc_call(method, params=[]):
        payload = {"method": method, "params": params, "jsonrpc": "2.0", "id": "verify_script"}
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print(f"Connection Error: Could not connect to bitcoind at {rpc_host}:{rpc_port}.")
            sys.exit(1)
        except Exception as e:
            print(f"RPC call failed: {e}")
            sys.exit(1)

    print(f"Connecting to RPC at {rpc_host}:{rpc_port}...")
    blockchain_info = rpc_call("getblockchaininfo")

    chain = blockchain_info['result']['chain']
    if chain == 'regtest':
        print(f"Node is successfully running in '{chain}' mode.")
    else:
        print(f"Node is running in '{chain}' mode instead of 'regtest'.")

    network_info = rpc_call("getnetworkinfo")
    version = network_info['result']['subversion']
    print(f"Connected to Bitcoin Core. Version: {version}")

    print("\nPhase 1 Verification Complete!")

if __name__ == "__main__":
    main()