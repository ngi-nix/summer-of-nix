---
title: Summer of Nix 2021
subtitle: A Program Report
classoption:
  - a4paper
  - 10pt
mainfont: DejaVu Serif
sansfont: DejaVu Sans
documentclass: scrartcl
author: Matthias Meschede
linestretch: 1.05
geometry: "left=4cm, right=3cm, top=2.5cm, bottom=2.5cm"

---

---
abstract: |

  _The Summer of Nix 2021_ was a large coordinated effort to reproducibly package Open Source software to make it readily available and usable by anyone. The program brought together independent developers and community enthusiasts for two months to write build-configure-run instructions for many Open Source tools with the next-gen reproducibility-first package manager Nix. This report outlines the wider context, the development of the idea, organizational details and design, as well as concrete outcome and feedback of the participants. It is thought to be an interesting read for the funding organizations, future organizers and participants alike.

---

# Context

## Free and Open Source Software in a complexity crisis

<!--
Decentralized Internet Vision because of resilience, control over data, making the infrastructure available to everyone
-->

The Internet should be open, decentralized, and privacy-respecting, built on top of a tissue of Free and Open Source Software (FOSS) that allows anyone to build new and innovative applications in a decentralized network of equally important nodes uncontrolled by few giants. This vision, pursued by many community and political actors[@ecstrategy], but at best partial reality right now, ultimately derives from the fundamental idea of a participative society of sovereign citizens.

<!-- open and diverse ecosystems vs controlled standardized -->

But, a tissue of Free and Open Software comes with complexity that tightly controlled ecosystems can often avoid. FOSS is thus often notoriously difficult to install, configure and run—a natural consequence of the enormous diversity of approaches that thousands of self-thinking developers without centralized organization come up with.

<!-- illustrate the former -->

These developers use their favorite programming languages, dependencies, operating systems, distribution formats and platforms, and their software often needs to be compiled from source because of this diversity. This diversity is a _feature_ of an open ecosystem which greatly fosters innovation and resilience. But it comes at the price that freely and openly available software is often difficult to actually set up and run. The cost of setting up a FOSS ecosystem, is thus often higher than paying for an out-of-the box, fully integrated but opaque solution. This problem has been recognized for a long time in computer science circles[@linus; @mancoosi].

<!-- Nix as a solution to reproducibility -->

The package manager Nix[@doolstra2004nix; @nixosHow] is an emerging technical solution to manage FOSS complexity, and as such, a central component to make any Open Source strategy a success. Making FOSS easily available via Nix is thus the “raison d'être” of the _Summer of Nix_ program that this report is about.

## Organizations and their interest behind the Summer of Nix

Four institutions with different interests teamed up to realize the _Summer of Nix_:

The **European Commission**[@ec] (EC) is the initial _source of funding_ for Summer of Nix via their Next Generation Internet (NGI) initiative. The goal of this initiative is to “shape the development and evolution of the Internet into an Internet of Humans. An Internet that responds to people’s fundamental needs, including trust, security, and inclusion, while reflecting the values and the norms all citizens enjoy in Europe” [@NGI]. NGI is a huge program funding a large variety of projects and subprograms with 312 million Euro between 2018 and 2022.

The **NLNet Foundation**[@nlnet] (NLNet) is an independent foundation, largely aligned with the above stated mission of the EC's NGI initiative, and funding independent software for a long time. NLNet has been charged, via the ECs cascading grant mechanism, to _distribute_ parts of the NGI funds, specifically from a subprogram called NGI Zero [@NGI0] that “provides grants to individual researchers and developers as well as small teams to work on important new ideas and technologies that contribute to the establishment of the Next Generation Internet.”, and within this grant from an initiative called PET [@PET] that focuses on privacy and trust enhancing technology. With this framework, NLNet has funded plenty of FOSS solutions that all have to deal with the above outlined challenge to reliably build and deploy them in a diverse FOSS ecosystem. Looking for a technical solution, NLNet has chosen Nix as their preferred packaging strategy because of its unique reproducibility guarantees and features such as composability that allow to realize their, and NGIs wider vision. This is how parts of the funds became available to package NGIs software with Nix. NLNet has approached the NixOS Foundation to help them with this packaging effort.

The **NixOS Foundation**'s [@nixosfoundation] mission is “to support the infrastructure and development of the NixOS project as a whole”. It's scope of action is limited to essential tasks in the Nix ecosystem—because of limited resources, but also because Nix is managed to a large extent by a vibrant and self-organizing community. Being approach with funding for Nix packaging by NLNet was of course a welcome opportunity for them to enlarge and improve the Nix ecosystem. Before the idea of Summer of Nix was born, the NixOS Foundation worked with individual contractors on this packaging work. They had therefore already set up infrastructure such as a continuous integration server, and a basic task lists before Summer of Nix. But the NixOS Foundation lacked the manpower to drive the program forward more actively. This is why the idea of a collaboration with Tweag came up. The NixOS Foundation was the _administrating organization_ of the Summer of Nix, handling contracts, payments, IT infrastructure and more, but could stay largely out of program design and daily management.

The final actor, **Tweag**[@tweag], is a software consultancy and one of the principal enterprise user and contributor to Nix. Tweag sponsored project management, free of charge, to actually _design, organize and run_ the Summer of Nix. Tweag's interest are to improve and give visibility to Nix, and to foster and participate in a lively community around it.

# Designing and running Summer of Nix

## The idea emerges

<!-- What is it -->

