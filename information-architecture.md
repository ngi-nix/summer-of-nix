# Information architecture

The NixOS Foundation's NGI0 partnership is a complex project that requires different tools to fulfill our duties, such as responding to support requests, timely status updates and financial reports.

We have multiple sources of information:

- [NLnet Dashboard](https://dashboard.nlnet.nl) (consortium management, private)
    - Complete list of projects with metadata:
      - Repository URL
      - Author's contact details
      - ...
    - Project status
        - We primarily use it to source new projects and track triage status
        - Use `Project preparing` as a stopgap for “triaged but not actionable yet”
- [Notion](https://www.notion.so/nixos-foundation/Summer-of-Nix-accounting-c94ec6fcab8344cbbce1842e19d4ff4d) (accounting and reporting, private)
    - High-level progress tracking
        - Priortisation
        - Internal notes
        - Status of outreach to project authors
        - Status of implementation activity
    - Timesheets (hours spent mapped to projects and pull requests)
    - Contracts (compensation and time commitment)
    - Invoice handling
    - Budget planning
    - Budget reporting
- [`ngi-nix` GitHub organisation](https://github.com/ngi-nix) (task management)
    - Milestones (one per project)
        - Lists public project metadata
    - Pull requests (work in progress)
    - Issues (tasks and assignments)
    - Projects (status overview and priorities)
- [NGIpkgs monorepo](https://github.com/ngi-nix/ngipkgs) (main code base)
    - [Project data structure](https://github.com/ngi-nix/ngipkgs/tree/main/projects)
        - Encodes state of completion (which packaging artefacts exist)
        - Can map to other sources:
            - Nixpkgs
            - [`ngi-nix` flakes](https://github.com/orgs/ngi-nix/repositories?q=visibility%3Apublic+archived%3Afalse)
            - project upstream repository
- [Summer of Nix repository](https://github.com/ngi-nix/summer-of-nix) (front page)
    - Announcements
    - Reports
    - Process documentation and tooling
