<div align="center">

<img src="./assets/static/hero-phoenix.svg" alt="BlazeDashX | Refat Md. Labbi | Full-stack engineering and applied AI" width="100%">

<sub>DEVELOPMENT SYSTEMS · PRACTICAL PRODUCTS · LEARNING IN PUBLIC</sub>

<br><br>

<a href="#about">ABOUT</a> &nbsp; / &nbsp;
<a href="#selected-work">PROJECTS</a> &nbsp; / &nbsp;
<a href="#engineering">ENGINEERING</a> &nbsp; / &nbsp;
<a href="#live-signal">LIVE SIGNAL</a> &nbsp; / &nbsp;
<a href="#connect">CONNECT</a>

<br><br>

<img src="https://komarev.com/ghpvc/?username=BlazeDashX&label=UPLINK+COUNT&color=EF7338&style=flat-square&labelColor=101724" alt="Profile visitor counter" />
<img src="https://user-badge.committers.top/bangladesh/BlazeDashX.svg" alt="Committers.top Bangladesh public contribution ranking" />
<img src="https://img.shields.io/github/followers/BlazeDashX?label=NETWORK&color=2DBFE4&style=flat-square&labelColor=101724" alt="GitHub followers" />

</div>

---

<a id="about"></a>

## 01 / About

I'm **Refat Md. Labbi**, a Computer Science undergraduate based in **Dhaka, Bangladesh**. I work on full-stack web applications, mobile interfaces, and the services that connect them. My current learning interests are **LLM integration, system design, and machine-learning fundamentals**.

I like software that feels considered at both ends: clear interfaces for people using it, and understandable systems for people maintaining it.

| CURRENT DIRECTION | PRACTICAL EXPERIENCE | AVAILABLE FOR |
| :--- | :--- | :--- |
| Full-stack web and mobile development | React, Next.js, Express, PostgreSQL | Internships and software collaborations |

<a id="selected-work"></a>

## 02 / Selected systems

**A closer look at the work, rather than a wall of repository badges.** These are selected public repositories; project illustrations are designed summaries, not deployment screenshots.

<a href="https://github.com/BlazeDashX/Personal-Expense-Tracker">
  <img src="./assets/static/project-expense.svg" width="100%" alt="Personal Expense Tracker project illustration">
</a>

### Personal Expense Tracker

A single-admin financial workspace for managing expenses, budgets, transactions, reports, calendar activity, and personal records. The repository includes a verification workflow covering type-checking, linting, tests, and builds.

**Technical focus:** Next.js 16, React 19, Auth.js v5, Drizzle ORM, Neon PostgreSQL, Tailwind CSS 4, Vitest.