<!-- idea came from developer feedback: -->

The initial idea, to run a large, concentrated community program in the summer, came up as a reaction on feedback from the Nix community about the already existing packaging effort with individual developers working independently through the large number of NLNet projects. The existing effort was not advancing as well as it should have, and it appeared not appealing enough to attract enough applications:

<!-- unqualified with no time to learn -->

Many community members felt unqualified to work professionally with an emerging technology that thus far had been mostly their hobby, or they felt that there might not be enough support and time to learn the required skills during the program. The entry barrier to applying for a packaging job was therefore quite high.

<!-- packaging research tools is unattractive -->

Another aspect was that packaging, although it can actually be a very interesting and worthwhile task, is not an attractive goal _in itself_ for independent developers. This was reinforced by the fact that many of the NLNet tools to package are still experimental, in prototype stage or alpha stage, without gigantic user base and sometimes no regular maintenance. Finally, although the program was decently funded, it was also not the place to get rich over night.

<!-- Real challenge: What excites developers? -->

The main challenge therefore was to design a program that is more attractive, and fulfilling, taking into account the non-monetarian interests _of the participating developers_ as much as those of the funding organizations to find the famous win-win situation.

<!-- What excites developers? -->

A few of the principles of the program emerged quite naturally from these thoughts. Participants should explicitly have time to **work, learn and meet**. Coding should not happen in isolation but in groups with discussions, feedback about the work. Participants should not only learn but also teach their peers. The program thus became much more than a simple coding gig, and we hoped that it would be a lot more attractive for participants.

<!--The money question -->

One direct consequence of realizing a project in the above spirit, open for beginners, with a lot more freedom for each participant to learn, teach, experiment and meet while applying their creativity, ideas and newly generated knowledge to useful work, was that we needed to go away from a professional software engineer's salary to stay within our given budget and to deliver the expected outcome for the allocated money. We decided to align it roughly to Google's Summer of Code rates instead.

<!-- the manpower question -->

Another challenge was that we had only very limited organizers available to work on the program: Even I, as the principal organizer, was by far not able to work full time on this project, although my employer Tweag generously supported me as they could. In addition to me, we had a small group of largely volunteer organizers that were a bit on-and-off depending on their time. It was thus clear from the beginning that, if we wanted to run a program with an emphasis on community and team work, we needed further organizational help, maybe in the form of a few selected people who would be experienced with Nix and willing to coordinate teams. The idea of “mentors” was born.

<!-- designing under constraint -->

The limited amount of dedicated time on the organizational side was probably the most constraining factor throughout the program, exacerbated by the fact that we were running it without experience and no prior infrastructure from scratch. This was clear to everyone from the beginning, but no situation is ever perfect, and we saw a good chance to deliver something decent within the constraints.

## Fixing the basics: compensation and time frame

<!-- interviews -->

The general idea was thus clear, but at this time, we had no idea how many applicants to expect, and also not how to put it in practice. Initially we guessed to maybe receive 10-15 applications of which certainly a few would drop out. Running the program with a team of about 5-10 people seemed realistic. Without any additional data, we made a final decision on the compensation, the time frame from August 2nd to October 15th, and also the mentor role.

<!-- compensation -->

Compensation was fixed to a flat base rate of 2750 Euro per participant for 8 weeks of full time work within the EU, as a gesture to the entity who ultimately funded this project, and otherwise adjusted for purchasing power based on a list from Google's Summer of Code in lack of a better resource. We considered worldwide equal pay as well, and arguments for and against came up, but ultimately we decided to adjust it, mainly because this was recommended by the European Commission and others who had more experience than us with the implications of one over the other. It is still unclear to me whether this was/is a fair choice or not. Participants from EU countries with lower purchasing power certainly made the best deal because of the flat rate, which corresponded to the rather high one at the NLNet Foundation's seat in the Netherlands. Payments themselves to all corners of the world were to be handled by the NixOS Foundation and NLNet, most experienced with this type of situation. One additional thought about compensation is that we didn't fix it based on the available budget but rather on a rough idea of what was expected to be delivered for the money. With the above compensation, a participant would have to deliver on average roughly three packages over the eight-week period—a number that we expected to vary hugely because the software to be packaged was so diverse. Still this seemed to be a good rough guideline for us to see how a more freely organized community event fairs economically in direct comparison with independent developers, and without taking any of its further benefits besides packaging into account.

<!-- time frame -->

The time frame from August 2nd to October 15th was also not easy to decide. We wanted to get university breaks across a variety of countries but didn't really have the data to take an optimal choice at this moment because we didn't know where participants would be applying from. One thought that came up was that the Southern Hemisphere was (as unfortunately so often), a bit disadvantaged by the fact that this was in their winter break and even just by the name of the event. Although there is certainly some truth to this, we weren't able to find a better solution for everyone within the limited time we had. For participants, we designed the program for 8 weeks, 320 hours, a bit similar to Google Summer of Code, so that actual work could be accomplished, leaving flexibility within the absolute time frame to take vacation or start earlier or later while at the same time making sure that there was enough overlap to actually work in a team. The stipend was to be paid in two chunks, after working the first 160 hours and then the second 160 hours. We expected to see more tangible outcome in the form of packages and other code contributions the second half of the program—something which turned out not to be true.

<!-- mentor arrangement -->

