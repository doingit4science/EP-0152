# 52Pi EP-0152 Raspberry Pi Fan Expansion Board - _UPDATED for Raspberry Pi 5_

Updated source code for the [52Pi EP-0152 Raspberry Pi Fan Expansion Board](https://52pi.com/products/raspberry-pi-cooling-fan-expansion-board-plus-0-91-oled-v1-0-compatible-for-raspberry-pi-4b-3b-3b-2b), sold on Amazon as [GeeekPi Fan Hat for Raspberry Pi 4 Model B, PWM Fan GPIO Expansion Board with 0.91inch OLED Display for Raspberry Pi 4B/3B+/3B/2B](https://a.co/d/0fnQFZCU).

The [original code](https://wiki.52pi.com/index.php?title=EP-0152) listed for the fan hat is woefully out of date, as it won't work for the Raspberry Pi 5 and doesn't use the [PEP 668 specification](https://peps.python.org/pep-0668/), which is now [required for Rasberry Pi OS](http://rptl.io/venv).

This repository is compatible with the following Raspberry Pi versions on [Raspberry Pi OS (64-bit) / Debian GNU/Linux 12 (bookworm)](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-64-bit):

- Raspberry Pi 5B ( :white_check_mark: - Tested)
- Raspberry Pi 4B ( :white_check_mark: - Tested)
- Raspberry Pi 3B+/3B ( :question: - Untested)
- Raspberry Pi 2B ( :question: - Untested)

## Assembly Steps

[![How to assemble the Fan hat.](https://wiki.52pi.com/images/thumb/4/4a/Oledfan%E5%AE%89%E8%A3%85.jpg/800px-Oledfan%E5%AE%89%E8%A3%85.jpg "52Pi EP-0152 Assembly")](https://wiki.52pi.com/index.php?title=EP-0152)

## Python Requirements

1. Create a Python Virtual Environment to install `pip` packages.

    ```bash
    sudo -i
    python3 -m venv /opt/EP-0152
    source /opt/EP-0152/bin/activate
    ```

2. Install `pip3` packages:

    ```bash
    pip3 install board busio pillow adafruit_circuitPython_ssd1306
    ```

    - For **Raspbery Pi 5**:

        ```bash
        pip3 uninstall RPI.GPIO
        pip3 install rpi-lgpio
        ```

3. Remember to exit from `sudo -i`:

    ```bash
    exit
    ```

## Fan Control

I've added [@franganghi](https://github.com/franganghi)'s version of [Raspberry-Pi5-PWM-Fan-Control](https://github.com/franganghi/Raspberry-Pi5-PWM-Fan-Control) as a submodule to this repository. To pull the submodule after cloning this repository, run:

```bash
cd EP-0152
git submodule update --init --recursive
```

After doing so, follow the instructions listed in the [README](https://github.com/franganghi/Raspberry-Pi5-PWM-Fan-Control/tree/master?tab=readme-ov-file#raspberry-pi5-pwm-fan-control) to install [as a Linux service](https://github.com/franganghi/Raspberry-Pi5-PWM-Fan-Control/tree/master?tab=readme-ov-file#as-a-service).

## PWM LEDs

### LEDs Installation

```bash
cd EP-0152/LEDs
sudo mkdir /opt/EP-0152/LEDs
sudo cp ep0152ledpwm.service /lib/systemd/system/ep0152ledpwm.service
sudo cp LEDsV2.* /opt/EP-0152/LEDs/.
sudo chmod 644 /lib/systemd/system/ep0152ledpwm.service
sudo chmod +x /opt/EP-0152/LEDs/LEDsV2.py
sudo chmod +x /opt/EP-0152/LEDs/LEDsV2.sh
sudo systemctl daemon-reload
sudo systemctl enable --now ep0152ledpwm.service
```

### LEDs Check Status

```bash
$ sudo systemctl status ep0152ledpwm.service
● ep0152ledpwm.service - EP-0152 LEDs PWM Pulse
     Loaded: loaded (/lib/systemd/system/ep0152ledpwm.service; enabled; preset: enabled)
     Active: active (running) since Fri 2024-06-21 10:34:34 PDT; 1h 13min ago
   Main PID: 2701 (LEDsV2.sh)
      Tasks: 5 (limit: 9248)
        CPU: 3.627s
     CGroup: /system.slice/ep0152ledpwm.service
             ├─2701 /bin/bash /opt/EP-0152/LEDs/LEDsV2.sh
             └─2710 python3 /opt/EP-0152/LEDs/LEDsV2.py

Jun 21 10:34:34 host systemd[1]: Started ep0152ledpwm.service - EP-0152 LEDs PWM Pulse.
```

### LEDs Uninstallation

```bash
sudo systemctl stop ep0152ledpwm.service
sudo systemctl disable ep0152ledpwm.service
sudo systemctl daemon-reload
sudo rm /lib/systemd/system/ep0152ledpwm.service
sudo rm -rf /opt/EP-0152/LEDs
```

## OLED Screen

Credit to [@AmazonShopper](https://www.amazon.com/gp/profile/amzn1.account.AH6T6UZJDFOPJJFIU7NEEZSCIVKA/) for [providing the edits](https://www.amazon.com/gp/customer-reviews/R2X09M6QTQ2GJC) to the original code.

### OLED Installation

```bash
cd EP-0152/OLED
sudo mkdir /opt/EP-0152/OLED
sudo cp ep0152oled.service /lib/systemd/system/ep0152oled.service
sudo cp oledV2.py /opt/EP-0152/OLED/.
sudo cp OLED.sh /opt/EP-0152/OLED/.
sudo chmod 644 /lib/systemd/system/ep0152oled.service
sudo chmod +x /opt/EP-0152/LEDs/oledV2.py
sudo chmod +x /opt/EP-0152/LEDs/OLED.sh
sudo systemctl daemon-reload
sudo systemctl enable --now ep0152oled.service
```

### OLED Check Status

```bash
$ sudo systemctl status ep0152oled.service
● ep0152oled.service - EP-0152 OLED Monitor
     Loaded: loaded (/lib/systemd/system/ep0152oled.service; enabled; preset: enabled)
     Active: active (running) since Fri 2024-06-21 10:34:34 PDT; 1h 18min ago
   Main PID: 2703 (OLED.sh)
      Tasks: 2 (limit: 9248)
        CPU: 1min 729ms
     CGroup: /system.slice/ep0152oled.service
             ├─2703 /bin/bash /opt/EP-0152/OLED/OLED.sh
             └─2711 python3 /opt/EP-0152/OLED/oledV2.py

Jun 21 10:34:34 host systemd[1]: Started ep0152oled.service - EP-0152 OLED Monitor.
```

### OLED Uninstallation

```bash
sudo systemctl stop ep0152oled.service
sudo systemctl disable ep0152oled.service
sudo systemctl daemon-reload
sudo rm /lib/systemd/system/ep0152oled.service
sudo rm -rf /opt/EP-0152/OLED
```

## Uninstallation of Python VEnv

```bash
sudo rm -rf /opt/EP-0152
```
