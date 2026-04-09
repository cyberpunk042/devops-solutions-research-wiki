# User Directive — 2026-04-09 — Raw Idea Flow: Patterns, Standards, Wiki LLM Evolution

## Verbatim

> support preferred work window config:
> We're offering a limited-time promotion that doubles usage limits for Claude users outside 8 AM-2 PM ET / 5-11 AM PT / 12-6 PM GMT on weekdays.
>
> What is the promotion?
> From March 13, 2026 through March 28, 2026, your five-hour usage is doubled during off-peak hours (outside 8 AM-2 PM ET / 5-11 AM PT / 12-6 PM GMT) on weekdays). Usage remains unchanged from 8 AM-2 PM ET / 5-11 AM PT / 12-6 PM GMT on weekdays.
>
> Eligibility
> No action is required to participate. If you're on an eligible plan, the doubled usage is automatically applied.
>
> Where does this apply?
> The 2x usage increase applies across the following Claude surfaces:
> Claude Code
> ...
>
>
> ---- There is also the very important notion of the order of things and the repeated scaffold, foundation, infrastructure, features chain of evolution and design and engineering.
> This is important before it apply to almost any domain and any task when you think about it, just not on the same angles all the times and order and list.
> but its very important because if you are to build a whole project for example there is already at least evidently all those.
>
> More info:
> Scaffolding is just the basics: the core configuration files, the project structure, the technology stack (e.g., Python + Flask web server), and things like configuring AI files and a couple of READMs/documentation files.
>
> It's about deciding where the project is headed and choosing the main technologies.
>
> Foundation is about choosing the modules/packages, design system, project spine/column structure, diagrams, and architecture documents. It's also the beginning of more advanced configurations, scripts, and compilation and execution methods. (It sounds more complicated than it actually is, but it's a difficult part to start with if you're not very familiar with it.)
> -> At the end of this, you have a single entry point to manage everything, build, and update your product build. (Build = Results after compilation) The build process also typically has a single entry point with multiple options when needed.
>
> Infrastructure is where you build on the foundation and move forward with the development component called infrastructure, which is often a more common component that others will use and/or depend on.
>
> At the end of this, you already have a solution, but it doesn't do anything special; it's simply in place and established. If you want to add a feature, you just have to respect the structure and design. (This is what an AI does naturally when instructed with the right configuration.)
> This means that your build is no longer just an output proving that your foundation is sound, but that the base is in place and ready to deliver a result with basic functionalities and the basic interface, as well as new guidelines and documentation for developing features later.
>
> Example of infrastructure: an Excel module or an MCP (Model Context Protocol / in-format | AI operations standard for calling tools) that calls a tool.
>
> Features are usually the special features of your product, after being an environment and established standards ready to evolve.
>
> Advanced/specialized features in the interface (public server) or the backend (internal server).
>
> (Example feature: create an Excel spreadsheet using the ABC template for the XYZ case with the parameters "I, J, K")
>
> POC is when you rush things and skip steps to deliver something that would normally need to be rewritten. One or two or three features that prove the concept.
>
> MVP is when you do things properly and have at least three good features/features, plus additional ones, and are ready to scale/evolve without major problems.
> ______
> That was only for the a project as a whole but if we think deeper for example a new development for a feature or whatnot, then this repeat again.
> Or at multiple stage it repeats. Sometimes it mean to look top-down and then bottom-up, sometimes it means to do a design X before a design Y, or to look at what is in place in terms of foundation, infrastructure and existing features.
> The principle or starting with ordered stages and evolving artifacts and documentations and then adding metadata and annotations.
> This is wild right. but its a repeated pattern that has to repeat itself when building things...
> To build a skyscraper like we aim or any decent building or construction or product, there is always an order.
> We love the skyscraper analogy, we use it into the systems-course. its about the ideal being the skyscraper and the pyramid being the compromise between it and the mountain which is the spaghetti and deprecated patterns and solutions. the pyramid is how you deal with real world situation in general or already damaged solution to be able to compromise and deliver anyway. its the realism that you have to deal with the limitations, with the stack, with the requirements...
> skyscraper is easier when you start from scratch or you can refactor anything, especially when you are not even in production. it also is a bit flexible but its has a structure too which is important when working even if only lightly when needed.
> Another Example if front <-> middleware <-> Backend. or even a mediator when there is more than two ends (And again this is not limited to the literal of it but like top-down and bottom-up there is a pattern and paradigms)
>
> _____
>
> we will also make sure that we use all the superpower and main skills from high quality repositories marketplaces packs
>
>
> ____
> we might need to use the hooks and the notions of reverse hooks more too
>
> _____
> we might also need to do our own custom /commands generic and per role, a bit like for the skills
>
> _____
>
> we also now start to use a LLM wiki pattern with a notes / messages log and a backlog that can have the desired format per project such as Epic, Module, Task / Issue and we structure claude to continuously and naturally work with that and have the appropriate skill to do good work inside like with anything and like we want to pair commands (proper "https://github.com/artemgetmann/claude-slash-commands") and plugin. like "https://github.com/backnotprop/plannotator" which will be key (especially with the PM)
>
>
> ___
>
> the agents in the artifacts and document must define clear specs.md and design.md and
>
> there is also a new way to work in general.. Its called Wiki LLM and its flexible and I adapted it to my desired structure which we will share a schema that will evolve as it needs.
> it allow us to have a wiki/log and wiki/backlog with /backlog/epics|modules|tasks|issues.
>
> It comes with a high usage of the document header / annotations and metadata and custom fields and a structured format with per document / artifact high standards definition to be able to compare from strong document once those are defined and then the standards or vice-versa.
> even without open fleet with an individual agent it allow to follow methodologies and to proceed in orderly steps and respect rules and keep a per-project tracking and structured PM and internal documentation / wiki and artifact folders.
>
> This doesn't remove anything that we are already doing in openfleet its just transform it, evolve it. More surface to connect and more interconnected and structure and standards and norms.
> Once its fully done the information will transfer back to all the other project and serve as a model and the openfleet groups calls and tool-chains and sync features and such will embrace this model when working which will fit perfectly with the Ops/Kanban Board and the real PM/Scrum/Plane Board.
>
> This is a long task, treat it as such and check if we need to improve our second brain too.

