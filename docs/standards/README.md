---
title: Standards Root
description: Mandatory technical specifications and hard rules
categories:
  - standards
draft: false
date: 2026-02-27
lastmod: 2026-02-26T22:20:43.568Z
tags:
  - standards
  - protocol
  - spec
agent-readable: true
agent-editable: true
agent-moveable: false
agent-deletable: false
agent-friendly: true
---

# SYNOPSIS

standards ::= {Hard_Rules | Technical_Specs | Mandatory_Protocols}

# PROTOCOL

- **Absolute_Compliance**: Standards defined here are non-negotiable requirements for all assets.
- **Structural_Integrity**: Every file must align with the schemas and naming conventions defined in this folder.

# TOPOLOGY

- /docs/standards/language.md :: Mandatory language policy (Primary/Secondary).
- /docs/standards/markdown.md :: Technical specification for Frontmatter and Links.
- /docs/standards/agent.md :: Standards for agentic behavior and response patterns.
- /docs/standards/document.md :: Mandatory dual-target pairing protocol (DPS).

# CONSTRAINT

- Type: Multi-target (README.md [Ag] | README.ko.md [Hu])
