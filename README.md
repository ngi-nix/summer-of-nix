---
title: Summer of Nix 2022 Report
classoption:
  - a4paper
  - 11pt
mainfont: DejaVu Serif
sansfont: DejaVu Sans
documentclass: scrartcl
author: The Summer of Nix organization team
geometry: "left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm"
numbersections: true
links-as-notes: true
---

<!--
TODO:

- unify capitalization in section 4
-->

# Summary

This is a short report about Summer of Nix 2022.
To understand the program and its history, we recommend reading the detailed [2021 Report](https://summer.nixos.org/assets/report-2021.pdf).
2021 was the first year in which Summer of Nix was held.
Despite its overall success, it became clear that organizing a group of 30+ developers for three months is a challenge.
The program for the 2022 edition was refined and new forms of organization were experimented with, as described in the [announcement](https://discourse.nixos.org/t/18479).

A prominent addition was the introduction of mentoring by maintainers of participating projects, such as Jitsi's Nix packaging, Nix documentation and dream2nix.
Also new were regular facilitated mob programming sessions.
Participants could also choose to work freely on packages in our main backlog of NGI projects, similar to 2021.
Another change to the program was that the attached Nix lecture series was made public.

The number and quality of contributions compared to the amount of resources invested in the program was satisfactory and there was enthusiasm from the participants.
The public lecture series got a lot of traction beyond Summer of Nix and was a success.

However, with low budget and limited time, coordinating and mentoring of so many developers – many of them junior – remained a challenge.
This left many with the feeling that we could achieve more in the given time.
For example, the packaging of many projects reached almost-completion, which is less than was intended.
Having three different organization forms: free packaging, project-specific mentoring, and mob programming, was confusing to participants.
The latter two forms, being more structured, were more pleasant for participants and more effective.

Overall, it remains our belief that the concept of Summer of Nix, a sponsored program where participants collaborate on Nix packaging of open-source software, is sound.
On the other hand, we intend to refine its implementation.
Work on upcoming solutions/improvments to the challenges mentioned above is ongoing in the planning of Summer of Nix 2023.

# Participation stats

- Total number of applicants: 156
- Total accepted candidates by role:
  - 21 participants
  - 6 tech-wiz's
  - 6 project leads
  - 5 team coordinators
  - 2 tech-wiz's on a waiting list
  - 16 participants on a waiting list
  - 99 declined applications
- Diversity:
  - 1 woman out of 38 accepted participants
  - 5 participants from Central Asia,  
    3 from East Asia,  
    18 from Europe,  
    2 from Middle East,  
    10 from North America
- Actual participants:
  - 4 accepted participants and 1 team coordinator did not participate
  - 5 participants gave up their stipend for various reasons

# Budget

- Stipends paid: 65649 EUR
- Cost of material (mostly cloud servers): 340 EUR
- Grand total of costs: 65 989 EUR

# Summer of Nix 2022 contributions

## Communication (Articles, Videos, Communication)

- New website summer.nixos.org:  
  https://github.com/NixOS/nixos-summer/pull/28
- Blog post on Deploying a simple Jitsi Meet server with NixOS:  
  https://summer.nixos.org/blog/deploying-simple-jitsi-meet-server/
- Talk at NixCon 2022 about Summer of Nix work on Jitsi Meet:  
  https://www.youtube.com/watch?v=-hsxXBabdX0&t=12554s
- Public lectures about Nix
  - A complete playlist:  
    https://youtube.com/playlist?list=PLt4-_lkyRrOMWyp5G-m_d1wtTcbBaOxZk
  - The Evolution of Nix:  
    https://www.youtube.com/live/h8hWX_aGGDc
  - The History of NixOS:  
    https://www.youtube.com/live/t6goF1dM3ag
  - The Architecture and History of Nixpkgs:  
    https://www.youtube.com/live/TKgHazs3AMw
  - Flattening the Learning Curve:  
    https://www.youtube.com/live/WFRQvkfPoDI
  - Nix Is Going Mainstream:  
    https://www.youtube.com/live/WuWZqSSoLxY
  - Hydra, Nix's CI:  
    https://www.youtube.com/live/AvOqaeK_NaE
  - Nix/Guix and Reproducible Science:  
    https://www.youtube.com/live/SjjEDTccpQA
  - Nix × IPFS Gets a New Friend: SWH:  
    https://www.youtube.com/live/DjJyPzwEzmU
  - The Significance of Reproducible Software in International R&D:  
    https://www.youtube.com/live/TM5zpCn4piM
  - Real World DevOps with Nix:  
    https://www.youtube.com/live/LjyQ7baj-KM
  - The Road to Nix at Replit:  
    https://www.youtube.com/live/jhH2LWGUHhY
  - State of Nix at European Commission:  
    https://www.youtube.com/live/I7wdcJ3YhoU

## Nix documentation

- Discourse: What does “warning: Git tree ‘/a/path’ is dirty” mean exactly?  
  https://discourse.nixos.org/t/20568
- Discourse: `rev` and `ref` attributes in `builtins.fetchGit` (and maybe flakes too?)  
  https://discourse.nixos.org/t/20588
- Discourse: How to build the Nix manual? (not the Nix man pages)  
  https://discourse.nixos.org/t/20508
- Discourse: Ideas to make it easier to contribute to the documentation  
  https://discourse.nixos.org/t/20312
- Discourse: Building RISC-V Phone’s Firmware, where is riscv64-unknown-elf-gcc?  
  https://discourse.nixos.org/t/20578
- Discourse: Move script from flake into its own file  
  https://discourse.nixos.org/t/21158
- Discourse: Hydra, hash and inputs  
  https://discourse.nixos.org/t/21133
- Discourse: readFile doesn’t find file  
  https://discourse.nixos.org/t/21103
- Discourse: Usability studies + linked user studies  
  https://discourse.nixos.org/t/21404
- Discourse: OpenGL issues on non-NixOS nix  
  https://discourse.nixos.org/t/3
- Discourse: "Nix overlays: the fixpoint and the (over)layer cake" by @Layus  
  https://discourse.nixos.org/t/20694
- Discourse: What “scope” do “package mechanisms” apply to?  
  https://discourse.nixos.org/t/20745

- https://github.com/NixOS/nixpkgs/pull/183761
- GitHub (comment): `NixOS/nix` issue #5128  
  https://github.com/NixOS/nix/issues/5128#issuecomment-1198254451
- GitHub (comment): i18n #6842  
  https://github.com/NixOS/nix/issues/6842#issuecomment-1210057729
- GitHub (gist): Re-imagining the documentation for Nix's `builtins.fetchGit` (that could serve as a template for other function docs)  
  https://gist.github.com/toraritte/ee35da9aadca4c4cf18b39d864cd5f8a
- GitHub (issue): `nix-community/wiki` issue #43: question Where to raise questions when it comes to content organization?  
  https://github.com/nix-community/wiki/issues/43
- GitHub (review): Document what Nix *is* #6420  
  https://github.com/NixOS/nix/pull/6420
- GitHub (review): Greatly expand architecture section, including splitting into abstract vs concrete model #6877  
  https://github.com/NixOS/nix/pull/6877
- GitHub (review): doc/manual: define {local,remote} store, binary cache, substituter PR#6870  
  https://github.com/NixOS/nix/pull/6870

- NixOS wiki edits  
  https://gist.github.com/toraritte/31a40a00f8efff6febfe64c2c1251950

- Stackoverflow: How do Git revisions and references relate to each other?  
  https://stackoverflow.com/questions/73145810

## Nix tooling

### dream2nix

- https://github.com/nix-community/dream2nix/pull/228
- https://github.com/nix-community/dream2nix/pull/283
- https://github.com/nix-community/all-cabal-json/pull/3
- https://github.com/nix-community/dream2nix/pull/227
- https://github.com/nix-community/dream2nix/pull/229
- https://github.com/nix-community/dream2nix/pull/236
- https://github.com/nix-community/dream2nix/pull/239
- https://github.com/nix-community/dream2nix/pull/248
- https://github.com/nix-community/dream2nix/pull/256
- https://github.com/nix-community/dream2nix/pull/271
- https://github.com/nix-community/dream2nix/pull/311
- https://github.com/nix-community/dream2nix/pull/312
- https://github.com/nix-community/dream2nix/pull/317
- https://github.com/nix-community/dream2nix/pull/328
- https://github.com/nix-community/dream2nix/pull/257
- https://github.com/nix-community/dream2nix/pull/212
- https://github.com/nix-community/dream2nix/pull/274
- https://github.com/nix-community/dream2nix/pull/301
- https://github.com/nix-community/dream2nix/pull/315
- https://github.com/nix-community/dream2nix/pull/314
- https://github.com/nix-community/dream2nix/pull/317
- https://github.com/nix-community/dream2nix/pull/319
- https://github.com/nix-community/dream2nix/pull/328
- PHP ecosystem support:
  - https://github.com/nix-community/dream2nix/pull/258
  - https://github.com/nix-community/dream2nix/pull/262
  - https://github.com/nix-community/dream2nix/pull/286
  - https://github.com/nix-community/dream2nix/pull/296
  - https://github.com/nix-community/dream2nix/pull/297
  - https://github.com/nix-community/dream2nix/pull/300
- https://github.com/nix-community/dream2nix/pull/252
- https://github.com/nix-community/dream2nix/pull/263
- https://github.com/nix-community/dream2nix/pull/284
- https://github.com/nix-community/dream2nix/pull/287
- https://github.com/nix-community/dream2nix/pull/290
- https://github.com/nix-community/dream2nix/pull/294
- https://github.com/nix-community/dream2nix/pull/298
- https://github.com/nix-community/dream2nix/pull/302
- https://github.com/nix-community/dream2nix/pull/304
- https://github.com/nix-community/dream2nix/pull/308
- https://github.com/nix-community/dream2nix/pull/321
- https://github.com/nix-community/dream2nix/pull/323

### microvm.nix

- https://github.com/NixOS/nixpkgs/pull/187177
- https://github.com/NixOS/nixpkgs/pull/186473
- https://github.com/NixOS/nixpkgs/pull/185981
- https://github.com/NixOS/nixpkgs/pull/186328
- crosvm tap network interface support
- PCI/USB device passthrough
- Enhanced documentation  
  https://astro.github.io/microvm.nix/conventions.html
- Can now optionally use hypervisors from the host's nixpkgs for security
- Support for **erofs** bootDisks
- Serial console support
- A reusable Flake to run NixOS MicroVMs on Hyperconverged
  Infrastructure using NixOS/GlusterFS/Nomad:
  Skyflake  
  https://github.com/astro/skyflake

## NGI Packages

### castopod-host

- https://github.com/ngi-nix/castopod-host/pull/1
- https://github.com/ngi-nix/castopod-host/pull/2

### katzenpost

- https://github.com/ngi-nix/katzenpost/pull/2

### node-Tor

- https://github.com/ngi-nix/node-Tor/pull/1

### scion-path-discovery

- https://github.com/ngi-nix/scion-path-discovery/pull/2

### Lemmy:

- https://github.com/NixOS/nixpkgs/pull/182251
- https://github.com/NixOS/nixpkgs/pull/182371
- https://github.com/NixOS/nixpkgs/pull/182441
- https://github.com/NixOS/nixpkgs/pull/183613
- https://github.com/jhass/nodeinfo/pull/58

### vg:

- https://github.com/ngi-nix/magic_rb-vg/pull/1

### hyperspace:

- https://github.com/ngi-nix/hyperspace

### kaitaistruct, kaitai-struct-compiler

- https://github.com/NixOS/nixpkgs/pull/182154

### ngx-http-auth-sasl-module

- https://github.com/stef/ngx_http_auth_sasl_module/pull/2

### ARPA 2

- https://github.com/NixOS/nixpkgs/pull/184588

### Dino

- https://github.com/NixOS/nixpkgs/pull/181929
- https://github.com/NixOS/nixpkgs/pull/185173

### Ocaml-dns, cmdliner updates

- https://github.com/NixOS/nixpkgs/pull/184394

### BANG

- https://github.com/armijnhemel/binaryanalysis-ng/pull/330

### proximity_matcher_webservice (for BANG)

- https://github.com/armijnhemel/proximity_matcher_webservice/pull/2
- https://github.com/armijnhemel/proximity_matcher_webservice/pull/3

### univers (for BANG)

- https://github.com/nexB/univers/pull/77
- https://github.com/nexB/univers/pull/78

### flare-floss (for BANG)

- https://github.com/NixOS/nixpkgs/pull/182814

### Nitrokey

- https://github.com/NixOS/nixpkgs/pull/183099
- https://github.com/ngi-nix/nitrokey-firmware/pull/1

### ChipWhisperer:

- https://github.com/newaetech/chipwhisperer/pull/415
- https://github.com/ngi-nix/chipwhisperer/pull/3

### ocaml-fsq

- https://github.com/p2pcollab/ocaml-fsq/pull/3
- https://github.com/ngi-nix/p2pcollab-ocaml-fsq

### sbws

- https://github.com/ngi-nix/sbws-flake/pull/1

### Fractal

- https://github.com/ngi-nix/fractal

### Sylk Server

- https://github.com/NixOS/nixpkgs/pull/188018
- https://github.com/NixOS/nixpkgs/pull/188021
- https://github.com/NixOS/nixpkgs/pull/188015
- https://github.com/NixOS/nixpkgs/pull/187995

### ocaml-psi

- https://github.com/ngi-nix/p2pcollab-ocaml-psi

### Cryptolyzer

- https://github.com/ngi-nix/cryptolyzer
- https://github.com/NixOS/nixpkgs/pull/185456

### Sipexer

- https://github.com/NixOS/nixpkgs/pull/185278

### StreetComplete

- https://github.com/ngi-nix/StreetComplete

### JShelter

- https://github.com/ngi-nix/jshelter

### LiberaForms

- https://github.com/ngi-nix/liberaforms-flake
- https://gitlab.com/liberaforms/liberaforms/-/merge_requests/320

### Goblins

- https://github.com/NixOS/nixpkgs/pull/188250

### GNU SASL
- https://github.com/NixOS/nixpkgs/pull/186893

### Blink

- https://github.com/ngi-nix/blink/pull/1

### opaque-sphinx

- https://github.com/ngi-nix/opaque-sphinx/pull/4

### EgilSCIM

- https://github.com/ngi-nix/EgilSCIM/commit/74781d

### Bloomf

- https://github.com/p2pcollab/bloomf/pull/2

### plotkicadsch

- https://github.com/NixOS/nixpkgs/pull/189045

### riscv-phone

- https://github.com/ngi-nix/riscv-phone
- https://github.com/ngi-nix/riscv-phone/pull/8

### EteSync

- https://github.com/ngi-nix/etesync-ios

### re-Isearch

- https://github.com/NixOS/nixpkgs/pull/182120

### GNU Taler

- https://github.com/NixOS/nixpkgs/pull/182139

### SCION

- https://github.com/ngi-nix/scion/pull/5

### redwax

- https://github.com/NixOS/nixpkgs/pull/188060

### luna-pnr

- https://github.com/ngi-nix/LunaPnR-flake/pull/1

### Jitsi Meet

- Update of components to latest stable versions, fix of one update script:  
  https://github.com/NixOS/nixpkgs/pull/185033
- Vosk speech recognition service:  
  https://github.com/NixOS/nixpkgs/pull/186917/
- Vosk compatibility fixes for Jigasi:  
  https://github.com/NixOS/nixpkgs/pull/137003#pullrequestreview-1082232106
- Deployment Story:  
  https://github.com/NixOS/nixos-summer/pull/36
- Fix version order bug in all update scripts:  
  https://github.com/NixOS/nixpkgs/pull/197207
- Second update of components to latest stable versions:  
  https://github.com/NixOS/nixpkgs/pull/198303

### Nyxt

- https://github.com/NixOS/nixpkgs/pull/185975

### mobile-nixos

- Development Story:  
  https://collinarnett.me/Mobile%20NixOS%20Development.html
- In progress calamares extension:  
  https://github.com/ngi-nix/mobile-nixos-calamares-extension

### vframe

- https://github.com/ngi-nix/vframe/tree/nix-integration

### etherpad

- In progress nixos module:  
  https://github.com/ngi-nix/etherpad-nix

### Milagro-crypto-js

- https://github.com/ngi-nix/ngi/issues/196

### Milagro-dta

- https://github.com/ngi-nix/ngi/issues/196

### LibrEDA (in progress)

- https://github.com/ngi-nix/libreda

### PeerTube

- https://github.com/NixOS/nixpkgs/pull/191494
- https://github.com/NixOS/nixpkgs/pull/191497

### Misskey

- https://github.com/ngi-nix/misskey-d2n

### Supermin

- https://github.com/ngi-nix/supermin

## Ecosystem

### PRoot

- Fix unsupported syscall breaking nix installer on current kernels:  
  https://github.com/proot-me/proot/pull/338