The mentor arrangement was a bit different. For the mentors, we kept the original rate that independent NLNet packagers received, about 50 Euro/hour. This meant that we couldn't possibly employ them full time over the duration. We thought therefore to design it for about 8 hours per week, and a total of 100 hours over the program. We hoped to be able to better compensate the mentors better for the added responsibility they had with this stipend. I'll defer more thoughts about this to later in this report.

## Announcement and interviews

<!-- announcement -->

These basic decisions were enough to announce the program on the NixOS discourse [@sonannouncement] and see who would apply. We didn't want to design the program before knowing who would actually participate. The response to this announcement was overwhelming and much more than the 10-15 applications we expected. In total, we received **94 participant applications and in addition about 10 for mentoring**. Applications were handled over email only because we tried to avoid sign-ups and reduce the barrier to participation as much as possible. Also email seemed more personal, especially when expecting maximum 15 applications anyway. But, given the high number of applications email became an overhead, although we half automated it, and getting applications in a more structured form might have simplified things.

<!-- interviews -->

In the application email, we asked a few simple questions to the applicants: Who are you? Why are you interested in this program? What are you able to do with in Nix? What would you like to learn? When are you available? What time zone? Specific requirements? Optional CV. These questions turned out to be very useful to quickly assess the goals of the applicants. But we also decided, before knowing how many applications we would receive, to have short 15-30 minute interviews with everyone without exception to get a personal connection and also to answer potential questions. We thus did over 100 interviews in about one month with a little team of four volunteers who were doing this besides their work. Again, in hindsight this was maybe not worth it and quite e exhausting, but it also gave the program a very personal, respectful and warm touch. As interviewers we got a much better feeling for the Nix community, the wishes and goals of the applying participants, and therefore ultimately the program that we were going to run. During these interviews it became clear that we had a lot of enthusiastic, extremely nice and very knowledgeable people applying.

## Selection process and team building

<!-- why we needed to select -->

The sheer amount and the high quality of the application was extremely motivating and made us want to turn forward time to get started, but it also brought us in the unpleasant situation of having to select and pick one good person over another—something we had hoped wouldn't happen anyway.

<!-- selection through team building -->

Ultimately we had a limited number seats in the program because of our budget, and once we saw the number of applications, we realized that we needed several teams to provide for the support structure that we wanted to achieve with this program. We decided to go with **five developers plus one mentor as basic team structure**.

<!-- diversity -->

Furthermore, since the program was specifically _not_ about just delivering code as quick as possible, but also about learning together and meeting other like-minded people, we didn't want to simply sort by “Nix skill” in whatever subjective definition and fill up the teams in order. In contrast, team **diversity** seemed to be highly desirable to actually make a fun program in the work-learn-meet spirit outlined above, naturally generating opportunities to learn from and have interesting conversations with each other.

<!-- geographical diversity -->

