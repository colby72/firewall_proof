![Python 3](https://img.shields.io/badge/python-3.x-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-available-brightgreen)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Firewall Proof

## Description

Firewall compliance audit tool, designed to allow organizations to audit their Firewalls flow matrix against a set of rules, namely a security policy. It can uncover potential misconfigurations or security flaws.

To put it straight, a Firewall whose only rule **allows** flows from **all** source objects to **all** destinations on **any** service, well ... it's fairly useless actually.

For an efficient secure network filtering, a Firewall shall at least be configured with a set of rules that ensure network segregation between different object groups and network zones, following a block-all allow-required basis. These rules can further enhanced by restricting network subnets or tunneling sensitive communications (using IPSec for example).

## Installation

No installation required. **Firewall Proof** is distributed as a portable standalone executable.

## Usage

- Download the appropriate ZIP archive as per your OS (Windows or Linux)
- Uncompress the archive
- Run the **Firewall Proof** executable

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

## Development status and Roadmap

The software is still in its early development stage. At this point, and in addition to bug fixes, there are several software features that can be either improved or added. Some of these, to mention a few:

- The **Reporting** feature is working. Nevertheless, reports templates are still primitive and to be further developed.
- The **Analytics** feature already implement some basic algorithms. But these are yet yet to be polished and further advanced algorithms are to be implemented.
- GUI design to be polished, especially through QSS stylesheets.
- Statistics plots to be improved.

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Licensed under the GNU General Public License, version 3 or (at your option)
any later version: ([LICENSE](LICENSE) or
<https://www.gnu.org/licenses/gpl-3.0.html>)

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

For any commercial or professional use, please first send an email to ramy.software@protonmail.com. Commercial use would be allowed in certain situations.

### Commercial and professional use

In case:

- You wish to use this software for commercial purposes, or in a professional environment
- You need more custom reporting features or report templates templates (Microsoft Word, HTML, LaTeX)
- You require technical assistance with the software usage
- Need technical advice on how to define and fine-tune an effective policy for your architecture
- You want to add custom analytics features to the software

Please send an email to ramy.software@protonmail.com and I shall be happy to help as I can.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the license above, shall be
licensed as above, without any additional terms or conditions.