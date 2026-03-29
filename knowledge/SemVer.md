---
foam_template:
  filepath: "0 - INBOX/SemVer.md"
  description: "New note"
created: "2026-01-27"
---

# SemVer

SemVer ou Semantic Version est une convention de nommage des version d'une application, projet...

https://semver.org/

> A simple example will demonstrate how Semantic Versioning can make dependency hell a thing of the past. Consider a library called “Firetruck.” It requires a Semantically Versioned package named “Ladder.” 
> 
> At the time that Firetruck is created, Ladder is at version 3.1.0. Since Firetruck uses some functionality that was first introduced in 3.1.0, you can safely specify the Ladder dependency as greater than or equal to 3.1.0 but less than 4.0.0. 
> 
> Now, when Ladder version 3.1.1 and 3.2.0 become available, you can release them to your package management system and know that they will be compatible with existing dependent software.

This is working because minor version x.m.x doesn't bring breaking change in the application it keeps being retro-compatible.

But major version M.x.x change completely the 'API' so we can just blindly upgrade.