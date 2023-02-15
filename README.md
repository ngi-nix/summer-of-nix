# Summer of Nix

## Definition

Summer of Nix is a program where participants contribute to Free/open-source projects in the Nix ecosystem.

that roughly takes place in the (northern hemisphere) summer months.
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
- shift from a many-repo strategy to a monorepo "ngipkgs"
  - Primary produce of the Summer of Nix are open-source Nix packages (code, documentation, and deployment stories)
  - Where can these packages currently go?
    - An upstream repository
    - [nixpkgs]() or a fork of it,
    - package-specific repositories under the ngi-nix GitHub organization
    - a yet non-existent monorepo ngi-nix/ngipkgs
  - We feel that a monorepo would serve the best balance between the needs of the users, the developers (participants) and the funding organizations. 

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

## Stipends

Role            | Per role (EUR) 
----------------|----------------
mob facilitator |           5000 
participant     |           3000 
organizer       |           2000 
grand total     |

EU member states all receive the base rate without modification.
Stipend for non-EU countries for any role are adjusted according to [Purchasing Power Parity](https://en.wikipedia.org/wiki/Purchasing_power_parity).
[Google Summer of Code](https://developers.google.com/open-source/gsoc/help/student-stipends)'s stipend system is adopted for this purpose, as shown in this example:

The stipend for a Nepalese participant is the base Summer of Nix stipend multiplied by the ratio of GSoC's Nepalese and Netherlands stipends (amounts sourced [here](https://developers.google.com/open-source/gsoc/help/student-stipends#total_stipend_amount)).
The formula is

```
SoN_Nepal = base_stipend × GSoC_medium_project_Nepal ÷ GSoC_medium_project_Netherlands
          = 3000 EUR × 1500 USD ÷ 2700 USD
          ≅ 1666.67 EUR
```

## Budget


 Total (EUR)
------------
       25000
       60000
        6000
   **91000**Number | 
-------|-
     5 | ## Eligibility
    20 | 
     3 | - Past the age of majority
       | - Basic familiarity with Nix


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

## Questions and answers

- Is this program specifically for experts? – No 
- Is this program specifically for beginners? – No
- How familiar must I be with Nix in order to participate?
- Why are you using GitHub and other proprietary, unfree and closed-source programs? – Because ...
- Why mob programming?
- I am in timezone X. Can I participate?
