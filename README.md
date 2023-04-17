# PSA Connected Car API Client

API client for PSA groupe connected car service.

This is a rework of the wonderful [PSA Car Controller](https://github.com/flobz/psa_car_controller) by [@flobz](https://github.com/flobz).

The goal is to extract the core functionality and provide it as a library to be used by systems like Home Assistant directly, without the need to run a separate server.

It builds upon some great libraries:

- `httpx` for the asynchronous REST API requests
- `authlib` to handle the Oauth2 authentication
- `msgspec` for the decoding of the API response into python classes
- `pyaxmlparser`, a lighter alternative to `androguard`, to get the needed information from the PSA android app
