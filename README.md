# ndeapy - A Norde open banking api python client with uplink

# How to use

1. Export your client variables (Optionally pass them as kwars to the client constructor)
```
export NDEAPY_CLIENT_ID=<YOUR_CLIENT_ID>
export NDEAPY_CLIENT_SECRET=<YOUR_CLIENT_SECRET>
```

2. Pass the token to the client, and make your API calls
```
from ndeapy import *
import json

client = Ndeapy("YOUR_TOKEN")
accounts = client.get_accounts()

# Print accounts
print("Accounts response")
print(json.dumps(accounts, indent=4, sort_keys=True))
```

# Currently supported operations

## Accounts

#### client.get_accounts()

#### client.get_account(<account_id>)

#### client.get_transactions(<account_id>)