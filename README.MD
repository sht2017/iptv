[![Testing](https://github.com/sht2017/iptv/actions/workflows/CI.yaml/badge.svg)](https://github.com/sht2017/iptv/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/sht2017/iptv/graph/badge.svg?token=VCN5CCEC5F)](https://codecov.io/github/sht2017/iptv)
[![GitHub License](https://img.shields.io/github/license/sht2017/iptv)](https://github.com/sht2017/iptv/blob/main/LICENSE)

English | [中文](README_chs.md)

# IPTV Simulate 

Utilities for China Telecom's IPTV authentication with an example.

Tested in Hubei

## How does it work?
The encryption and authorization algorithm (package located in `/src/epg/`) is optimized and rewritten based on the best practices of Python in a modern way. Original algorithms have come from reverse engineering of the app on my STB. 

The core idea of the example project is to give up on simulating each package, which took a complex analysis and made it impossible to fit different cases. I eventually chose to use the same way originally on the STB, a browser. It's way more easy to debug and control.

For that, I implemented the package `/src/browser/` to automatically finish the authorization and receive EPG. Specifically, `/src/browser/browser.py` provides a browser interface which allows me to interact with it and will auto-quit once the destination address is hit. And the `/src/browser/remote_injector/` provides a few classes and functions to inject Python methods and classes to the browser as JavaScript.

## How to use?
requirement: git, python>=3.10 (tested on Python 3.12), python3-pip, python3-venv
> ⚠️ the version of the playwright currently freezes to 1.44.0 because there is a critical bug on the latest version (1.45.0) which leads to failure. (The `/src/browser/remote_injector/template/invokeRemoteFunction.js` would successfully be injected via `/src/browser/remote_injector/inject.py` but won't work)
- ## linux
    - ### Debian-like (Debian, Ubuntu, etc...)
        - ### Setup
            ```shell
            sudo apt-get update
            sudo apt-get install git python3 python3-pip python3-venv -y
            ```
            ```shell
            git clone https://github.com/sht2017/iptv.git
            cd iptv
            ./setup.py
            ```
        - ### Run Example Project

            > ⚠️ `/config.yaml` is required
            >
            > ℹ️ You can create it as in `/config.example.yaml`

            ```shell
            PYTHONPATH="$(pwd)/src:${PYTHONPATH}" python3 src/custom/main.py
            ```
            Go check `/db.json` and enjoy
- ## Windows
    - ### CMD
        - ### Setup
            > ⚠️ winget might not available on your system
            ```cmd
            winget install --id Git.Git -e --source winget
            winget install python3 --source winget
            ```
            ```cmd
            git clone https://github.com/sht2017/iptv.git
            cd iptv
            python setup.py
            ```
        - ### Run Example Project

            > ⚠️ `/config.yaml` is required
            >
            > ℹ️ You can create it as in `/config.example.yaml`

            ```cmd
            set PYTHONPATH=%cd%\src;%PYTHONPATH%
            python src/custom/main.py
            ```
            Go check `/db.json` and enjoy


## Development

for utility libs check docstring in src/epg, suggest to modify in `/src/custom/`.

## Acknowledgement (not listed in order)
- China Telecom 
- [Telecom-IPTV-Mock](https://github.com/VergilGao/Telecom-IPTV-Mock) - [@VergilGao](https://github.com/VergilGao)
- [RouterOS 抓包 IPTV & 实现 IPTV 的认证和频道列表获取 - Skimige's Blog](https://xyx.moe/018-RouterOS-IPTV-packet-capture-and-authentication-implementation.html) [<sup>Archived on July 11, 2024</sup>](https://web.archive.org/web/20240711154952/https://xyx.moe/018-RouterOS-IPTV-packet-capture-and-authentication-implementation.html)
 