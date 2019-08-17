import os
from uplink import Consumer, get, Path, Query, returns, response_handler

# You can define these in the os level, or durint client initialization
CLIENT_ID = os.getenv('NDEAPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('NDEAPY_CLIENT_SECRET')


def raise_for_status(response):
    """Checks whether or not the response was successful."""
    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response

    raise UnsuccessfulRequest(response.url)

@response_handler(raise_for_status)  # First, check success
class Ndeapy(Consumer):
    """A Python Client for the NDEA API."""

    def __init__(self, access_token, client_id= None, client_secret= None):
        super(Ndeapy, self).__init__(base_url="https://api.nordeaopenbanking.com/v3/")
        self.session.headers["Authorization"] = "Bearer {}".format(str(access_token))
        self.session.headers["X-IBM-Client-Secret"] = client_id or CLIENT_SECRET
        self.session.headers["X-IBM-Client-Id"] = client_secret or CLIENT_ID

    @returns.json
    @get("accounts")
    def get_accounts(self):
       """Get accounts"""

    @returns.json
    @get("accounts/{account_id}")
    def get_account(self, account_id):
       """Get account details"""

    @returns.json
    @get("accounts/{account_id}/transactions")
    def get_transactions(self, account_id):
       """Get account transactions"""
