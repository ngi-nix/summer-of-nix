# Summer of Nix 2024

Summer of Nix is a coordinated effort to support selected free and open source software (FOSS) projects, by making them available as [Nix packages](https://search.nixos.org/packages) or [NixOS service modules](https://search.nixos.org/options?query=services).
It is funded by the European Commission's [Next Generation Internet (NGI)](https://www.ngi.eu/) initiative through the [NLNet Foundation](https://nlnet.nl/) and the [NixOS Foundation](https://github.com/NixOS/foundation).

This northern-hemisphere-summer program is a rare opportunity for students or early-career professionals with diverse technical skills and interests to practice disciplined software development with Nix while contributing to the public good and receiving some payment for it.
Participation in Summer of Nix has been – for some – a pathway to attractive jobs in software development.

Learn more about Nix on [nix.dev](https://nix.dev/).

## Goals

The program is designed for participants to **work, learn, and meet**:

- Improving the deployment story of [software projects funded by the NLnet Foundation](https://nlnet.nl/project/)

  Just writing the code is not enough: Programs have to be easy to obtain and run to be widely adopted.
  Getting complex software to work reliably on a whim is the aspiration for Summer of Nix.

  As a participant, you will write Nix derivations, NixOS modules, integration tests, and documentation.
  And you will solve a lot of tricky problems on the way.

- Skill-sharing among participants

  Making computers useful for a mass audience requires diverse skills and broad knowledge, and no one person has it all.

  As a participant, you will learn from – and teach – your peers about widely used programming languages, software testing, technical writing, web design, and the Nix ecosystem with various its tools.
  You will closely collaborate in a group of five people on a regular schedule.

- Growing the Nix community

  As a participant, you will join a community of [more than 700 active contributors](https://github.com/NixOS/nixpkgs/pulse/monthly).
  You will engage in an open source software development workflow and take part in public technical discussion.

  After successful participation, you will be invited to NixCon 2024, a conference for Nix users and developers from all over the world.
  And you will be afforded an opportunity for exposure with potential employers for whom Nix is a core strength.

## Mob programming

As a participant, you will be in one of several teams working in [remote mob programming format](https://www.remotemobprogramming.org/).
To ensure successful collaboration, each team includes a facilitator – a more experienced developer who is familiar with mob programming.

The teams will be supported by a resident developer and the program organisers.

## Timeline

- March: Organisers recruit facilitators
- April: Facilitators recruit mob members
- Late May to early September: Mobs work

## Applications

Mob programming facilitators are recruited by the organisers.
The [call for facilitator applicatons](./facilitators.md) is open until 2024-03-24.

Each facilitator sets their mob's schedule and, in turn, recruits four members for their mob.
We will publish a call for participant applications in April 2024.

## Eligibility

People from anywhere in the world can apply.
To be considered for participation, applicants must:

 - Be a natural person of legal age
 - Be fluent in English
 - Have essential programming skills, including proficiency with
   - The command line
   - Git version control
   - At least one programming language
 - Have basic familiarity with Nix
 - Meet the [technical requirements](#technical-requirements)
 - Be available for a total of 160 hours of regular sessions over 13 weeks.

## Stipends

| Role               | Base stipend [EUR] |
|--------------------|--------------------|
| Mob member         |               3000 |
| Mob facilitator    |               5000 |

Residents of EU member states receive the base stipend.
For residents of other countries, stipends are adjusted according to [purchasing power parity](https://en.wikipedia.org/wiki/Purchasing_power_parity) relative to the Netherlands.
See the [list of stipends by country](./stipends.md) for exact amounts.

You must be able to receive payments via one of:

- Bank transfer
- [PayPal](https://www.paypal.com)
- [Wise](https://wise.com)

## Technical requirements

Remote mob programming requires being able to simultaneously share your screen, view others' screens, talk to each other, and compile software.
This is only possible with sufficiently performant hardware, and therefore it's a condition for participation.

### Processing power

Be able to build the Linux kernel in under 35 minutes.
Here's how to benchmark using Nix:

```bash
PKGS="github:NixOS/nixpkgs?tag=23.11"
NIX_CONFIG="experimental-features = nix-command flakes"
nix build --no-link "$PKGS#linux.inputDerivation"
time nix build --offline --no-link --print-build-logs "$PKGS#linux"
```

To rebuild, execute the last command with an additional flag `--rebuild`.

### Video calls

- Video camera
- Headphones and reasonable-quality microphone
- Consistently low-noise environment

Please use a friend to make a test call on [Jitsi Meet](https://meet.jit.si/), including video, audio and *entire screen* sharing.
Ask a friend whether they can see your screen and hear you well while you are running [the benchmark](#processing-power).

### Internet connection

- Sufficient bandwidth
- Stable throughout multiple hours of video call

From the organisers' experience, mobile data is unlikely to suffice.

## Questions and answers

### Why mob programming?

With proper facilitation, mob programming avoids many problems prevalent in solo-programming and asynchronous collaboration.
It seems to produce better software and make for happier developers.
It optimises for knowledge sharing, which is critical for short-term teams that collaborate on unfamiliar projects, such as in this program.
It also reduces the organisation overhead due to cross-participant support.

### How to get notifications and updates?

Notifications are posted in the public Matrix room [Summer of Nix Announcements](https://matrix.to/#/#summer-of-nix-announce:matrix.org).
Set up your [Matrix client](https://matrix.org/try-matrix/) to receive push notifications on new messages.

News about the program are published in the [Summer of Nix Discourse category](https://discourse.nixos.org/c/events/summer-of-nix/45).
[Subscribe](https://meta.discourse.org/t/notifications-primer/228439) to receive push notifications or emails on new messages.

### Do I have to pay taxes on my stipend?

It depends.
**You are responsible for observing the laws that apply to you when receiving payments.**

The stipend is compensation for work towards a non-profit cause.
This means that in some jurisdictions it may be exempt from income tax, value-added tax (VAT), or from counting towards social insurance or health insurance obligations.

In some jurisdictions you may have to register a business to legally account for receiving payments.

Note that the stipend amount is exactly what the NixOS Foundation can pay.
If you have to process VAT, the total expense for the NixOS Foundation still must be the stipend amount, even if you put "reverse charge" on the invoice.

### Is this related to Google Summer of Code?

No, Summer of Nix is an independent program organised by the NixOS Foundation.
It is funded by the European Commission via the NLnet Foundation.

Summer of Nix was originally modeled after Google Summer of Code, but has developed its own profile.
We use the [purchasing power parity data](https://developers.google.com/open-source/gsoc/help/student-stipends#total_stipend_amount) from Google Summer of Code to calculate our stipends.

Unrelated, the Nix community applied for [Google Summer of Code 2024](https://discourse.nixos.org/t/call-for-mentors-google-summer-of-code-2024/39031) and [Google Season of Docs 2024](https://discourse.nixos.org/t/google-season-of-docs-2024-call-for-proposals-to-enhance-nix-documentation/40107), where you can participate to directly improve tooling and documentation in the Nix ecosystem.

### Why does this NGI-sponsored program use this or that software?

We do our best to select free and open source, privacy-respecting software.
But this is not a hard constraint, nor the only criterion.

We use:

- [GitHub](https://github.com/) for development and public technical discussion
- [Matrix](https://matrix.org/) for private, ephemeral, or real-time communication
- [Notion](https://notion.so/) for accounting

As a participant, you will need an account on each of these services.

## Organisers

- Shahar "Dawn" Or (mob programming)

  - GitHub: [@mightyiam](https://github.com/mightyiam)
  - Matrix [@mightyiam:matrix.org](https://matrix.to/#/@mightyiam:matrix.org)

- Valentin Gagarin (program direction)

  - GitHub: [@fricklerhandwerk](https://github.com/fricklerhandwerk)
  - Matrix: [@fricklerhandwerk:matrix.org](https://matrix.to/#/@fricklerhandwerk:matrix.org)

[Open an issue](https://github.com/ngi-nix/summer-of-nix/issues) to ask a question in public.
Send us direct messages on Matrix for questions that require privacy.
