#  ![img.png](https://ipntest.alfaline.dev/img/log_in/header_logo.svg)
<hr/>

![image](https://img.shields.io/pypi/v/ipn-pi.svg)
![image](https://img.shields.io/pypi/pyversions/ipn-py.svg)

A modern, easy-to-use library for interacting with the [IPN](https://ipn.tools/), written in Python.
<hr/>


## Key Features
<hr/>

- Interaction with the [IPN](https://ipn.tools/) API.
- Creating and managing transactions.

## Installing
<hr/>

**Python 3.9 or higher is required**


To install the library, use the command
```bash
pip install ipnpy
```

To install the development version, do the following:

```bash
git clone https://github.com/IPNTools/ipn-py
cd ipnpy
```

## Quick Example
<hr/>

Send transaction:
```python
from ipnpy.rpc import EvmJsonRPC

provider = EvmJsonRPC('https://data-seed-prebsc-1-s2.binance.org:8545/')
transaction = provider.send_native_token(
    private_key='YOUR_PRIVATE_KEY',
    from_address='0xdB87EE96B5D2D7F5b0e9eC400240D605f870756f',
    to_address='0xdB87EE96B5D2D7F5b0e9eC400240D605f870756f',
    amount=23000,
)

print(transaction)
```

Add, replace and delete address in [IPN](https://ipn.tools/):
```python
from ipnpy.ipn import IPNTools

ipn = IPNTools(secret_key='YOUR_SECRET_KEY')
ipn.add_address('address4')
ipn.replace_addresses(addresses=['address1', 'address2', 'address3'])
ipn.delete_address('address3')
```

## Links
<hr/>

- [Official IPN site](https://ipn.tools/)
- [Telegram channel](https://t.me/ipn_tools)