[![Testing](https://github.com/sht2017/iptv/actions/workflows/CI.yaml/badge.svg)](https://github.com/sht2017/iptv/actions/workflows/CI.yaml)
[![codecov](https://codecov.io/github/sht2017/iptv/graph/badge.svg?token=VCN5CCEC5F)](https://codecov.io/github/sht2017/iptv)
[![GitHub License](https://img.shields.io/github/license/sht2017/iptv)](https://github.com/sht2017/iptv/blob/main/LICENSE)

[English](README.md) | 中文

# IPTV 模拟

中国电信 IPTV 认证实用程序及示例项目。

测试于湖北

## 它是如何工作的？
加密和授权算法（位于 `/src/epg/` 中的软件包）根据 Python 的最佳实践以现代方式进行了优化和重写。原始算法来自对我的机顶盒上的鉴权app的逆向工程。

示例项目的核心思想是放弃对每个软件包的模拟，因为模拟需要对鉴权过程进行分析，很难适应不同地区的情况。我最终选择与在机顶盒相同的方式，即使用浏览器来自动化。且这样更易于调试和控制。

为此，我实现了 `/src/browser/` 包，以自动完成授权并接收EPG信息。具体来说，`/src/browser/browser.py` 提供了一个用来交互，可以在到达目标后自动退出的浏览器接口。此外，`/src/browser/remote_injector/` 提供了一些类和函数，用于将 Python 方法和类作为 JavaScript 注入浏览器。

## 如何使用？
依赖：git、python>=3.10（在 python 3.12 上测试）、python3-pip、python3-venv
> ⚠️ 因为最新版本（1.45.0）的一个bug会导致无法运行，目前将playwright的版本冻结在1.44.0。（可以通过 `/src/browser/remote_injector/inject.py` 成功注入远程调用方法 `/src/browser/remote_injector/template/invokeRemoteFunction.js` ，但无法调用）
- ## linux
    - ### Debian-like (Debian, Ubuntu, etc...)
        - ### 初始化
            ```shell
            sudo apt-get update
            sudo apt-get install git python3 python3-pip python3-venv -y
            ```
            ```shell
            git clone https://github.com/sht2017/iptv.git
            cd iptv
            ./setup.py
            ```
        - ### 运行示例项目

            > ⚠️ 配置文件 `/config.yaml` 是必须的
            >
            > ℹ️ 可以以 `/config.example.yaml` 的示例为基础创建

            ```shell
            PYTHONPATH="$(pwd)/src:${PYTHONPATH}" python3 src/custom/main.py
            ```
            检查 `/db.json` ，其中可能包含了你需要的信息
- ## Windows
    - ### CMD
        - ### 初始化
            > ⚠️ 在您的系统中winget可能是不可用的
            ```cmd
            winget install --id Git.Git -e --source winget
            winget install python3 --source winget
            ```
            ```cmd
            git clone https://github.com/sht2017/iptv.git
            cd iptv
            python setup.py
            ```
        - ### 运行示例项目

            > ⚠️ 配置文件 `/config.yaml` 是必须的
            >
            > ℹ️ 可以以 `/config.example.yaml` 的示例为基础创建

            ```cmd
            set PYTHONPATH=%cd%\src;%PYTHONPATH%
            python src/custom/main.py
            ```
            检查 `/db.json` ，其中可能包含了你需要的信息


## 开发

对于实用库，请检查 `src/epg` 中的docstring，如果要开发自己的EPG解析服务建议在 `/src/custom/` 中修改。

## 致谢 (排名不分先后)
- 中国电信 
- [Telecom-IPTV-Mock](https://github.com/VergilGao/Telecom-IPTV-Mock) - [@VergilGao](https://github.com/VergilGao)
- [RouterOS 抓包 IPTV & 实现 IPTV 的认证和频道列表获取 - Skimige's Blog](https://xyx.moe/018-RouterOS-IPTV-packet-capture-and-authentication-implementation.html) [<sup>Archived on July 11, 2024</sup>](https://web.archive.org/web/20240711154952/https://xyx.moe/018-RouterOS-IPTV-packet-capture-and-authentication-implementation.html)
 