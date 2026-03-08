import requests
import os
import sys

def get_rpc_connection(wallet_name=None):
    if os.path.exists("bitcoin-data/bitcoin.conf"):
        conf_path = "bitcoin-data/bitcoin.conf"
    elif os.path.exists("../bitcoin-data/bitcoin.conf"):
        conf_path = "../bitcoin-data/bitcoin.conf"
    else:
        print("Error: Could not find bitcoin.conf in current or parent directory.")
        sys.exit(1)

    config = {"rpcbind": "127.0.0.1", "rpcport": "18443"}

    with open(conf_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('#', ';', '[')): continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    rpc_user = config.get("rpcuser")
    rpc_password = config.get("rpcpassword")

    if not rpc_user or not rpc_password:
        print(f"Error: Found {conf_path} but could not extract rpcuser/rpcpassword.")
        sys.exit(1)

    rpc_host = config.get('rpcbind', '127.0.0.1')
    rpc_port = config.get('rpcport', '18443')

    base_url = f"http://{rpc_host}:{rpc_port}/"
    wallet_url = f"{base_url}wallet/{wallet_name}" if wallet_name else base_url
    auth = (rpc_user, rpc_password)

    def rpc_call(method, params=None, use_base=False):
        if params is None: params = []
        endpoint = base_url if use_base else wallet_url
        payload = {"method": method, "params": params, "jsonrpc": "2.0", "id": "lab"}

        response = requests.post(endpoint, json=payload, auth=auth)

        if response.status_code == 401:
            print(f"\n401 Unauthorized: The node rejected User '{rpc_user}'.")
            print("   -> Fix: Make sure you started bitcoind from the root Assign_2_proj_Blockchain directory!")
            sys.exit(1)

        response.raise_for_status()

        json_resp = response.json()
        if json_resp.get("error"):
            raise Exception(json_resp["error"])
        return json_resp.get("result")

    return rpc_call