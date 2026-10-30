# ha-demand-bug

## Procedure

- Plug in Raspberry Pi Pico 2 W while holding BootSel button
- Copy the uf2 file to the Pico, which will reboot automatically
```
cp RPI_PICO2_W-20260824-v1.29.0.uf2 /Volumes/RP2350/
```
- In Thonny or similar, run test3.py

## Specs

Panel specs: https://files.waveshare.com/upload/5/59/2.13inch_e-Paper_V3_Specificition.pdf

Original source: https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.13_V3.py

See also: https://github.com/cdjq/DFRobot_RPi_Display_V3
