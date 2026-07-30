---
title: NGI0 Review repository report (February 1, 2024 – July 31, 2026)
author:
- Ivan Minčík
geometry: a4paper, margin=1.5in
linestretch: 1.05
numbersections: true
colorlinks: true
...

# Work carried out and overview of progress

The main role of the NixOS Foundation within the NGI Zero consortium is to make
software available as Nix packages, making the projects developed under NGI0
easier to obtain and run.

During this reporting period, a new packaging and software distribution
platform - [NGI Forge](https://ngi.nixos.org/) - was developed.

NGI Forge lowers the barrier to software packaging, making it more accessible
to a wider developer and user audience while preserving all the power of Nix.
It is also significantly increasing sustainability of packaging and package
maintenance.

Packaging work was performed in the [NGIpkgs](https://github.com/ngi-nix/ngipkgs/)
and [NGI Forge](https://github.com/ngi-nix/forge/) repositories. Some of the
packaged software was upstreamed to Nixpkgs, currently the largest, most
up-to-date software repository in the world.

## Projects supported during reporting period 2

### NGIpkgs repository

Nix@NGI team has packaged the following NGI0 Review projects in NGIpkgs
repository:

- [Blink](https://ngi.nixos.org/project/Blink)
- [Bonfire](https://ngi.nixos.org/project/Bonfire)
- [Briar](https://ngi.nixos.org/project/Briar)
- [Corteza](https://ngi.nixos.org/project/Corteza)
- [CryptoLyzer](https://ngi.nixos.org/project/CryptoLyzer)
- [ERIS](https://ngi.nixos.org/project/ERIS)
- [Funkwhale](https://ngi.nixos.org/project/Funkwhale)
- [Heads](https://ngi.nixos.org/project/Heads)
- [Inventaire](https://ngi.nixos.org/project/Inventaire)
- [Irdest](https://ngi.nixos.org/project/Irdest)
- [Kaidan](https://ngi.nixos.org/project/Kaidan)
- [Kazarma](https://ngi.nixos.org/project/Kazarma)
- [Keyoxide](https://ngi.nixos.org/project/Keyoxide)
- [Liberaforms](https://ngi.nixos.org/project/Liberaforms)
- [LibreSOC](https://ngi.nixos.org/project/LibreSOC)
- [Librecast](https://ngi.nixos.org/project/Librecast)
- [Mastodon](https://ngi.nixos.org/project/Mastodon)
- [MirageOS](https://ngi.nixos.org/project/MirageOS)
- [Mobilizon](https://ngi.nixos.org/project/Mobilizon)
- [Mox](https://ngi.nixos.org/project/Mox)
- [Namecoin](https://ngi.nixos.org/project/Namecoin)
- [Nitrokey](https://ngi.nixos.org/project/Nitrokey)
- [Nominatim](https://ngi.nixos.org/project/Nominatim)
- [Re-Isearch](https://ngi.nixos.org/project/Re-Isearch)
- [SCION](https://ngi.nixos.org/project/SCION)
- [Sylk](https://ngi.nixos.org/project/Sylk)
- [ThresholdOPRF](https://ngi.nixos.org/project/ThresholdOPRF)
- [Wireguard](https://ngi.nixos.org/project/Wireguard)
- [lemmy](https://ngi.nixos.org/project/lemmy)
- [nyxt](https://ngi.nixos.org/project/nyxt)
- [owasp](https://ngi.nixos.org/project/owasp)
- [owncast](https://ngi.nixos.org/project/owncast)
- [verso](https://ngi.nixos.org/project/verso)

All packaged projects are available via the NGIpkgs web UI at
[https://ngi-nix.github.io/ngipkgs/](https://ngi-nix.github.io/ngipkgs/).

### NGI Forge repository

Nix@NGI team has packaged the following NGI0 Review projects in NGI Forge
repository:

- [BANG](https://ngi.nixos.org/app/bang)
- [CryptoLyzer](https://ngi.nixos.org/app/cryptolyzer)
- [Dino](https://ngi.nixos.org/app/dino)
- [Fractal](https://ngi.nixos.org/app/fractal)
- [Himalaya](https://ngi.nixos.org/app/himalaya)
- [Kaitai Struct](https://ngi.nixos.org/app/kaitai-struct)
- [Mox](https://ngi.nixos.org/app/mox)
- [Nyxt](https://ngi.nixos.org/app/nyxt)
- [Offen](https://ngi.nixos.org/app/offen)
- [PyCM](https://ngi.nixos.org/app/pycm)
- [QLever](https://ngi.nixos.org/app/qlever)
- [Re-Isearch](https://ngi.nixos.org/app/re-isearch)
- [Sequoia PGP](https://ngi.nixos.org/app/sequoia-pgp)
- [Servo](https://ngi.nixos.org/app/servo)
- [Variation Graphs](https://ngi.nixos.org/app/vg)
- [Zenroom](https://ngi.nixos.org/app/zenroom)
- [ip2unix](https://ngi.nixos.org/app/ip2unix)

All packaged projects are available via the NGI Forge web UI at
[https://ngi.nixos.org/](https://ngi.nixos.org/).

## Events

The Nix@NGI team organized the Summer of Nix 2025 program and participated as
a partner in the [Outreachy](https://www.outreachy.org/) program in 2025.

Team members have actively participated in NixCon 2025 and FOSDEM 2026 with
multiple presentations.

NixCon 2025 presentations:

- "How NixOS is built: From Pull Request to your `/nix/store`" by Dionysis Grigoropoulos
- "Life without Kubernetes: Hosting Mirrors with NixOS" by Sizhe Zhao

FOSDEM 2026 presentations:

- "Nix Forge - become a Nix smith over the weekend" by Ivan Mincik

## Overview of communication efforts

The following is the list of team communication channels:

- Team page: https://nixos.org/community/teams/ngi/
- Project management board: https://github.com/orgs/ngi-nix/projects/8
- Discourse: https://discourse.nixos.org/c/dev/ngi-zero/45