**What to inspect:** the authenticated workspace, domain-specific feature modules, database schema, reporting features, and verification scripts. [Explore source](https://github.com/BlazeDashX/Personal-Expense-Tracker).

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/BlazeDashX/LostLink">
<img src="./assets/static/project-lostlink.svg" alt="LostLink application design summary" width="100%" />
</a>

### LostLink

A lost-and-found app connecting reports, item discovery, claims, and recovery conversations. The mobile client and backend use separate application layers.

**Stack:** Expo, React Native, TypeScript, Express, PostgreSQL; optional Cloudinary uploads.

[Explore source](https://github.com/BlazeDashX/LostLink)

</td>
<td width="50%" valign="top">
<a href="https://github.com/BlazeDashX/Ayanco-frontend">
<img src="./assets/static/project-ayanco.svg" alt="Ayanco Trade Corporation system design summary" width="100%" />
</a>

### Ayanco Trade Corporation

A corporate site with product and service catalogues, quote requests, an administrative interface, and CMS-managed content.

**Stack:** Next.js 16, NextAuth, Cloudflare D1/R2, Resend.

[Explore source](https://github.com/BlazeDashX/Ayanco-frontend)

</td>
</tr>
</table>

**More repositories:** [Learning Platform frontend](https://github.com/BlazeDashX/Learning_Platform_frontend) · [Backend](https://github.com/BlazeDashX/Learning_Platform) · [Crown Clothing](https://github.com/BlazeDashX/crown-clothing-nextJS) · [A-05 Emergency Hotline](https://github.com/BlazeDashX/A-05-Emergency-Hotline)

<details>
<summary><b>OPEN THE ENGINEERING FILES / architecture notes</b></summary>

#### 01. Expense Tracker: product-to-database flow

Feature-based application structure, credentials authentication, data persistence through Drizzle ORM, and automated checks using the repository's scripts.

```mermaid
flowchart LR
    A[Next.js Application] --> B[Auth.js]
    A --> C[Feature Modules]
    C --> D[Drizzle ORM]
    D --> E[(Neon PostgreSQL)]
    F[Type Check / Lint / Vitest] -.checks.-> A
```

#### 02. LostLink: mobile-to-service flow

Expo/React Native client, Express endpoints for users/items/claims/conversations, and PostgreSQL records.

```mermaid
flowchart LR
    A[Expo Mobile Client] --> B[Express API]
    B --> C[(PostgreSQL)]
    B --> D[Uploads]
    A --> E[Local Storage]
```

#### 03. Ayanco: public site and content administration

Public website and a protected administrative area for content workflows, with Cloudflare services for data/media and Resend for outgoing messages.

```mermaid
flowchart LR
    A[Public Site] --> B[Next.js APIs]
    C[Admin Area] --> B
    B --> D[(Cloudflare D1)]
    C --> E[Cloudflare R2]
    B --> F[Resend]
```

</details>

<a id="engineering"></a>

## 03 / Engineering workbench

<img src="./assets/static/workflow-map.svg" width="100%" alt="How frontend, application logic, and data systems connect across projects" />

**Technologies I use or study**

| AREA | LANGUAGES AND TOOLS |
| :--- | :--- |
| Web interfaces | JavaScript, TypeScript, React, Next.js, Tailwind CSS |
| Services and data | Node.js, Express, NestJS, PostgreSQL, MongoDB |
| Mobile applications | React Native, Expo |
| AI/ML exploration | Python, PyTorch, LLM API integration |
| Engineering workflow | Git, GitHub, VS Code, Docker, Vercel, Postman, Figma |

<div align="center">
<img src="https://skillicons.dev/icons?i=js,ts,react,nextjs,tailwind,nodejs,express,postgres,python,pytorch,git,docker&perline=12" width="92%" alt="Technology icon set including JavaScript, TypeScript, React, Next.js, Tailwind, Node.js, Express, PostgreSQL, Python, PyTorch, Git and Docker">
</div>

<details>
<summary><b>OPEN THE WORKBENCH / what I'm learning and practicing</b></summary>

- **Application structure:** separating UI state, application logic, services, and persistence.
- **Authentication and access:** studying authentication flows and protected application areas.
- **Data modelling:** relational schemas, queries, and changes to stored data.
- **Testing and delivery:** applying repeatable checks where projects support them.
- **Applied AI:** exploring how LLM APIs and ML pipelines fit into useful software.

These are areas of practice, not a claim of equal expertise in every technology.

</details>

<a id="live-signal"></a>

## 04 / Live engineering signal

The graphics below refresh automatically from **public GitHub data** after Phoenix Profile Autopilot is enabled. They are generated by a scheduled workflow inside this profile repository, not hard-coded pictures.

<img src="./assets/live/dashboard.svg" alt="Live public repository counts, public stars, followers, and recent events" width="100%" />

### The repository constellation

A custom data-driven map of recently pushed public repositories. Node labels and sizes update from the GitHub API; connecting lines indicate membership in this portfolio, not software dependencies.

<img src="./assets/live/constellation.svg" alt="Live original repository constellation of recently pushed public projects" width="100%" />

### Development pulse

<img src="./assets/live/pulse.svg" alt="A thirty-day activity histogram based on real public GitHub events" width="100%" />

### Recent change log

<img src="./assets/live/activity.svg" alt="Most recent public GitHub repository events" width="100%" />

<details>
<summary><b>OPEN THE DATA ROOM / repository radar and language footprint</b></summary>

**Recently pushed public repositories**

<img src="./assets/live/radar.svg" alt="Most recently pushed public repositories and their latest dates" width="100%" />

**Primary languages across owned public repositories**

<img src="./assets/live/languages.svg" alt="Repository counts grouped by primary language" width="100%" />

*Language counts measure public repositories, not skill level or lines of code. Recent events only cover the public event feed's recent window, and do not include private activity.*

</details>

<details>
<summary><b>OPEN THE CONTRIBUTION TRACE / animated activity graph</b></summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/live/snake-dark.svg" />
  <img src="./assets/live/snake.svg" width="100%" alt="Automatic contribution snake generated from the GitHub contribution calendar" />
</picture>

</details>

<a id="connect"></a>

## 05 / Connect

**Portfolio:** [refatmdlabbi.vercel.app](https://refatmdlabbi.vercel.app/)  
**Email:** [refat00021@gmail.com](mailto:refat00021@gmail.com)  
**GitHub:** [@BlazeDashX](https://github.com/BlazeDashX)

<div align="center">

---

<sub>PHOENIX / BUILD · VERIFY · ITERATE · REPEAT</sub>

</div>