Unfortunately team diversity in all aspects wasn't easily achievable: A first decision that we felt forced to take was to have timezone-homogeneous teams that weren't spread over more than **±3 hours of time zone difference**, ideally less. Meetings and synchronous communication with more than three people spread over America, Europe and Asia, which we thought was _the_ essential part of the team idea, just seemed too hard to organize otherwise. We thus focused on geographical diversity _across_ but not within teams. This lead us to reserve 15 spots (3 teams) for Central European/African time zones, 10 spots (2 teams) for American time zones and 5 spots (1 team) for East European, Middle East and 5 spots (1 team) Eastern Asian time zones [we didn't have applicants from other parts of the world]. Although this distribution is biased toward European/African time zones, something normal because the funding came from there, this choice of numbers was mostly imposed by the number of applications from each region because by far most of them came from Europe. But, paradoxically it still gave a significantly higher chance to non-Europeans to participate, although there were less overall slots for them. Non-Europeans, here strictly refers to place of living at the time of the program, and some of those non-Europeans were Expat-Europeans. So, although we did have quite a range of continents and cultures present, we definitely didn't have anything globally representative, not even if one would focus on tech-savvy regions only.

<!-- gender -->

Another failure, as unfortunately so often in the tech world, was to achieve gender diversity. The only two (very strong) female applications weren't enough to even consider forming somewhat gender diverse teams.

<!--how we built the teams in the end -->

All this meant that we were left with building teams that were diverse along the axes of **seniority** and **nix skill**. We did this in a way which I'll call, for the lack of a better term, compartmentalized randomness: building on a 3×3 matrix of seniority and nix skill a random queue of applicants. The process was certainly not objective as basically any application process, but I think we were guided by reasonable principles. It meant in the end that senior Nix experts did have the highest chance to participate, simply because there weren't as many of them, but it also gave a fair chance to others.

<!-- other possibilities -->

We maybe could have considered additional axes to build the teams. For example, grouping people who were interested in similar technology, but this seemed to become too complicated under the other constraints and also a bit premature because we didn't go through the actual work yet in detail and hadn't thought about how to actually distribute it among the teams. Perhaps, rather than searching for ways to optimize teams further upfront, an additional mechanism to adapt and improve them during the program would have been something useful—but also potentially dangerous if done maladroit.

<!-- result -->

In any case, we have built seven teams of five with this process, meaning that we would have **35 participants and 7 (+1) mentors**. The additional mentor was reserved for additional tasks, and it would become clear later what those were. The total number of participants and mentors also determined the overall budget that we would need, which was higher than originally anticipated and meant that we were eating into money reserved for later, but it felt like a good investment since the application quality was so high.

## Timeline, issue organization and start

<!-- time lines -->

Everything that has been described so far, from first idea to the end of the selection process, happen in a relatively short time. It began end of January with a first mention of the idea on January 22nd, and then with one of the oldest of about 500 Summer of Nix related email threads in my in-box (excluding auto-generated notifications) from February 6th that reads: “we could have 4 participants FT for 5 weeks including budget for the mentors. This is probably the most challenging but also most rewarding endeavor and would need to be organized quickly if it is for this summer.”. The discourse announcement post came out on March 21st and we reached the end of the selection process on May 16th after 100+ applications. There was really not a lot of time for planning afterwards, because after about one month of down time, we had to start preparing for 35 developers and 8 mentors asking for what to do.

<!-- work item preparation -->

We started regular meetings with the mentors to start discussing the program details. As mentioned earlier, we had one huge up-front asset in this program:

<!-- the issue list -->

Thanks to prior work from the NLNet and NixOS Foundations, we already had a written list of relatively independent work items, the 200+ NLNet projects to package, prepared on GitHub. Certainly, some information was missing, there were duplicates and some of those issues were not tractable, but overall this list was a treasure trough and we would have had trouble to get ready in time without it.

<!-- assign and trade -->

Initially we thought about going through the issue list upfront, tag and distribute it to the teams, e.g. by technology. But we quickly realized that we simply didn't have the time to do this before the program started and that the list was too large for any single sequential group to deal with it. We therefore opted for a different method which I call **assign-and-trade**: The full issue list was randomly divided by 7, labelling every issue with a label belonging to one of the teams. Coincidentally the full list had quite precisely 7 pages on GitHub which means that splitting and labelling was really easy to do. This meant that some teams would have more difficult issues than others, and sometimes a team wouldn't have anyone with the required skills or simply wouldn't be interested in an issue. This is why we introduced a trading mechanism, where teams could flag interest in an issue they liked or put issues on the market that they didn't like.

<!-- packaging workflow -->

As further preparation, we also wrote a little, step-by-step packaging work flow to get everyone started quickly. This work flow also defined a few standards and roughly went like this: As developer you would look through the issues assigned to your team via a GitHub label, and then pick from the list one that seems interesting, assigning it to yourself. An issue corresponds to a NLNet project and the first step typically was to find out what it was about, and what could actually be packaged. Once this was done, actual packaging work began by forking the repository to the [NGI-Nix](https://github.com/ngi-nix) GitHub organization, adding the Nix build instructions directly to the repository. Once this had been done, there were several paths to continue: a PR to the original source repository (that is why we thought forking was a good idea), a PR to nixpkgs, Nix's official package repository, or simply leaving it as independent build instructions on the repository.

<!-- feedback via an independent reviewer -->

Finally, we decided to assign the role of an independent reviewer to the 8th mentor who wasn't assigned to any team of the seven teams. The goal here was to give independent feedback to the participants and drive quality of the outputs up. We hoped that this would allow the mentors to concentrate on working with their team as much as possible without having to switch into the role of a counter-player themselves.

<!-- getting started with a test run -->

With the issue assignment strategy and the basic work flow, we felt ready to get started, but also scared to actually do so. Having 43 participants and mentors all begin at once without any test seemed audacious. The fear was not that our upfront preparation and game plan would work out perfectly, it was always thought more as a guideline for smart individuals, and with the little time that we had to organize the program we didn't hope to get anywhere close to perfection. But we feared to have missed something major that would block and demotivate the smartest participants from the beginning. Fortunately, two participants and their team mentor were willing to get started already in July, one month before the actual start date on August 2nd, to try what we had come up with. They started to package the first repositories, started to flag up problems and got used to the program.

## Tooling

During the preparation phase, we also had to take decisions about the tools that we used to organize this event. **Simplicity** over fanciness was probably our major guideline here. In addition, we tried to use **FOSS tools** because it corresponded to the overall spirit of the program and because they were often quicker and easier to use because no further budget and sign-ups were required. But we also decided to be **pragmatic** and use commercial tools whenever they were providing us with a clearly simpler and more robust solution.

Some of the FOSS tools we used (none of them self-hosted) were:

- Cryptpad for collaborative text documents and sheets
- BigBlueButton for webinar-style presentations
- Jitsi for face-to-face video conferencing
- Matrix for synchronous chat

Some of the commercial tools we used were:

- Hellosign for signatures
- GitHub for the issue list, program documentation, discussion board and the actual source code
- Google drive/docs to store administrative documents

In addition we used simple Email with a private contact list for administrative purposes and to send out .ics calendar invitations.

## The program runs

<!-- project start, handover to the mentors -->

The strange thing about bigger projects from the perspective of the organizer is that the start doesn't really feel like the start because so much of the work seems to have already happened. As soon as the boulder starts rolling down the hill, its much harder to influence where it'll end up. But the built-in day-to-day guidance, via the mentors who were admittedly dropped into a situation with quite some responsibility with little time for preparation and tight time budget (mentors were officially only available one day per week for coordination), paid out. They handled from day one the major part of the work load, guiding, organizing and resolving little issues directly on site.

<!-- little vision about what actually happened -->

A strange, but maybe common, situation that we were in over the whole program was that no-one precisely knew what was actually going on. Work was distributed and trust-based and everyone had just a limited perspective. Participants knew most about the packages they were working on, mentors had a larger vision of their team activities and also the issue list, organizers were busy organizing.

<!-- approximate organized events -->

Besides autonomously working, learning and talking to other participants, typical _organized_ events for a participant in a week were a team meeting, sometimes a centrally organized presentation on Wednesday in two editions to cover all time zones, and sometimes a participant presentation on Tuesdays. The centrally organized presentations were given by invited speakers, some of them participating themselves in the program, others not, about in-depth Nix topics more than about the newest and craziest ideas.

<!-- other events -->

Other events happened of course, proposed by various participants, and every team organized differently. Later in the program we sent out a list randomly assigning one or two meetings with someone from another team every week to foster cross-team communication.

<!-- difficult to describe -->

It is difficult to describe what happened exactly then, the program did run more or less autonomously, I was even able to hand over coordination for 2 weeks to go on vacation, and although certainly problems came up and we were far from optimal work allocation or feedback mechanisms for the participants, it went through without bigger accidents. Some of the deeper organizational problems that happened, and that are important indication to what we could be done better _even under the same constraints_ if we were to repeat this program became visible and clear _after_ the program when we asked for detailed feedback which we will cover in a later section in this report.

## The hiring event

Despite the actual event running, an additional idea that seemed high very valuable to pursue, even at the expense of having less time to actively drive the main program, came up already at the end of the interview process.

Besides organizing the Summer of Nix event, I am a consultant at Tweag and often talk to companies using it. Often, and similar to other emerging technologies, Nix is a blessing and curse at the same time for them. Obviously an emerging technology can solve previously unsolved problems, but one downside is that often it doesn't come with a job market that is as vibrant as with other, less powerful tools. Immediately after the interview phase, I knew that companies would have great interest in meeting those candidates, and I had the feeling that the same was true for many participants themselves who often considered Nix more as a hobby of theirs but as something they might find a job with. From this perspective, the idea of bringing Summer of Nix applicants (independent of how many spots we had in the program), together with companies was natural, but it meant further organization when we were already spread very thin.

Still, I took the decision that this was worth pursuing simply because it felt like without it this event wouldn't be complete. The hiring event provided a great point of motivation and direction for the training aspect of Summer of Nix, connecting talented community members to the professional life, after the experience of delivering paid work in a somewhat protected and freer environment. However, it did come at the cost that I had less time to spend on the main event, and, to realize this event, we had to reduce it to the essential, no-fuzz, just straight to the bottom of it connecting one side with the other in the most efficient way. Since we had no choice anyway, we decided to make a feature out of this constraint requiring as little upfront setup for anyone who wanted to participate as possible.

We compiled a list of about 60 companies who we knew had been using Nix, many of them small enterprises but some also very large and reached out to them. Of those 13 decided to actively participate in the hiring event. Although we duplicated every event so far to cover all time zones, we decided to go for a unique slot this time from roughly 5pm (UTC+2) - 8pm (UTC+2). There is no single slot available that covers West-Coast US to far-eastern Japanese time zones. This one was picked at the expense of Japan, for whom the event unfortunately was very late from midnight till two o'clock in the morning, but we felt we had no choice here.

The rest of it was essentially a matching problem, filling up a matrix of meeting slots x participants x companies with unique entries while considering time zones, participant and company preferences. We decided against 1-on-1 meetings, because we didn't want to create an interview situation but rather a more active conversation going. But we also wanted to avoid a non-interactive, webinar style situation. Our ideal goal was thus to get little groups together, anything between 2-on-5 or the opposite. With some little helper scripts but also a ton of manual intervention, we came up with schedules for those direct companies-participant meetings, and also organized 1 hour of lightning presentations of all 13 companies right before so that everyone knew what was coming.

# Contributions

## The Birds eye perspective


<!-- gathering data -->

During the program I knew that everyone was doing _something_, but it was unclear what we actually accomplished as a group. There also was no time to gather during the program and it was only after it finished mid-October that I started doing this, getting a better perspective.

<!-- activity on the issue list -->

![Number of newly created and closed issues in our central issue list as a function of time.](./figures/issues.png){#fig:issues}

A first entry point into the work we have done is the GitHub issue list that we worked on. The issue list activity is shown in @fig:issues. Most issues were created (orange line) automatically in two big chunks prior to starting Summer of Nix, from an internal project database that NLNet maintains. The number of issues grew further during the program, because some of the auto-generated issues were broken up into sub-issues and a few new projects were added by NLNet. Issues were closed (blue line) for a variety of reasons, primarily because the work had been done but also for a number of other reasons. For example, some issues have referred to hardware-only projects without anything to package, others were intractable for other reasons. A few issues remained in “ready for review” state at the end of the program since we were bottlenecked on capacity for more reviews. In absolute numbers, we have started with about 230 open issues at the start of the program of which a bit over 10 were already closed by prior packaging efforts. We ended up with a total number of 276 issues of which 101 were closed and 27 flagged as “ready for review”.

The sheer number of issues doesn't really give an idea of the work involved though, because their size and difficulty varied drastically. Some issues involved simply bumping a version on nixpkgs because the associated project had already been packaged there, others involved profound work on bootstrapping infrastructure or mobile NixOS that could easily have taken the time of a single packager over the whole program's time frame and more. Another number is the number of issues closed or flagged as “ready to review” _on average per participant_, which was about 3.4, slightly above our expected rate of 3. However, this number is not great and really only a gross approximation because in addition to issue diversity we also had drastic developer diversity so that a simple mean doesn't give a good idea of the actual accomplished work distribution. Finally, and most importantly, the number of closed NGI packages only captures a small part of the actual code contributions of this program plenty of upstream contributions, bug fixes, improved documentation came out of it, and it doesn't capture the quality of it.

<!-- number of repositories -->

![Number of repositories in the ngi-nix GitHub organization as a function of time.](./figures/repositories.png){#fig:repositories}

Another, similarly limited but still interesting, perspective of the work done during Summer of Nix is the number of repositories under the `ngi-nix` GitHub organization. Every tool to be reproducibly packaged went under its own repository although there were exceptions such as upstream nixpkgs contributions. @fig:repositories shows that the number of repositories went up drastically once the program started, and a lot of new ones were created over the course of the program. All in all there are now about 180 repositories, many public but also some private, in the organization holding NLNet projects reproducibly packaged to varying degree (not all of the work was finished).

<!-- add numbers about contributions channels from time sheets -->

![Number of contributions for different upstream channels.](./figures/channels.png){#fig:channels width=50%}

<!-- add numbers about additional team contributions from time sheets -->

Besides GitHub, another source of information are the time sheets that program participants have filled out with their contributions. Although it is a tedious job, we have gathered every reported contribution, a whopping number of 199 repositories, upstream PRs or relevant issues to various channels in structured form (The full list is in the end of this report). @fig:channels summarizes where those contributions went: most are repositories on NGI, filled with Nix package descriptions for the respective tools, then a lot of contributions went directly to nixpkgs, Nix' official software library, with NGI packages or dependencies of them, and others to the wider Nix ecosystem or to upstream repositories with bug fixes or other enhancements that came up in the packaging effort.

<!-- other Nix contributions -->

The wider contributions for the Nix community were bug fixes on the so-called 2nix helper tools to reproducibly package various programming language ecosystems. But also new and very interesting tools were initiated like dream2nix, static analyzer, and contributions to documentation that hopefully simplify future packaging efforts.

<!-- outcome for participants -->

It's hard to say what concrete outcomes the program had for individual participants. Some became first-time maintainers on nixpkgs, others got hired either by the project teams they worked on, or through the hiring event—but I don't have exact numbers and not even a vague idea here how many in total.

We had in total four participant drop outs—two of those before the program started. Not everyone finished the program fully. The participant contract was designed to deliver 320 hours in two chunks of 160 hours. Basically everyone delivered the full chunk on the first half, but 5 participants finished the second part only partially for various reasons. This means that we initially had 31 participants working and a few less at the end of the program.

In addition to just participating, one participant ran a Nix camp where one could hack on-site together. Another wrote a blog post for the Summer of Nix website. Yet another participant helped to record all video sessions (which turned out to be great learning material but unfortunately not produced to become public).

# Participant feedback

We organized four open feedback sessions after Summer of Nix to gather thoughts about the program from the perspective of participants and mentors—ultimately the core groups of the program.

The overall experience was diverse, mostly positive, but also different from person to person and team to team. Some wider aspects of the program were universally seen as positive, and their absence regretted where it didn't work out:

- Participants universally appreciated in particular the **team experience, active communication and not working alone**. Some teams faired much better here than others, providing lively discussions, a weekly rhythm and a good support structure. But even in these teams, moments when participants, in particular those with less Nix experience, had to work alone on a package were seen as difficult. Other teams were much quieter and therefore the participants had a harder time. Similarly, from the mentor perspective a quieter team with star-shaped communication meant more work for the mentor because they were the principal fall-back point. The same theme, either appreciation of good support communication or the lack of it, came up in various aspects: Participants felt lost and mentors said that some were blocked for a long time without asking for help. It is no wonder, that all participants appreciated pair programming sessions that we later-on in the programming organized via two random, cross-team pairings per week, and regretted the lack of those in the beginning of the program. To summarize, it seems team work sometimes went very well, sometimes not. We weren't bad but there is certainly room for improvement here.
- The centrally organized presentations about the fundamentals of Nix by core developers with an interactive Q&A session attached were mentioned as highlights of the program. This was certainly not only due to the quality content but also due to the fact that this was a moment of community and also something that, similar to regular team meetings, gave a certain rhythm to the program. **Rhythm and structure** was a central aspect of the feedback in general. It seems we were definitely on the lower end, and more rhythm and structure would have been appreciated. Presentations, team meetings, and then later-on cross-team pairing sessions were all appreciated. In addition it was mentioned that motivation tapered off towards the end of the program, which might have been less if there were events like a closing ceremony (e.g. final presentations were proposed) to work towards. A mentor mentioned that the first week was super busy, so that they were barely able to work on day job and after a while the team got bored and work tapered off.
- Work distribution was another central aspect that generated some frustration: although the general assign-and-trade approach worked fine, some larger package families, that is packages from a similar programming language or software ecosystem, were spread across teams. It took a while to all bring them to the same people to tackle them jointly. And with the GitHub issue list alone it was difficult to see who worked on what and when. Furthermore, some participants would have liked to specialize on packaging software written in specific programming languages and we had no notion of that in our work distribution. On the other hand, I had the impression that some also enjoyed peaking into diverse and new technology. Probably a common denominator was that there was a perceived lack of ecosystem-oriented communication beyond the team boundaries, such as a simple Matrix channel to discuss Javascript packaging—so that every one has **an opportunity to follow their tech interests**..
- Another aspect related to motivation were the actual packages we worked on. Some of them, such as Jitsi, BigBlueButton, Arpa2 are very big, well-known tools, but sometimes demotivating because big and difficult to package. Inversely, others were small, prototype-like tools without regular maintenance where the question why we were spending time on them came up. Many felt that it would be worth to investing more time in central projects for the Nix community that simplify packaging in general. This became in particular clear when similar questions came up over and over from different participants. It was frustrating not to work on improving those directly. We somewhat allowed this, if it directly or indirectly helped for NGI packages and if someone had already worked on many “official” packages, but we didn't encourage it either because we were bound by the goals of the funding grant. **A clear answer to why we are working on something** would be appreciated.
- Some participants spend a significant amount of time on no-Nix and no-code tasks, chasing upstream/maintainers and so on. Few actually liked this part of the work and would have appreciated contacting project upstream maintainers beforehand to get cleaner task descriptions, or support with communication skills and what someone called “software archaeology”. Some packages were also just not possible to package, e.g. hardware related, and it was puzzling for some to be assigned to do something which isn't possible. **Clearer task descriptions** would have been great.
- we had no “formal” roles in Summer of Nix, besides participants, mentors and admin. However, some participants did take initiative and responsibility to organize things such as recording all presentations and distributing them, hosting code & chat sessions and more. Some were sliding in these roles and would have appreciated a more structured role distribution to know clearly what their tasks would be.
- Some aspects of the packaging workflow and work organization weren't ideal. E.g. the choice between external and internal flakes and between separate repositories or a big monorepo.


Then a few points about Nix came up:

- The Nix documentation was universally seen as difficult to read on many points
- Mediocre support for various ecosystems and bugs, and lack of documentation, templates and tutorials on how to use the various lang2nix tools. Simply finding and picking the right tool was a challenge as well because there is no unified place for this and there are many competing tools out there. Specific ecosystems that were mentioned are: Racket, Java, Android and Javascript apps.
- flakes restrictions were not a problem because it was part of the learning experience

Also some mentoring suggestions:

- Expect lots of similar questions: how to do overlays, how to do X. Also on ecosystems on tooling. Explain common themes such as lang2nix, services, nixos-container, modules, caches/hydra to participants.
- Get people to communicate. Ideally in issues but some feel it's very permanent and thus don't use it. Matrix is less overhead, easier, less formal and might be necessary to jump start working.
- Some are afraid to ask for help. Foster a culture of open exchange, organize a regular checkin with yesterday, today, blockers.
- Explain programming vs packaging skills: communication and archeaology.
- Show and help how to “sell” Nix adoption to upstream

Concrete ideas for a future edition:

- The introduction system (having a suggestion of 2 people to meet per week) was amazing, if possible it should start at the beginning. This is one way that you can find other people that might help you when you get stuck.
- If some people become long time members of the Nix community that's success.
- Clearer rules about the general and the off-topic channels in the chat. Many participants were in there and the rooms were flooded by messages.
- External communication in the form of blog posts would be great and also motivating. We only had a single post there and didn't encourage this much.
- Assign multiple people per package. It was amazing to collaborate with others on packages.
- Get common compute resources, e.g. from a cloud provider, and actually have the service running on our own servers would be great.
- Facilitator for pairing meetings would be great because when meetings happened they were great.
- Move to external flake and monorepo, or a metaflake.
- Have an official internal documentation/timesheet page per participant
- Have both, teams (time zones) and cross-team communities of interest (language/ecosystem)
- Better upfront issue and team assignment.
- Use automatic ryantm-style update PRs or CI
  - eg: https://github.com/DeterminateSystems/update-flake-lock
- Make use of the content/experiences that we make during the program. E.g. publish the presentations and produce quality content for the community.
- Staggered beginning to handle the workload in the beginning.
- Build better onboarding material, similar to the Rustlang book, but for Nix.
- Permanent Jitsi channel to drop in
- Every participant could give half an hour to explain sometime for other participants on any topic so that they have to learn about it and that there is more exchange cross-teams.
- Officially work on upstream documentation.
- Part of Summer of Nix could be about getting the commit bit for nixpkgs.
- Summer of Nix could prepare participants for a NixCon conference talk.
- Work outside of NGI would be interesting. Summer of Nix should be more than NGI. Companies could submit projects to this event. Call for projects?
- Organizing marketing with an aesthetic dimension could also be interesting. Community manager could organize some polls or games. If too many diverse people are working on documentation, writing blog posts etc, new users can be lost quickly due to different styles and so on.
- Have a follow up period with a second stipend to *write*. Provide professional support with that.
- One “tech mentor” per programming language. The mentors were really helpful and knowledgeable, I felt that our problem were very programming language specific (e.g.: I'm getting this weird error with some javascript package, what do I do). Having a mentor of reference with experience in a particular area of the eco-system would be quite helpful. Potentially there could be the Java mentor, the Javascript mentor (if such a person exists)... One of the most frustrating points was getting stuck of course, and having somebody who experienced particular problems would be very helpful. Note that I think the mentors did a great job, this could just be the cherry on the cake.
- Take interest into account when making teams. Some people have an affinity/experience for some a programming language, trying to make teams that are interested in the same area (i.e. the rust team) could lead to synergies (people sharing useful informations they found about a certain thing) and more resilience to frustration (I like rust so I will work harder to make this work). Of course some teams might be more crowded than others, but that could be another criteria to select participants (e.g.: we don't have space in the rust team unfortunately, but would you be interested in joining the javascript team). Note that you could have a team interested in rust, but within the team some people are experienced with python and so you could give them a python and rust package. It will also improve the willingness to maintain a package in the long-term in case someone is interested in the technologies. The teams were formed by geography, I'm not sure it's so important, as long as time zones overlap by 4 hours during the day, I would think it's enough to have all the required meetings.
- Another, more basic nixos-module presentation. The nixos-module presentation was truly on another level. However it dealt with abstract informations around the nixos-modules. I feel there needs to be a "boring" presentation that goes through some existing modules and explains what is happening (e.g.:systemd has a require attribute that does... In this module you can see how to initialise a database). All those informations can be of course found in nixpkgs, but a detail of the most common "tricks" might go a long way.
- Pre-screening the packages for unmaintained ones. It was a little confusing to see unmaintained packages in issues. Pre screening for only the relevant packages might improve the motivation of the participants. Getting stuck on a maintained pakage is one thing. Getting stuck on something that feels it will never be used anyway reduces motivation significantly.
- Organise a pre-packaging effort to help upstream projects be “cleaner” to package.
- New participant role community manager: someone who animates Summer of Nix community organizing discussions, polls, games.
- New participant role pairing partner: experienced Nixer available for pairing.
- New role web-master: someone who administers an open website on a repo where everyone can contribute. Move website to static site generator.

# Budget

We delivered Summer of Nix slightly under budget because of a few dropouts and some who decided to volunteer and leave the money in the original pool. The anticipated budget for all of this work was 131755€. The final amount will very likely be 107700€, including mentor and participant stipends as well as extra costs for material and organization.

# Conclusions

Overall, I am quite happy with how the overall program turned out. We knew that we had quite tight time constraints but we had probably a unique opportunity this year with pre-existing budget to realize an event like this. Under these constraints, now after gathering the data I am amazed about what we have accomplished:

We delivered more than expected although not everyone finished the program.

It seemed to have been a fun event for the participants. Much of the feedback can be traced back to a lack of time on the organizational side, and the fact that we were designing this program from scratch, and that everyone was new in their respective roles. There was little concern about the general idea and set up of the program. The principal goals of the program, **learn, meet, deliver** seem to be appreciated as well as working with FOSS software.

Independent of the work output, a measure of success for the Summer of Nix is whether we can bring new long term members to the community—maybe even professionally, and certainly we succeeded with some in this regard as well.

A future edition should therefore focus on improving the implementation and organization of the program and focus to make most out of everyone's time. I think there is good general alignment on what could be improved. The main bottleneck here are the organizational capacities that we have to actually realize these ideas under budget and other constraints. Distributed decision making will be central to achieve this.

All in all, I am really grateful to have been given the chance to organize this program by my direct employer Tweag, the NixOS and NLNet Foundations and ultimately the European Commission, but then especially all the participants, mentors and volunteered who actually ran this program in the end and who achieved an amazing amount of contributions.

I hope that together we were able to make a small contribution to the FOSS universe and that we can continue to doing so in a variety of forms.

# Contribution List

<!-- this is replaced at build time with the list of contributions -->
{{contributions}}

# References

---
references:
- id: SoNWebsite
  author: The Summer of Nix organization team
  title: The Summer of Nix website
  year: 2021
  url: https://summer.nixos.org/
  urldate: 2022-01-05
  type: online

- id: ecstrategy 
  author: European Commission 
  title: The European Commission's Open Source strategy for 2020-2023
  year: 2020
  url: https://ec.europa.eu/info/sites/default/files/en_ec_open_source_strategy_2020-2023.pdf
  urldate: 2022-01-05
  type: online

- id: NGI
  author: The Next Generation Internet website
  title: About the NGI initiative
  url: https://www.ngi.eu/about/
  urldate: 2022-01-05
  type: online

- id: NGI0
  author: The Next Generation Internet website
  title: About NGI0
  url: https://www.ngi.eu/ngi-projects/ngi-zero/
  type: online

- id: nlnet
  author: NLNet
  title: Foundation Website
  url: https://nlnet.nl/
  type: online

- id: PET
  author: The NLNet website
  title: About PET
  url: https://nlnet.nl/PET/
  type: online

- id: linus
  author: YouTube
  title: Linus Torvalds on why desktop Linux sucks
  url: https://youtu.be/Pzl1B7nB9Kc
  type: online

- id: sonannouncement
  author: The NixOS discourse
  title: The Summer of Nix—learn Nix while doing useful, paid work
  url: https://discourse.nixos.org/t/the-summer-of-nix-learn-nix-while-doing-useful-paid-work/12225
  type: online

- id: mancoosi
  author: Roberto Di Cosmo et al.
  title: The Mancoosi project
  url: https://www.mancoosi.org/
  type: online

- id: doolstra2004nix
  type: inproceedings
  title: "Nix: A Safe and Policy-Free System for Software Deployment."
  author: {Dolstra, Eelco and De Jonge, Merijn and Visser, Eelco and others}
  booktitle: {LISA}
  volume: {4}
  pages: {79--92}
  year: {2004}

- id: nixosHow
  author: Nixos Community
  title: NixOS Website
  url: https://nixos.org/guides/how-nix-works.html
  type: online

- id: tweag
  author: Tweag
  title: Company Website
  url: https://tweag.io
  type: online

- id: nixosfoundation
  author: NixOS Foundation
  title: Mission statement
  url: https://github.com/NixOS/nixos-foundation
  type: online

- id: ec
  author: European Commission
  title: What the European Commission does
  url: https://ec.europa.eu/info/about-european-commission/what-european-commission-does_en
  type: online

---