## Interpretation

### Distinct Topics Identified

#### 1. Preferred Work Window / Off-Peak Usage
Claude offers 2x usage during off-peak hours. Relevant to scheduling automation and cost optimization. Connect to Claude Code Scheduling page.

#### 2. The Scaffold → Foundation → Infrastructure → Features Pattern (SFIF)
A MAJOR new pattern to document. The user describes a universal 4-stage build lifecycle:
- **Scaffold**: core config, project structure, tech stack, AI files, READMEs
- **Foundation**: modules, design system, spine structure, diagrams, architecture docs, single entry point
- **Infrastructure**: common components others depend on, basic interface, development guidelines
- **Features**: specialized product features built on the established base
- **POC**: skip steps to prove concept (needs rewrite later)
- **MVP**: 3+ proper features, ready to scale

This pattern is RECURSIVE — it repeats at project level, feature level, design level. It maps to the skyscraper analogy: skyscraper (ideal from scratch), pyramid (realistic compromise), mountain (spaghetti/legacy). Also maps to front↔middleware↔backend and top-down↔bottom-up.

#### 3. Wiki LLM Pattern Evolution
The user is evolving the LLM Wiki pattern to include:
- wiki/log — notes/messages log
- wiki/backlog — with epics, modules, tasks, issues (per-project format)
- Structured PM with document headers, annotations, metadata, custom fields
- Agents working with these artifacts continuously
- specs.md and design.md as standard agent artifacts
- This model transfers to ALL projects in the ecosystem

#### 4. Skills, Commands, Hooks, Plugins Ecosystem
- Use ALL superpowers and high-quality marketplace skills
- Explore hooks and "reverse hooks" more
- Custom /commands per role (generic + role-specific)
- Pair commands + skills + plugins properly
- Ingest: https://github.com/artemgetmann/claude-slash-commands
- Already using: https://github.com/backnotprop/plannotator (key for PM)

#### 5. OpenFleet Integration
This wiki model becomes the standard that OpenFleet agents embrace. Group calls, tool-chains, sync features integrate with this model. Ops/Kanban Board + PM/Scrum/Plane Board alignment.

### Action Items
1. Create SFIF pattern page (Scaffold → Foundation → Infrastructure → Features)
2. Create skyscraper analogy page (skyscraper vs pyramid vs mountain)
3. Evolve wiki schema to support backlog structure (epics/modules/tasks/issues)
4. Ingest the two new GitHub repos (claude-slash-commands, plannotator)
5. Document the preferred work window in Claude Code Scheduling
6. Research hooks and reverse hooks patterns
7. Design per-role /commands structure
8. Plan the wiki/log and wiki/backlog directories
9. Update OpenFleet integration page with new model
10. Check and improve the second brain as requested
