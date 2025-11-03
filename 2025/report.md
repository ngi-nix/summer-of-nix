---
title: Summer of Nix 2025
subtitle: Program report
author:
- Fedi Jamoussi
- Ivan Minčík
- Daniel Ramírez
date:
geometry: a4paper, margin=1.5in
linestretch: 1.05
numbersections: true
colorlinks: true
...

Summer of Nix is a coordinated effort to support free and open source
software (FOSS) projects that are funded by the European Commission's
[Next Generation Internet (NGI)](https://www.ngi.eu/about/) initiative through
the [NGI0](https://nlnet.nl/NGI0/) consortium coordinated by the
[NLnet Foundation](https://nlnet.nl/foundation/).

The program's main objective is to make more software available as Nix packages
or NixOS service modules. This is in order to make the projects developed
under NGI0 easier to obtain and run – something that is not a given due to the
complexities involved in software development – and thus help end users and
developers to reap the benefits of the public funding campaign. Nix itself is
a proven technology for highly repeatable software builds and deployments, and
supports an ecosystem of tools for building a fully transparent software supply
chain.

Packaging artefacts for supported open source projects are collected in
[NGIpkgs Git Repository](https://github.com/ngi-nix/ngipkgs/) and presented via
[NGIpkgs Overview Web Interface](https://ngi.nixos.org/).

This year, the team was newly formed to sustain packaging and maintenance effort
with a [kickoff meeting on Jan 13th](https://www.notion.so/NGI-2025-Kickoff-meeting-0b27164d3e3449498d0bbf4836102fca?pvs=21).
Long term [goals](https://github.com/orgs/ngi-nix/projects/8/views/14) were set using
[OKR framework](https://en.wikipedia.org/wiki/Objectives_and_key_results).
In addition to packaging work itself, the team has focused on redefining the NGI
package content and design (package deliverables), packaging quality, tasks
and project management and automation in order to provide the best possible
contributor and user experience.


# Summary

- Activities from January 2025 to November 2025
- Team's role and gender distribution (after [UN M49 standard](https://en.wikipedia.org/wiki/UN_M49))

![](./M49_team-distribution.pdf)

## Expenses

| Cost Category      | Amount [€] |
|:-------------------|-----------:|
| Paid (in balance)  | 82 200     |
| Pending invoices   | 17 600     |
| Allocated budget   | 55 800     |
| Travel expenses    |  3 100     |
| **Total**          |**158 700** |

- Time worked: 3 900 h
- Average compensation: 26.50 EUR/h

## Packaging work

The following software projects where packaged:

| Project | Funds |
|:--------|:------|
[0WM](https://ngi.nixos.org/project/0WM) | Core: 1
[Arcan](https://ngi.nixos.org/project/Arcan) | Core: 2, Entrust: 1
[Blink](https://ngi.nixos.org/project/Blink) | Entrust: 1, Review: 2
[Briar](https://ngi.nixos.org/project/Briar) | Review: 2
[Corteza](https://ngi.nixos.org/project/Corteza) | Review: 3
[CryptoLyzer](https://ngi.nixos.org/project/CryptoLyzer) | Core: 1, Review: 1
[Draupnir](https://ngi.nixos.org/project/Draupnir) | Core: 1
[ERIS](https://ngi.nixos.org/project/ERIS) | Review: 1
[Galene](https://ngi.nixos.org/project/Galene) | Core: 1
[Gnucap](https://ngi.nixos.org/project/Gnucap) | Commons: 1, Entrust: 2
[Heads](https://ngi.nixos.org/project/Heads) | Review: 2
[Inventaire](https://ngi.nixos.org/project/Inventaire) | Entrust: 1, Review: 2
[Irdest](https://ngi.nixos.org/project/Irdest) | Core: 1, Entrust: 2, Review: 1
[Kaidan](https://ngi.nixos.org/project/Kaidan) | Commons: 1, Entrust: 1, Review: 4
[Kazarma](https://ngi.nixos.org/project/Kazarma) | Entrust: 1, Review: 1
[Keyoxide](https://ngi.nixos.org/project/Keyoxide) | Review: 4
[Liberaforms](https://ngi.nixos.org/project/Liberaforms) | Commons: 1, Review: 2
[LibreSOC](https://ngi.nixos.org/project/LibreSOC) | Entrust: 2, Review: 6
[Librecast](https://ngi.nixos.org/project/Librecast) | Commons: 1, Core: 1, Review: 2
[MarginaliaSearch](https://ngi.nixos.org/project/MarginaliaSearch) | Core: 1, Entrust: 1
[Mastodon](https://ngi.nixos.org/project/Mastodon) | Commons: 1, Entrust: 1, Review: 1
[Mox](https://ngi.nixos.org/project/Mox) | Core: 1, Entrust: 1, Review: 1
[Namecoin](https://ngi.nixos.org/project/Namecoin) | Review: 5
[Nitrokey](https://ngi.nixos.org/project/Nitrokey) | Commons: 2, Entrust: 1, Review: 1
[NodeBB](https://ngi.nixos.org/project/NodeBB) | Commons: 1, Core: 1
[Nominatim](https://ngi.nixos.org/project/Nominatim) | Entrust: 1, Review: 1
[Openfire](https://ngi.nixos.org/project/Openfire) | Core: 2
[PagedJS](https://ngi.nixos.org/project/PagedJS) | Commons: 1
[Re-Isearch](https://ngi.nixos.org/project/Re-Isearch) | Commons: 1, Review: 1
[ReOxide](https://ngi.nixos.org/project/ReOxide) | Entrust: 1
[Repath-Studio](https://ngi.nixos.org/project/Repath-Studio) | Commons: 1
[SCION](https://ngi.nixos.org/project/SCION) | Core: 4, Entrust: 1, Review: 3
[Seppo](https://ngi.nixos.org/project/Seppo) | Entrust: 1
[Tau](https://ngi.nixos.org/project/Tau) | Core: 1
[Teamtype](https://ngi.nixos.org/project/Teamtype) | Core: 1
[ThresholdOPRF](https://ngi.nixos.org/project/ThresholdOPRF) | Entrust: 1, Review: 3
[Wax](https://ngi.nixos.org/project/Wax) | Core: 1
[Wireguard](https://ngi.nixos.org/project/Wireguard) | Entrust: 2, Review: 5
[holo](https://ngi.nixos.org/project/holo) | Core: 1
[jaq](https://ngi.nixos.org/project/jaq) | Commons: 1, Entrust: 1
[kbin](https://ngi.nixos.org/project/kbin) | Entrust: 2
[nyxt](https://ngi.nixos.org/project/nyxt) | Entrust: 1, Review: 2
[oku](https://ngi.nixos.org/project/oku) | Entrust: 1
[openXC7](https://ngi.nixos.org/project/openXC7) | Entrust: 1
[owasp](https://ngi.nixos.org/project/owasp) | Core: 1, Review: 1
[owi](https://ngi.nixos.org/project/owi) | Commons: 1, Core: 1
[proximity-matcher](https://ngi.nixos.org/project/proximity-matcher) |
[slipshow](https://ngi.nixos.org/project/slipshow) | Commons: 1
[stalwart](https://ngi.nixos.org/project/stalwart) | Core: 1, Entrust: 1
[verso](https://ngi.nixos.org/project/verso) | Core: 2, Review: 2
[xrsh](https://ngi.nixos.org/project/xrsh) | Entrust: 1
[y-crdt](https://ngi.nixos.org/project/y-crdt) | Commons: 1, Entrust: 1

## Additional metrics

In the NGIpkgs repository, the team is maintaining

- 47 services and 55 programs
- 30 projects with demo available
- 97 NixOS tests, associated with 97 examples
- 80 derivations, 59 of which have an explicit update script

Funded by the following subgrants

- 16 Commons
- 38 Core
- 64 Entrust
- 102 Review

In the upstream Nixpkgs repository, the NGI team is maintaining 131 derivations, 107 of
which have explicit update scripts.

## Non-packaging work

In addition to packaging work, the following additional work was done:

- Designed and implemented a new
  [NGI project schema](https://github.com/ngi-nix/ngipkgs/blob/main/maintainers/docs/project.md)
  for metadata and deliverables with type checking support using the NixOS
  module system

- Improved project and deliverable tracking with
  [issue templates](https://github.com/ngi-nix/ngipkgs/issues/new/choose)

- Implemented demos for programs and services as a practical way to showcase
  projects

- Implemented update script support and bulk updates support

- Implemented multiple improvements to the UI/UX of the project
  [overview page](https://ngi.nixos.org/) such as:
  - implementation of website generation using NixOS modules
  - implementation of metadata, deliverables, demo and demo instructions sections
  - implementation of code snippets, with copy-paste and download buttons
  - implementation of highlighting of missing deliverables, such as programs,
    services, or demos, with links to implement them
  - implementation of breadcrumbs and dark mode
  - addition of usage instructions for multiple Linux distributions

- Implemented significant improvements of tasks and project management
  [tools](https://github.com/orgs/ngi-nix/projects/8)
  and processes (planning, backlog grooming and review sessions)

- Provided support for integration of Nix based development environments to
  upstream source code bases of NLnet funded software

- Provided regular weekly NGI team office hours for public audience

- Joined [Outreachy](https://www.outreachy.org/) program
  (1 mentor from the core team and 1 Outreachy mentee)

- Participated in NixCon conference and gave multiple talks


# Evaluation

After the team was newly established early this year, it took us considerable
time to properly scope our work and settle on suitable project and task
management methods and suitable assignment of tasks to full-time and part-time
team members. Also, in the chase for maximum efficiency, we suffered from
premature attempts to automate our processes which didn't give us the expected
results.

Nevertheless, this year's results are very positive. We have packaged
significantly more software than last year (57 projects compared to 35 in 2024,
representing a 63% increase) with higher quality. Each package now includes
better documentation, tests, and demos. The packaging effort was more consistent
throughout the year, and thanks to improved task management, we were able to
focus on high-priority software projects.


# Future plans

In addition to continued software packaging and maintenance effort, we want to
significantly improve our user feedback loop, which in turn will allow us to
improve our product.

We also want to strengthen collaboration with upstream projects by encouraging
adoption of Nix-based development environments and packaging best practices. This
will help ensure that NGI-funded projects remain easily installable and deployable
long after initial funding ends, maximizing the return on public investment in
open source innovation.
