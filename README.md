# ESPHome IKEA VINDRIKTNING

## [LinkTree](https://linktr.ee/DzurisHome)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/DzurisHome)

</br>

### How to make IKEA VINDRIKTNING Smart

### Benefits
- Locally
- MQTT
- Home Assistant Autodiscovery
- Web Server
- OTA Update

</br>

> [!NOTE]
> ### Whats need
> 
> ESPHome or Download [Firmware](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/README.md#esphome-firmwares)
> 
> ESP Board with 5V or Step-Down Converter for ESP Board with 3V
> 
> Some Cables
> 
> Soldering Iron
> 
> Soldering Gun
> 
> Tools
>
> USB Cable for Flashing Board

</br>

![Home Assistant ESPHome Bedroom Air Quality](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/Home%20Assistant%20ESPHome%20Bedroom%20Air%20Quality.png)
![ESPHome WebServer Bedroom Air Quality](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/ESPHome%20WebServer%20Bedroom%20Air%20Quality.png)

</br>

> [!CAUTION]
> ### Recommendations
>
> Boards [XIAO ESP32-C3](https://s.click.aliexpress.com/e/_Dd9y9cz), [ESP32 Wemos D1 Mini](https://s.click.aliexpress.com/e/_DFpDpnJ), [ESP32 C3 Super Mini](https://s.click.aliexpress.com/e/_DlP529f) or [ESP8266 Wemos D1 Mini](https://s.click.aliexpress.com/e/_Dm8FxHL)
> 
> Cables [Dupont Line](https://s.click.aliexpress.com/e/_DFdLicl)
>
> [ESPHome Web Flasher](https://web.esphome.io/) for Flashing ESP Board

</br>

![IKEA VINDRIKTNING PCB](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%20PCB.png)
![IKEA VINDRIKTNING PCB Cables](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%20PCB%20Cables.png)

| VINDRIKTNING | ESP Board or Step-Down Converter |
|--------------|----------------------------------|
| 🔴 +5V       | 5 Voltage                        |
| ⚫ GND       | Ground                           |

| VINDRIKTNING | ESP32 Wemos D1 Mini |
|--------------|---------------------|
| 🟡 REST      | GPIO21              |
| 🟢 FAN-      | GPIO16              |

| VINDRIKTNING | XIAO-ESP32-C3 |
|--------------|---------------|
| 🟡 REST      | GPIO6         |
| 🟢 FAN-      | GPIO9         |

| VINDRIKTNING | ESP32 C3 Supermini |
|--------------|--------------------|
| 🟡 REST      | GPIO8              |
| 🟢 FAN-      | GPIO3              |

| VINDRIKTNING | ESP8266 Wemos D1 Mini |
|--------------|-----------------------|
| 🟡 REST      | D2                    |
| 🟢 FAN-      | D4                    |

</br>

> [!IMPORTANT]
> Read this before Flashing if you have Single Core Chip and using BLE (Like ESP32 C3 Super Mini) [Use on single-core chips](https://esphome.io/components/esp32_ble_tracker.html#use-on-single-core-chips)
> 
> Config for [ESP32 Single Chip BLE](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/esp32_single_core_ble.yaml)

### ESPHome Configs
- [Example](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/example.yaml)
- [ESP32 Wemos D1 Mini](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/esp32_wemos_d1_mini.yaml)
- [ESP32 C3 Super Mini](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/esp32_c3_super_mini.yaml)
- [ESP8266 Wemos D1 Mini](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/esp8266_wemos_d1_mini.yaml)
- RP2040 SOON Maybe

### ESPHome Firmwares
- SOON

</br>

![IKEA VINDRIKTNING 0.6](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.6.png)
![IKEA VINDRIKTNING on the Shelf](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%20on%20the%20Shelf.png)

### Colors
🟩 `GREEN` 0-35 μg/m³

🟧 `ORANGE` 36-85 μg/m³

🟥 `RED` 86+ μg/m³

</br>

![IKEA VINDRIKTNING 0.5](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.5.png)
![IKEA VINDRIKTNING 0.7](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.7.png)
![IKEA VINDRIKTNING 0.8](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.8.png)

## [LinkTree](https://linktr.ee/DzurisHome)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/DzurisHome)
