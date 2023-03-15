# Summer of Nix 2023

## What is Summer of Nix

Summer of Nix is a rare opportunity to collaborate on Nix packaging of open-source software in a supportive environment while being paid.

It's for anyone who desires to develop and share their Nix and software development skills while working together.

As a participant, you join a team and work together remotely within July to October.

## Format

In addition to collaboration on (the work), the 2023 edition also includes a public lecture series and a hiring event.

The program is entirely remote.
Participation will occur exclusively in mob programming format for 20 hours per week.
There will be a public lecture series.
We would like to organize a hiring event at the end.
Work on a monorepo "ngipkgs".

## Goals this year

- improve the deployment story of NGI-funded projects using Nix
- skill-sharing among the participants and beyond
- expand the nix community

- 20 hours per week
- public lectures
- hiring event
- shift from a many-repo strategy to a monorepo "ngipkgs"

## Timeline

2023-04-01: open application window
2023-04-30: close application window
2023-05-15: answer applications
2023-07-17: start of the program
2023-10-13: end of the program (13 weeks after start)
2023-10-31: (maybe) hiring event

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

## Why exclusively mob programming?

=> dropping the project specific track handed over to NixOS Fdt
=> dropping free packaging handed over to NLNet directly

   - consist of four participants and a mob programming facilitator
   - has a regular weekly schedule
   - determines its own agenda and objectives within the scope of the program
Participation in this program involves making decisions, such as what to work on or how to implement something.
Often, which decision is most appropriate is not clear from the information available.
In the past two editions, the organizers were approached with questions more frequently than they were able to respond to.
And even if they were able, they wouldn't necessarily have the answers.
We hope that the mob programming format will [help with decision making](#why-mob-programming).

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




## TODO

- a safe and welcoming environment
- participation of Nix users of all levels

monorepo reasons
  - Primary produce of the Summer of Nix are open-source Nix packages (code, documentation, and deployment stories)
  - Where can these packages currently go?
    - An upstream repository
    - [nixpkgs]() or a fork of it,
    - package-specific repositories under the ngi-nix GitHub organization
    - a yet non-existent monorepo ngi-nix/ngipkgs
  - We feel that a monorepo would serve the best balance between the needs of the users, the developers (participants) and the funding organizations. 
