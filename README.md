# PSA Connected Car API Client

API client for PSA group connected car service.

This is a rework of the wonderful [PSA Car Controller](https://github.com/flobz/psa_car_controller) by [@flobz](https://github.com/flobz).

The goal is to extract the core functionality and provide it as a library to be used by systems like Home Assistant directly, without the need to run a separate server.

It builds upon some great libraries:

- `httpx` for the asynchronous REST API requests
- `authlib` to handle the Oauth2 authentication
- `msgspec` for the decoding of the API response into python classes
- `pyaxmlparser`, a lighter alternative to `androguard`, to get the needed information from the PSA android app

## Installation

```shell
pip install psa-connected-car-client
```

## Usage

A basic usage of the library can be found at `tests/demo_cli.py`.

### Simple version

You can create the `PSAClient` using the `create_psa_client` function.

```python
from psa_ccc import create_psa_client


async def main():
    client = await create_psa_client(brand, country_code, email, password)
```

The arguments are self-explanatory, but just in case:

- `brand` is the car brand; possible values are:
  - `Peugeot`
  - `Citroen`
  - `DS`
  - `Opel`
  - `Vauxhall`
- `country_code` is your 2 letter uppercase country code
- `email` is the address you used to register to the "MyBrand" app
- `password` is - you guessed it - the password for the app

Behind the scenes, this function will download the APK of the mobile app, extract the data needed to establish a connection to the PSA servers and save it in a config file.
Subsequent runs of the function will read from that config file, if it exists.

You're now ready to use the client to talk to the PSA connected car service!

```python
    user = await client.get_user()
    print("User:", user)
    vehicles = await client.get_vehicles()
    print("Vehicles:", vehicles)
    vehicle_id = vehicles[0].id
    vehicle = await client.get_vehicle(vehicle_id)
    print("First vehicle:", vehicle)
    alerts = await client.get_vehicle_alerts(vehicle_id)
    print("Vehicle alerts:", alerts)
    status = await client.get_vehicle_status(vehicle_id)
    print("Vehicle status:", status)
    maintenance = await client.get_vehicle_maintenance(vehicle_id)
    print("Vehicle maintenance:", maintenance)
    print(
        "Vehicle position:",
        status.last_position.geometry.coordinates,
        "last updated at",
        status.last_position.properties.updated_at,
    )
```

### Customizable storage

the `create_psa_client` function accepts two optional parameters for choosing where to store the configuration and the auth tokens:

- `cache_storage` accepts any implementation of the `CacheStorage` protocol.
  The library comes with the `SimpleCacheStorage` class that stores the files inside the given directory.
  This is the storage used in the [simple version](#simple-version) above, and uses the current working directory as storage.
- `token_storage` accepts any implementation of the `TokenStorage` protocol.
  Again, the library has a `MemoryTokenStorage` class that keeps the token in memory (it is never written to disk).
  This is the default token storage for the [simple version](#simple-version) above.

```python
from pathlib import Path
from psa_ccc import SimpleCacheStorage
from psa_ccc import MemoryTokenStorage
from psa_ccc import create_psa_client


async def main():
    storage = SimpleCacheStorage(Path(__file__).parent)
    token_storage = MemoryTokenStorage()
    client = await create_psa_client(
        brand, country_code, email, password, storage, token_storage
    )
    # do whatever you want with client...
```
