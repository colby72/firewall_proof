![Python 3](https://img.shields.io/badge/python-3.x-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-available-brightgreen)
[![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

# Firewall Proof

## Description

Firewall compliance audit tool, designed to allow organizations to audit their Firewalls flow matrix against a set of rules, namely a security policy. It can uncover potential misconfigurations or security flaws.

To put it straight, a Firewall whose only rule **allows** flows from **all** source objects to **all** destinations on **any** service, well ... it's fairly useless actually.

For an efficient secure network filtering, a Firewall shall at least be configured with a set of rules that ensure network segregation between different object groups and network zones, following a block-all allow-required basis. These rules can further enhanced by restricting network subnets or tunneling sensitive communications (using IPSec for example).

## Installation

*TODO*

## Usage

*TODO*

## Why I started this project ?

There are several Firewall auditing solutions out there. And having practiced some of them myself, they can deliver a very decent performance in some cases.

However, most of these tools available today are proprietary, lack simplicity and flexibility, compatible with a limited set of vendors, and usually require some manual integration effort. These limitations make them merely adequate for many business needs, especially with varying business structures and IT/OT architectures across companies, thus yielding an integration and operability overhead. Besides, they're pretty much affordable only to mid to large organizations with enough cyber security budget, to cover proprietary licenses and the forementioned operating costs.

This led me to start this project, a free alternative that would be:

- **Simple and user-friendly:** Straight-forward and synthetic interface with clear features, each do one thing at a time, faithful as possible to the *KISS* philosophy *- Keep It Simple and Stupid*.

- **Flexible:** Offers a modeling backend and reporting features that would fit diffrent business use cases, from small companies with a minimal network architecture, to large organizations with networks spread across multiple zones and affiliates.

- **Extensive compbatibility:** Covers as many vendors as possible (Cisco ASA, Fortinet, Zyxell, CheckPoint, Juniper ...) through an arsenal of parsers and a dedicated data structure.

- **Thourough features:** Provide comprehensive network security analysis features and algorithms.

- **Free:** Available for large corporations, but also to small and mid-size companies who rarely have financial and human resources for a dedicated cyber security team.

But most importantly, I'm doing it to learn, sharpen my programming skills, practice my hobby  ... and to have fun.

## License

[![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License][cc-by-nc-nd].

For any commercial or professional use, please send an email to ramy.software@protonmail.com. Commercial use would be allowed in certain situations.

[![CC BY-NC-ND 4.0][cc-by-nc-nd-image]][cc-by-nc-nd]

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg