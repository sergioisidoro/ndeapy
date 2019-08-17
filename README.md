# ndeapy 
## [A Nordea open banking api](https://developer.nordeaopenbanking.com/) version 4 python client with uplink

# How to use

0. Install requirements 

```shell
pip install -r requirements.txt
```

1. Export your client variables 

```shell
export NDEAPY_CLIENT_ID="<YOUR_CLIENT_ID>"
export NDEAPY_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
export NDEAPAY_SIGNATURE_KEY="./QSealC-NordeaDevPortal.p12"
export NDEAPAY_SIGNATURE_KEY_PASSPHRASE="1111"
```

Optionally pass them as kwars to the client constructor
```python
client = Ndeapy(
    "TOKEN",
    client_id="CLIENTID",
    client_secret="SECRET"
    )
```

2. Pass the token to the client, and make your API calls

```python
from ndeapy import *
import json

client = Ndeapy("YOUR_TOKEN")
accounts = client.get_accounts()

# Print accounts
print("Accounts response")
print(json.dumps(accounts, indent=4, sort_keys=True))
```

# Currently supported operations

```
from ndeapy import *
import json


client = Ndeapy(
    # VERY SECRET STUFF HERE...
    )

accounts = client.get_accounts()
print("Accounts response")
print(json.dumps(accounts, indent=4, sort_keys=True))

test_account = accounts["response"]["accounts"][0]
account = client.get_account(test_account["_id"])

print("Accounts detail")
print(json.dumps(account, indent=4, sort_keys=True))

print("Accounts transactions")
transactions = client.get_transactions(test_account["_id"])
print(json.dumps(transactions, indent=4, sort_keys=True))
```