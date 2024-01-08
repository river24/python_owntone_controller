# `python_owntone_controller`

`python_owntone_controller` is a Python script to control [OwnTone](https://owntone.github.io/owntone-server/) by some input devices.

## Supported Input Devices

Currently, it supports the following input devices:

- [FiiO KB1K](https://fiio.com/productinfo/950623.html)

## How to Use

### Preparetion

```
$ git clone https://github.com/river24/python_owntone_controller
$ cd python_owntone_controller
$ ./scripts/prepare.bash
```

- creates python3 venv dir named `venv` on the top of the project directory
- install python modules in `requirements.txt` to the python3 venv

### Installation

```
$ sudo ./scripts/install.bash
```

- creates `/etc/systemd/system/python_owntone_controller.service` from `./configs/systemd.base`
- runs `systemctl daemon-reload`
- enables `python_owntone_controller.service`
- starts `python_owntone_controller.service`

### Uninstallation

```
$ sudo ./scripts/uninstall.bash
```

- stops `python_owntone_controller.service`
- disables `python_owntone_controller.service`
- deletes `/etc/systemd/system/python_owntone_controller.service`
- runs `systemctl daemon-reload`

## Acknowledgements

This project uses code from [this repository](https://github.com/econchick/mayhem) ([related article](https://www.roguelynn.com/words/asyncio-graceful-shutdowns/)), which is licensed under the MIT License. We are grateful to the contributors of the repository for their work.

## [License](LICENSE)

The MIT License (MIT)

Copyright (c) 2024 river24

