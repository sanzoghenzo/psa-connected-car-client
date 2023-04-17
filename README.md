# PSA Connected Car API Client

API client for PSA groupe connected car service.

This is a rework of the wonderful [PSA Car Controller](https://github.com/flobz/psa_car_controller) by [@flobz](https://github.com/flobz).

The goal is to extract the core functionality and provide it as a library to be used by systems like Home Assistant directly, without the need to run a separate server.

It builds upon some great libraries:

- `httpx` for the asynchronous REST API requests
- `authlib` to handle the Oauth2 authentication
- `msgspec` for the decoding of the API response into python classes
- `pyaxmlparser`, a lighter alternative to `androguard`, to get the needed information from the PSA android app

## TODO

### MQTT

Può essere che REST API non aggiorni stato carica; se da mqtt EventMessage.is_charging e REST API energy electric.charging_status != in progress chiamo un wakeup

Per aggiornare token:

"https://api.groupe-psa.com/connectedcar/v4/virtualkey/remoteaccess/token?client_id={client_id}"

headers = {
  "x-introspect-realm": self.account_info.realm,
  "accept": "application/hal+json",
  "User-Agent": "okhttp/4.8.0",
}

#### OTP

- Classe Otp salvata e caricata con pickle
- metodo pubblico get_otp_code con rate limit di 6 al giorno, può dare ConfigException, in tal caso serve ripetere config
- codice via SMS tramite API POST f"https://api.groupe-psa.com/applications/cvs/v4/mobile/smsCode?client_id={client_id}", e headers come sopra

### ABRP
TODO: return the "tlm" dict from VeichleStatus, the ABRP

POST https://api.iternio.com/1/tlm/send
{
  "token": token,
  "api_key": api_key,
  "tlm": {
    "utc": int(datetime.timestamp(energy.updated_at)),
    "soc": energy.level,
    "speed": getattr(kinetic, "speed", None),
    "car_model": abrp_name
    "current": battery.current,
    "is_charging": energy.charging.status == "InProgress",
    "lat": last_position.geometry.coordinates[1],
    "lon": last_position.geometry.coordinates[0],
    "power": energy.consumption
  }
}

## Per Home Assistant

- platform è hub, un'istanza per device (auto) multiple
- config flow
  - tipo user che chiede
    - brand auto
    - email
    - password
    - country code
  - step successivo è OTP via SMS + PIN app
- devices li posso ottenere con list veichles
- entities escono da get veichle info - alcune dipendono da motore etc
- platforms:
  - binary sensor per roba booleana
  - device tracker per last_position
  - Lock per porte (se c'è)
  - sensori per il resto
  - notifications? posso mandare roba all'infotainment?
  - buttons: switch per roba attivabile (quasi tutta MQTT)
