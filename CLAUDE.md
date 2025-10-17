# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**research-os** is a Claude Code plugin ecosystem that provides an integrated research-to-implementation workflow. It's a spec-based research engineering system with specialized AI agents for each phase of development.

The repository implements a **marketplace-compatible plugin** (`plugins/researcher/`) that contains:
- **25 specialized subagents** organized by workflow phase
- **4 user-facing commands** that orchestrate multi-agent workflows
- **Structured output artifacts** in markdown format

## Architecture & Workflow

The system follows a 5-phase workflow, with outputs from each phase feeding into the next:

```
1. RESEARCH PLANNING → Creates research-os/project/
   ├─ research-journal.md (iterative refinement history)
   ├─ related-work.md (literature review)
   ├─ abstract.md (positioned abstract with hypothetical results)
   ├─ roadmap.md (experiment phases with dependencies)
   └─ tech-stack.md (technical requirements)

2. SPECIFICATION → Creates research-os/artifacts/YYYY-MM-DD-spec-name/
   ├─ planning/
   │   ├─ initialization.md (raw idea)
   │   ├─ requirements.md (gathered requirements)
   │   └─ visuals/ (reference images)
   ├─ spec.md (detailed specification)
   └─ tasks.md (strategic task breakdown)

3. IMPLEMENTATION → Updates spec folder with:
   ├─ planning/task-assignments.yml
   └─ implementation/ (reports per task group)

4. VERIFICATION → Adds to spec folder:
   └─ verification/ (verification reports)

5. FINAL OUTPUT → Complete documented implementation
```

## Plugin System Structure

### Agent Definition Pattern

All agents follow this YAML frontmatter + markdown pattern:

```yaml
---
name: agent-identifier
description: Brief description of agent's purpose
tools: Write, Read, Bash, WebFetch
color: purple  # UI color coding
model: opus    # Model selection: opus/sonnet/haiku
---
```

Agents use template references like `{{workflows/planning/gather-research-info}}` and `{{standards/global/*}}` to include workflows and standards.

### Command Structure

Commands in `plugins/researcher/commands/` are markdown files that:
1. Define multi-phase workflows
2. Delegate to specialized subagents using the Task tool
3. Pass context between agents via file artifacts
4. Produce structured documentation

## Key Commands

### Research Planning Phase
```bash
/plan-research
```
Initiates comprehensive research planning workflow. Creates `research-os/project/` with all research documentation.

### Specification Phase
```bash
/new-artifact [feature-description]
```
Initializes a new feature specification in `research-os/artifacts/YYYY-MM-DD-spec-name/`.

```bash
/create-artifact
```
Generates detailed specification and task breakdown from gathered requirements.

### Implementation Phase
```bash
/implement-artifact
```
Executes implementation workflow:
1. Reads tasks.md and assigns to specialist agents
2. Delegates implementation to appropriate agents (api-engineer, database-engineer, ui-designer, etc.)
3. Runs verification workflow
4. Produces implementation reports

## Working with Subagents

When delegating to subagents, always provide:

1. **Clear context**: Spec folder path, relevant files, specific task assignments
2. **Explicit scope**: Which tasks they should implement (agents check their areas of specialization)
3. **Output expectations**: Where to write reports, which files to update

Example delegation pattern:
```javascript
// Use the Task tool with subagent_type parameter
{
  subagent_type: "api-engineer",
  prompt: "Implement Task Group 2 from research-os/artifacts/2025-01-15-feature/tasks.md.
           Read spec.md for context. Document in implementation/task-2-api.md."
}
```

## Implementation Specialists

The system includes 5 specialized implementers, each with defined areas:

- **api-engineer**: API endpoints, controllers, business logic, request/response
- **database-engineer**: Migrations, models, schemas, database queries
- **ui-designer**: UI components, layouts, styling, responsive design
- **testing-engineer**: Test files, test coverage, fixtures
- **prompt-engineer**: Agentic workflows, orchestration, sub-agent prompts

## File Conventions

### Research Outputs
- Always create in `research-os/project/`
- Use standard filenames: research-journal.md, related-work.md, abstract.md, roadmap.md, tech-stack.md

### Specification Outputs
- Create in `research-os/artifacts/YYYY-MM-DD-descriptive-name/`
- Maintain folder structure: planning/, implementation/, verification/
- Core files: spec.md, tasks.md

### Task Updates
When implementing tasks, always update `tasks.md` checkboxes:
```markdown
- [ ] Incomplete task → - [x] Completed task
```

## Standards & Preferences

The system expects user standards in `research-os/standards/`:
- `backend/`: api.md, migrations.md, models.md, queries.md
- `frontend/`: accessibility.md, components.md, css.md, responsive.md
- `global/`: coding-style.md, conventions.md, error-handling.md, tech-stack.md
- `testing/`: coverage.md, unit-tests.md

Agents reference these via `{{standards/global/*}}` template syntax.

## Development Notes

### Adding New Agents
1. Create agent definition in `plugins/researcher/agents/`
2. Follow YAML frontmatter pattern
3. Define clear areas of specialization
4. Update implementers.yml or verifiers.yml if applicable

### Adding New Commands
1. Create command in `plugins/researcher/commands/`
2. Define phase-based workflow
3. Delegate to existing agents via Task tool
4. Ensure proper artifact passing between phases

### Extending the Plugin
To extend for pure software engineering (removing research focus):
1. Modify phase 1 commands to skip research planning
2. Start directly with specification phase
3. Adjust agent prompts to remove research-specific language
4. Keep implementation and verification phases intact

## Current State

The system is partially adapted for research engineering:
- **Fully adapted**: Research planning phase (all agents and commands)
- **Partially adapted**: Specification phase (retains some software-only language)
- **To be adapted**: Implementation and verification phases still use general software engineering terminology

Future work involves updating remaining agents to align with research engineering context while maintaining the robust multi-phase, multi-agent architecture.

## Ressources

To fully understand how the marketplace, plugin and components (slash commands, hooks, subagents and skills) work, check out

https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
https://docs.claude.com/en/docs/claude-code/plugins-reference
https://docs.claude.com/en/docs/claude-code/slash-commands
https://docs.claude.com/en/docs/claude-code/sub-agents
https://docs.claude.com/en/docs/claude-code/skills
https://docs.claude.com/en/docs/claude-code/hooks