# Summer of Nix

## Definition

<!-- Summer of Nix is an annual -->

- program

Summer of Nix is a three month train & work program that roughly takes place in the (northern hemisphere) summer months.
It is made for anyone who wants to rapidly increase their Nix skills while doing useful work for the Nix and the wider FOSS community.
As participant you join a remote team and get paid a nice stipend.

## Goals

- improve the deployment story of NGI-funded projects using Nix
- skill-sharing among the participants and beyond 
- expand the nix community

## Strategies

- a safe and welcoming environment
- participation of Nix users of all levels
- mob programming
- public lectures
- hiring event

## Timeline

2023-04-01: open application window
2023-04-30: close application window
2023-05-15: answer applications
2023-07-17: start of the program
2023-10-13: end of the program (13 weeks after start)
2023-10-31: (maybe) hiring event

## Format

The program is entirely remote.

Contribution toward improvement of deployment stories ("the work") occurs in the context of mob programming groups ("mobs").

Each mob:

- consist of four participants and a mob programming facilitator
- has a regular weekly schedule
- determines its own agenda and objectives within the scope of the program

### Roles, rates and budget

Role            | Number | Rate (EUR/h) | Hours | Per role (EUR) | Total (EUR)
----------------|--------|--------------|-------|----------------|------------
mob facilitator |      5 |           25 |   200 |           5000 |       25000
participant     |     20 |           15 |   200 |           3000 |       60000
organizer       |      3 |           20 |   100 |           2000 |        6000
grand total     |        |              |       |                |   **91000**

## How to prepare for the mob programming sessions

If you need help with preparation, ask for help [here](TODO)  anything, feel free to message me. Please arrive prepared at your first session.

# General

1. Read http://remotemobprogramming.org/.
1. Make a test [Jitsi Meet](https://meet.jit.si/) call with a friend and use it to test video, audio and screen sharing, entire screen.
1. Install the [mob command line utility](https://mob.sh/).
1. Test that [`git` is set up to authenticate with GitHub](https://docs.github.com/en/get-started/quickstart/set-up-git).
1. Have [direnv](https://direnv.net/) or equivalent both;
   1. [installed](https://direnv.net/docs/installation.html)
   1. and [set up in your shell](https://direnv.net/docs/hook.html).
1. Configure [two-factor authentication for your GitHub account](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication).

# Rust

1. Test that you have [a recent version of Rust installed](https://www.rust-lang.org/tools/install) and you are able to [compile a dummy project](https://doc.rust-lang.org/book/ch01-02-hello-world.html). Tip: installing Rust on Windows takes considerably more time than on other operating systems.
1. Set up [support for Rust in your editor](https://code.visualstudio.com/docs/languages/rust).

 - GitHub for code and documentation
 - Matrix for chat
 - Jitsi for video conferencing and screen share

Be ready for entire screen sharing so that you could quickly show terminal,
browser. A second screen is handy for privacy purposes but not required.


## Project ideas for Summer of Nix 2023

- reunite all independent repositories in the ngi-nix GitHub org into a monorepo “ngipkgs”, similar to https://github.com/nix-community/NUR .


<!--
Activities: work / learn / meet
Timesheets: 30% active coding / 30% active learning / 30% active meeting

I spent Monday, Tuesday working on issue X, on Wednesday I read about flakes, on Thursday I participated in a discussion in the Nix discourse and on Friday I learned about NixOps. => acceptable

I spent weeks 1-4 reading about flakes and in the Nix manual. => tell the person to contribute something in the form of code and maybe participate in community discussions.

I worked weeks 1-4 alone on packaging A,B,C,D,E,F,G. => the goal of summer of nix is to share knowledge ....
-->
