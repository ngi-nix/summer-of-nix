# Summer of Nix 2023

Summer of Nix is a rare opportunity for Nix users of varying skills and interests,
to practice Nix remotely,
in a format that emphasizes knowledge sharing,
sustainable practice, and quality of product,
while contributing to open source _and_ receiving [(some) payment](#stipends-payment) for it.

The 2023 edition also has [public talks](#public-talks)
and a life-changing [hiring event](#hiring-event).

Summer of Nix 2023 takes place between July and October 2023.

## Goals

Summer of Nix is sponsored by a [Next Generation Internet (NGI)](https://www.ngi.eu/) grant
through the [NLNet Foundation](https://nlnet.nl/) and the NixOS Foundation
to:

- improve the deployment story of NGI-funded projects (using Nix, of course)
- skill share among the participants
- expand and enrich the Nix community

## The main activity

The main activity for achieving our [goals](#goals) is remote mob programming,
mostly [as described here][remote mob programming].
Participants organize into mobs —
collaboration groups of between five and seven each,
and work 20 hours a week during the program.
Each mob is joined by a facilitator —
an experienced developer who is familiar with mob programming.

## Stipends (payment)

The stipends for Summer of Nix 2023 are as follows:

|                  | Participant | Facilitator | Organizer |
|------------------|-------------|-------------|-----------|
| Base stipend EUR |        3000 |        5000 |      2000 |

Residents of EU member states receive the base stipend without modification.
For residents of other countries an adjustment applies
according to [purchasing power parity] relative to the Netherlands,
derived via [Google Summer of Code's stipend system].

For calculated rates, see [this spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vScs76kD8qJinBAMWX_rRD9Gxu9YbSZmutQhd4UCw7oN3iyVVHFDtAlB5tMKUba-8P6KsFLrcFQGSaJ/pubhtml).

[purchasing power parity]: https://en.wikipedia.org/wiki/Purchasing_power_parity
[Google Summer of Code's stipend system]: https://developers.google.com/open-source/gsoc/help/student-stipends

## Timeline

| Date       |                               |
| ---------- | ------------------------------| 
| 2023-04-01 | application window opens      |
| 2023-04-30 | application window closes     |
| 2023-05-15 | application responses sent    |
| 2023-07-17 | program begins                |
| 2023-10-13 | program ends (after 13 weeks) |
| 2023-10-31 | hiring event                  |

## Eligibility

Applicants should

 - be past the age of majority
 - have fluent English
 - posess at least "junior" programming skills
 - have basic familiarity with Nix
 - meet the [technical requirements](#technical-requirements)

## Technical requirements

…for participation in [remote mob programming] throughout the program.

- internet connection suitable for hours of ongoing video call
  - stable (mobile broadband unlikely to satisfy this)
  - sufficient bandwidth
- computer capable of doing work while sharing screen in a video call
  - a CPU with CPU mark of 7,000 and single thread rating of 1,900
    [according to PassMark](https://www.cpubenchmark.net/cpu_list.php)
    should suffice.
  - video camera
  - headphones and reasonable quality microphone
- consistently low noise environment

Please use a friend to make a test [Jitsi Meet](https://meet.jit.si/) call,
including video, audio and __entire screen__ sharing.
Ask your friend whether they can see your screen and hear you well
while you are [stressing your CPU](https://silver.urih.com/).

## How to apply

Fill [the application form][application form].

[application form]: https://baserow.io/form/HgVDOqCbHh5fWP1Tguu9DBpXmQzBA6WJv-zKbXnmAOk

## How to prepare

1. Read http://remotemobprogramming.org/.
1. Make a test [Jitsi Meet](https://meet.jit.si/) call with a friend
   and use it to test video, audio and entire screen sharing.
1. Familiarize yourself with the [mob command line utility](https://mob.sh/).
1. Have [`git` is set up to authenticate with GitHub](https://docs.github.com/en/get-started/quickstart/set-up-git).
1. Have [direnv](https://direnv.net/) or equivalent, both;
   1. [installed](https://direnv.net/docs/installation.html)
   1. and [set up in your shell](https://direnv.net/docs/hook.html).
1. Configure [two-factor authentication for your GitHub account](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication).

## Questions and answers

### Why mob programming?

The mob programming format optimizes for knowledge sharing.
This seems appropriate for short-lived teams
working on a series of unfamiliar projects.

Also, in the past two editions,
a significant bottleneck was the ogranizers' time.
With mob programming, we hope to reduce the load on organizers
by maximizing cross-participant collaboration.

Co-organizer [Dawn][Shahar "Dawn" Or], having been
organizing and participating in regular mob programming sessions since 2021
and having facilitated mob programming sessions in the [last year's edition](#2022),
is convinced that the format — with proper facilitation —
is absent many collaboration problems prevalent in solo-programming,
and overall produces better software, more sustainably.

Co-organizer [Matthias][Matthias Meschede] is optimistic about this premise and feels that holding this year's edition in mob programming format is a valuable experiment.

### Is this program specifically for beginners?

We intend to have participants of varying levels of experience.

### How familiar must I be with Nix?

Do you use NixOS?
Do you use Nix shell?
Do you use home-manager?
Did you make a derivation?
If you answered yes to any, you qualify.

### Why does this NGI sponsored program use this or that software?

We do our best to select open source and [zero-knowledge] software.
But those are not hard constraints,
nor are they the only factors to consider.

We use:

- [Baserow](https://baserow.io/)
- [GitHub](https://github.com/)
- [Matrix](https://matrix.org/)

[zero-knowledge]: https://en.wikipedia.org/wiki/Zero-knowledge_service

### Are participants from all timezones eligible?

Yes.

## Public discussion

In [this category](https://discourse.nixos.org/c/45).

## Organizers

Feel free to message us for private concerns.

- [Matthias Meschede]
- [Shahar "Dawn" Or]

<!-- URLs -->

[remote mob programming]: https://www.remotemobprogramming.org/
[son-2021-report]: https://summer.nixos.org/assets/report-2021.pdf
[Matthias Meschede]: https://mmesch.com/
[Shahar "Dawn" Or]: https://github.com/mightyiam
