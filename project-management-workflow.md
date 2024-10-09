# Project management workflows

This documents how we keep up with the NGI0 consortium requirements and make sure everything that needs to be done actually gets done.
We also want to be able to make a quantitative report to NLnet at any given time.

> This process description refers to various data sources; check the [information architecture document](./information-architecture.md) for details.

## Recurrent tasks

- **Triage:** Periodically (e.g. every 14-28 days) check “New Projects” and triage according to the [project assessment checklist](./project-assessment-checklist.md)
- **Status update:** Periodically (e.g. every 14-28 days) synchronize which projects are still active
    - Close [GitHub milestones](https://github.com/ngi-nix/ngipkgs/milestones) where the project has no planned tasks any more
    - Set the activity status in Notion accordingly, update the collaboration status
    - Set the status in the [NLnet dashboard](https://dashboard.nlnet.nl)
    
    This needs to be done manually for now, but could potentially be automated.
    
- **Progress tracking:** Keep notes related to management in the [Notion project entries](https://www.notion.so/nixos-foundation/0bea42f64e3d4780ab5ed918229ac693)
    - Tag updates with `@today`
    - List attendees when recording discussions or decisions
- **Timesheets:** Review participants' timesheets in regular check-ins (e.g. weekly)
    - Check that all entries have links to artefacts
        - pull request, issue comment, publication, …
    - Approve entries that pass the checks
- **Invoices:** When an invoice is submitted
    - Check that the approved timesheet entries add up to the invoiced hours
    - Check that [VAT rules](./README.md#do-i-have-to-pay-taxes-on-my-stipend) are followed
    - Create a new entry in the [Notion invoices table](https://www.notion.so/5563829a7afd4c4497ec088f6eeae807?pvs=21)
        - Add the PDF and enter invoice details, link the contract
    - Export approved timesheet items, run cleanup script, import into [global timesheets table](https://www.notion.so/nixos-foundation/beccc7a6e1c844c8b3e0b200c7d335d2)
        - Link the newly created invoice entry for all new items
    - When everything checks out, send out approval
        - NixOS Foundation has to trigger the transfer
- **Internal reporting:** As part of preparing an NLnet management check-in, run the reporting script (TODO) to generate an overview
    - Given the entire collection of projects for a fund, we want to be able to determine for each of them:
        - the degree of completion
            - relative to what was planned
                - read open issues from the GitHub milestone for the project
                - if issues have labels for deliverables, those are incomplete
            - relative to what the project may need
                - read the NGIpkgs data structure for the project
        - activity traces (pull requests, issue comments, …)
        - related work in progress (open pull requests)
        - planned future work (open/assigned issues in milestones)
        - cost per project
        - allocated amount, total amount paid, burn rate, runway
- **Reporting to the European Commission**: Following reporting periods for each grant, generate financial reports and compile written reports
  - For submitting reports, follow the [instructions for using the EU tenders portal](https://www.notion.so/nixos-foundation/Instructions-for-reporting-to-the-European-Commission-5111ba44905649f7a4ad6431f28f0ed4) 
