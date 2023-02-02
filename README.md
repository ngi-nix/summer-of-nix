# Summer of Nix

## Definition

<!-- Summer of Nix is an annual -->

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

## Rates and budget

Role            | Number | Base Rate (EUR/h) | Hours | Per role (EUR) | Total (EUR)
----------------|--------|-------------------|-------|----------------|------------
mob facilitator |      5 |                25 |   200 |           5000 |       25000
participant     |     20 |                15 |   200 |           3000 |       60000
organizer       |      3 |                20 |   100 |           2000 |        6000
grand total     |        |                   |       |                |   **91000**

The actual rate is calculated based on Purchasing Power Parity with respect to the Netherlands, as stated by [Google's Summer of Code](https://developers.google.com/open-source/gsoc/help/student-stipends). The exception are EU member states that all have the base rate.

As example, let's compute the stipend:

The 2023 GSoC medium project stipend for a Nepalese participant is 1500 USD ([Google's Summer of Code](https://developers.google.com/open-source/gsoc/help/student-stipends#total_stipend_amount)).
This is 55% (1500/2700) of the equivalent Netherland stipend.



## Eligibility

- Past the age of majority
- Basic familiarity with Nix
- Fluent in English
- Equipment and means to participate in mob programming sessions
  - internet connection that is reliable and fast enough for long video sessions
  - ability to use all tools mentioned in the How to prepare for mob programming section

## How to apply

We will open an application form on March 1st and you can apply until March 31th (Anywhere on Earth).
Decisions will be taken in the following 2 weeks.

## How to prepare for the mob programming sessions

If you need help with preparation, ask for help [here](TODO)  anything, feel free to message me. Please arrive prepared at your first session.

1. Read http://remotemobprogramming.org/.
1. Make a test [Jitsi Meet](https://meet.jit.si/) call with a friend and use it to test video, audio and screen sharing, entire screen.
1. Install the [mob command line utility](https://mob.sh/).
1. Test that [`git` is set up to authenticate with GitHub](https://docs.github.com/en/get-started/quickstart/set-up-git).
1. Have [direnv](https://direnv.net/) or equivalent both;
   1. [installed](https://direnv.net/docs/installation.html)
   1. and [set up in your shell](https://direnv.net/docs/hook.html).
1. Configure [two-factor authentication for your GitHub account](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication).

## Specific project ideas for Summer of Nix 2023

- write a deployment story for one package in the NLNet list. 
- reunite all independent repositories in the ngi-nix GitHub org into a monorepo “ngipkgs”, similar to https://github.com/nix-community/NUR .

## Questions and answers

- Is this program specifically for experts? – No 
- Is this program specifically for beginners? – No
- How familiar must I be with Nix in order to participate?
- Why are you using GitHub and other proprietary, unfree and closed-source programs? – Because ...
- Why mob programming?
- I am in timezone X. Can I participate?
