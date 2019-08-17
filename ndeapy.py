import os
import requests
from time import strftime, gmtime
from requests_http_signature import HTTPSignatureHeaderAuth
from OpenSSL import crypto 
from uplink import Consumer, get, Path, Query, returns, response_handler, headers

if os.getenv('NDEAPY_DEBUG'):
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

# You can define these in the os level, or durint client initialization
CLIENT_ID = os.getenv('NDEAPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('NDEAPY_CLIENT_SECRET')
SIGNATURE_KEY = os.getenv('NDEAPAY_SIGNATURE_KEY')
NDEAPAY_SIGNATURE_KEY_PASSPHRASE = os.getenv('NDEAPAY_SIGNATURE_KEY_PASSPHRASE')

class UnsuccessfulNdeapyRequest(Exception):
    pass


class NdeapyConfigError(Exception):
    pass

# Extract keys from the p12 file
def extract_from_p12(filename, passphrase):
    if not filename:
        raise NdeapyConfigError("P12 file path (NDEAPAY_SIGNATURE_KEY) not specified on ENV")

    p12 = crypto.load_pkcs12(open(filename, 'rb').read(), passphrase)
    cert = p12.get_certificate()        # (signed) certificate object
    key = p12.get_privatekey()          # private key.
    ca_cert = p12.get_ca_certificates() # ca chain.

    return (cert, key, ca_cert)

def raise_for_status(response):
    """Checks whether or not the response was successful."""
    if 200 <= response.status_code < 300:
        # Pass through the response.
        return response

    raise UnsuccessfulNdeapyRequest(response.url + " :: " + response.text)

@response_handler(raise_for_status)  # First, check success
@headers({"X-Nordea-Originating-Date": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())})
class Ndeapy(Consumer):
    """A Python Client for the NDEA API."""

    def __init__(self, access_token, client_id=None, client_secret=None):

        (cert, key, ca_cert) = extract_from_p12(SIGNATURE_KEY, NDEAPAY_SIGNATURE_KEY_PASSPHRASE)

        session = requests.Session()
        session.auth = HTTPSignatureHeaderAuth(
            algorithm="rsa-sha256", 
            key=crypto.dump_privatekey(crypto.FILETYPE_PEM, key), 
            key_id=(client_id or CLIENT_ID),
            headers=["(request-target)", "x-nordea-originating-host", "x-nordea-originating-date"])

        super(Ndeapy, self).__init__(
            base_url="https://api.nordeaopenbanking.com/v4/",
            client=session
        )
        
        self.session.headers["Authorization"] = "Bearer {}".format(str(access_token))
        self.session.headers["X-IBM-Client-Secret"] = client_secret or CLIENT_SECRET
        self.session.headers["X-IBM-Client-Id"] = client_id or CLIENT_ID
        self.session.headers["X-Nordea-Originating-Host"] = "api.nordeaopenbanking.com"
        
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
