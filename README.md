# ZKTeco Custom Component



## NOTE: This component currently only works with certain models. .  See [library](https://github.com/fananimi/pyzk) for compatibility.

Home Assistant component that can control the lock of ZKTeco biometrics stand alone units



## Installation

1. Download all this repositore and paste into config/custom_components
2. Add the code to your `configuration.yaml` using the config options below.
3. **You will need to restart after installation for the component to start working.**
.

## Platform Configuration

|Name|Required|Description|
|-|-|-|
|name|yes|The name of the lock|
|host|yes|IP address of unit|
|password|yes|Unit's password|
|protocol|yes|either tcp or udp|
|lock_timeout|no|The amount of seconds the door will maintain unlocked. Defaults to 15| 


## Sample lock Configuration

      lock:
        - platform: zk_teco
          name: Porta
          host: 192.168.0.202
          password: 12345
          protocol: udp
          lock_timeout: 10

    
    
    
# todo:
 - Add door sensor feedback from the unit or user given sensor entity
