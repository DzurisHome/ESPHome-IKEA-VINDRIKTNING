# ESPHome IKEA VINDRIKTNING

## [LinkTree](https://linktr.ee/DzurisHome)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N6M7OX3)

</br>

### How to make IKEA VINDRIKTNING Smart

### Benefits
- Home Assistant Autodiscovery
- MQTT
- Locally
- WebServer
- OTA Updates

</br>

> [!IMPORTANT]
> ### Whats need
> 
> ESPHome or Download [Firmware](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/README.md#esphome-firmwares)
> 
> ESP Board with 5V or Step-Down Converter for ESP Board with 3V
>
> MQ-135 only if we want too Carbon Monoxide and ESP Board with ADC Pin too
> 
> Some Cables
> 
> Soldering Iron
> 
> Soldering Gun
> 
> Tools
>
> USB Cable for Flashing

</br>

![Home Assistant ESPHome Integration Living Room Air Quality](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/Home%20Assistant%20ESPHome%20Integration%20Living%20Room%20Air%20Quality.jpg)
![ESPHome WebServer Living Room Air Quality](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/ESPHome%20WebServer%20Living%20Room%20Air%20Quality.png)

</br>

> [!IMPORTANT]
> ### Recommendations
>
> Boards [ESP8266 Wemos D1 Mini](https://s.click.aliexpress.com/e/_Dm8FxHL), [XIAO ESP32-C3](https://s.click.aliexpress.com/e/_Dd9y9cz), [ESP32 Wemos D1 Mini](https://s.click.aliexpress.com/e/_DFpDpnJ) or [ESP32 C3 SuperMini](https://s.click.aliexpress.com/e/_DlP529f)
>
> Carbon Monoxide [MQ-135](https://s.click.aliexpress.com/e/_DDRkLM1)
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

| VINDRIKTNING | ESP8266 Wemos D1 Mini |
|--------------|-----------------------|
| 🟡 REST      | D2                    |
| 🟢 FAN-      | D4                    |

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

</br>

![MQ-135 Caables](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/MQ-135%20Cables.png)

| MQ-135    | ESP Board or Step-Down Converter |
|-----------|----------------------------------|
| 🔴 VCC    | 5/3 Voltage                      |
| ⚫ GND    | Ground                           |

| VINDRIKTNING | ESP8266 Wemos D1 Mini |
|--------------|-----------------------|
| 🟢 A OUT     | A0                    |

| VINDRIKTNING | ESP32 Wemos D1 Mini |
|--------------|---------------------|
| 🟢 A OUT     | GPIO34              |

| VINDRIKTNING | XIAO-ESP32-C3 |
|--------------|---------------|
| 🟢 A OUT     | GPIO2         |

| VINDRIKTNING | ESP32 C3 Supermini |
|--------------|--------------------|
| 🟢 A OUT     | GPIO5              |

</br>

![IKEA VINDRIKTNING 0.1](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.1.jpg)
![IKEA VINDRIKTNING 0.2](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.2.png)
![IKEA VINDRIKTNING 0.3](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.3.png)
![IKEA VINDRIKTNING 0.4](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/Images/IKEA%20VINDRIKTNING%200.4.png)

</br>

### ESPHome Configs
- [ESP](https://github.com/DzurisHome/ESPHome-IKEA-VINDRIKTNING/blob/main/ESPHome%20Config/esp-config.yaml)
- RP2040 SOON

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
