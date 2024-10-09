# Project assessment and selection checklist

NLnet is funding many, many projects.
Program participants should know exactly what to do, and the project organisers' task is to provide overview and clear, tractable tasks.

1. Periodically triage new projects in the [NLnet dashboard](https://dashboard.nlnet.nl/) (private)

   The goal is to update the project status.

   - Filter for status `New Project`
   - Prioritise tagged projects

      NLnet managers do preliminary triaging to recommend projects for partners to engage with:

      - [`hl_NixOS`](https://dashboard.nlnet.nl/search?q=&tags=hl_NixOS) for hot leads — actively interested in collaboration
      - [`cl_NixOS`](https://dashboard.nlnet.nl/search?q=&tags=cl_NixOS) for cold leads — potentially suitable projects
      - [`dl_NixOS`](https://dashboard.nlnet.nl/search?q=&tags=dl_NixOS) for dead leads — don’t follow: not interested, inactive, ...

1. Check the source repository for relevance and liveness

   Can the project benefit from getting packaged for Nixpkgs or NixOS?
   Is the project under active development, in maintenance mode, or abandoned?

   Set status to `Out of scope` if:
   - By nature of the project there is nothing to package
   - It appears that it's not being worked on any more

   Set status to `Project preparing` as a stopgap for “triaged but not actionable yet”.

1. Ensure that the project has an entry in the [Notion project database](https://www.notion.so/nixos-foundation/0bea42f64e3d4780ab5ed918229ac693)

   Enter all the relevant data fields based on the NLnet project, in particular:
   - Page title: Symbolic project name (as found on https://nlnet.nl/project)
   - Fund (NGI0 Core, NGI0 Entrust, ...)

   Set status to `Active` to signal that we're working on it.

1. Create a GitHub milestone for the project

   Use the symbolic project name as a title.
   Tasks for this project will be GitHub issues attached to this milestone.

   - Export project metadata and put it into the milestone description
   - Update the executive summary to be brief and relevant for participants
   - Create issues for the next steps:
     - Identify possible deliverables
     - Check for existing artefacts

   This allows separating what's possible in principle from what we intend to actually work on, and measuring the degree of completion based on what's in the code against what was planned.

1. Identify possible deliverables

   Depending on the project, one may come up with different types of artefacts for distribution:

   - development environment

     A specification for a reproducible development environment that contains all necessary tools for working on the project.

   - library

     A software component that can be used in a build, leveraging Nixpkgs composition mechanisms.

   - program

     An executable or set of executables that can be run standalone.

   - service

     A program or set of programs that are configured to run in the background over prolonged periods of time.

     - test

       NixOS service modules invoke the original project's executables in a specific way that must be tested for correctness.

     - example

       NixOS service modules add an interface to the original software project that will necessarily differ from other modes of interaction.
       This requires providing configuration examples that show how to use the module.
       These examples should be used by the tests to make sure they are correct.

   Map out the deliverables in the corresponding [NGIpkgs project definition](https://github.com/ngi-nix/ngipkgs/tree/main/projects).
   Set fields for deliverables that have no obvious implementation to `null`.

   This allows systematically assessing the general complexity of projects.

1. Check which artefacts already exist

   - Does the project have its own `default.nix` or `flake.nix` upstream?
   - Is the project available in [Nixpkgs](https://search.nixos.org/packages)
   - Does it have a [NixOS module](https://search.nixos.org/options)?
   - Is there an [NGI repository](https://github.com/orgs/ngi-nix/repositories) packaging the project?
   - Is there an [issue in the NGI repository](https://github.com/ngi-nix/ngi/issues)  (private)?
   - Are there [open issues](https://github.com/NixOS/nixpkgs/issues) or [open pull requests](https://github.com/NixOS/nixpkgs/pulls) in Nixpkgs?

   Add all existing artefacts to the [NGIpkgs project definition](https://github.com/ngi-nix/ngipkgs/tree/main/projects).

1. Create issues for all missing deliverables

   Label them by type (`library`, `program`, `service`, ...).

   This allows estimating the complexity of projects and systematically inspecting their maturity.

1. Get in touch with project authors[^1] to assess if they are interested in or need help with:

   - Reproducible development environments
   - Contributor workflows
   - Continuous integration
   - Distribution to end users
   - Maintaining their Nix setup

   <!-- TODO: link to outreach template -->

   Set the collaboration status in Notion to `Reached out`.
   Update the collaboration status as needed. 

   [^1]: Sometimes contact details are provided on the dashboard, sometimes they are on the project website, but sometimes you have to dig into the project's commit log to find an email address. If contact details are hard to find, consider deprioritising that project.
