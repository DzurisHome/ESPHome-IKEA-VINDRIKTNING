# ESPHome IKEA VINDRIKTNING <a href="https://esphome.io"><img align="right" src="Images/Buttons/ESPHome-Compatible.svg" height="48" alt="Compatible with ESPHome"></a>

<a href="https://linktr.ee/DzurisHome"><img src="Images/Buttons/Linktree.svg" height="36" alt="Find me on Linktree"></a>&nbsp;
<a href="https://ko-fi.com/DzurisHome"><img src="https://ko-fi.com/img/githubbutton_sm.svg" height="36" alt="Support me on Ko-fi"></a>

</br>

### How to make IKEA VINDRIKTNING Smart

### Benefits
- Local Control
- MQTT
- Home Assistant Autodiscovery
- Web Server
- OTA Update
- Ready-made Firmware

</br>

> [!NOTE]
> ### What You Need
>
> ESPHome or [Ready-made Firmware](https://dzurishome.github.io/ESPHome-IKEA-VINDRIKTNING/)
>
> ESP Board with 5V or Step-Down Converter for ESP Board with 3V
>
> Some Cables
>
> Soldering Iron
>
> Hot Glue Gun
>
> Tools
>
> USB Cable for Flashing Board

</br>

<img src="Images/Home%20Assistant%20ESPHome%20Bedroom%20Air%20Quality.png" height="494" alt="Home Assistant ESPHome Bedroom Air Quality"> <img src="Images/ESPHome%20WebServer%20Bedroom%20Air%20Quality.png" height="494" alt="ESPHome WebServer Bedroom Air Quality">

</br>

> [!CAUTION]
> ### Recommendations
>
> Boards [XIAO ESP32-C3](https://s.click.aliexpress.com/e/_Dd9y9cz), [ESP32 Wemos D1 Mini](https://s.click.aliexpress.com/e/_DFpDpnJ), [ESP32 C3 Super Mini](https://s.click.aliexpress.com/e/_DlP529f) or [ESP8266 Wemos D1 Mini](https://s.click.aliexpress.com/e/_Dm8FxHL)
>
> Cables [Dupont Line](https://s.click.aliexpress.com/e/_DFdLicl)
>
> **Ready-made Firmware** → [Firmware Installer](https://dzurishome.github.io/ESPHome-IKEA-VINDRIKTNING/) — pick your board and click Install, no ESPHome needed
>
> **Own Firmware** (built in your ESPHome) → [ESPHome Web](https://web.esphome.io/)

</br>

<img src="Images/IKEA%20VINDRIKTNING%20PCB.png" height="420" alt="IKEA VINDRIKTNING PCB"> <img src="Images/IKEA%20VINDRIKTNING%20PCB%20Cables.png" height="420" alt="IKEA VINDRIKTNING PCB Cables">

| VINDRIKTNING | ESP Board or Step-Down Converter |
|--------------|----------------------------------|
| 🔴 +5V       | 5 Voltage                        |
| ⚫ GND       | Ground                           |

| VINDRIKTNING | ESP32 Wemos D1 Mini |
|--------------|---------------------|
| 🟡 REST      | GPIO21              |
| 🟢 FAN-      | GPIO16              |

| VINDRIKTNING | XIAO ESP32-C3 |
|--------------|---------------|
| 🟡 REST      | GPIO6         |
| 🟢 FAN-      | GPIO9         |

| VINDRIKTNING | ESP32 C3 Super Mini |
|--------------|---------------------|
| 🟡 REST      | GPIO8               |
| 🟢 FAN-      | GPIO3               |

| VINDRIKTNING | ESP8266 Wemos D1 Mini |
|--------------|-----------------------|
| 🟡 REST      | D2                    |
| 🟢 FAN-      | D4                    |

</br>

### ESPHome Configs
- [Example](ESPHome%20Config/Example.yaml)
- [ESP32 Wemos D1 Mini](ESPHome%20Config/ESP32_Wemos_D1_Mini.yaml)
- [ESP32 C3 Super Mini](ESPHome%20Config/ESP32_C3_Super_Mini.yaml)
- [ESP8266 Wemos D1 Mini](ESPHome%20Config/ESP8266_Wemos_D1_Mini.yaml)

### Firmware
<a href="https://dzurishome.github.io/ESPHome-IKEA-VINDRIKTNING/"><img src="Images/Buttons/Ready-made-Firmware.svg" width="374" alt="Install Ready-made Firmware"></a>

</br>

<img src="Images/IKEA%20VINDRIKTNING%200.1.png" height="300" alt="IKEA VINDRIKTNING 0.1">

<img src="Images/IKEA%20VINDRIKTNING%200.2.png" height="300" alt="IKEA VINDRIKTNING 0.2"> <img src="Images/IKEA%20VINDRIKTNING%200.4.png" height="300" alt="IKEA VINDRIKTNING 0.4">

### Colors
🟩 `GREEN` 0-35 μg/m³

🟧 `ORANGE` 36-85 μg/m³

🟥 `RED` 86+ μg/m³

</br>

<img src="Images/IKEA%20VINDRIKTNING%200.6.png" height="350" alt="IKEA VINDRIKTNING 0.6"> <img src="Images/IKEA%20VINDRIKTNING%200.7.png" height="350" alt="IKEA VINDRIKTNING 0.7"> <img src="Images/IKEA%20VINDRIKTNING%200.8.png" height="350" alt="IKEA VINDRIKTNING 0.8">

<img src="Images/IKEA%20VINDRIKTNING%20on%20the%20Shelf.png" height="373" alt="IKEA VINDRIKTNING on the Shelf">

</br>

<a href="https://linktr.ee/DzurisHome"><img src="Images/Buttons/Linktree.svg" height="36" alt="Find me on Linktree"></a>&nbsp;
<a href="https://ko-fi.com/DzurisHome"><img src="https://ko-fi.com/img/githubbutton_sm.svg" height="36" alt="Support me on Ko-fi"></a>
