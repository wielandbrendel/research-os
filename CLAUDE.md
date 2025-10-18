# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**research-os** is a Claude Code dual-plugin ecosystem that separates research planning from engineering implementation. It provides two independent, marketplace-compatible plugins that can be used individually or together.

The repository implements **two specialized plugins**:

### Researcher Plugin (`plugins/researcher/`)
- **5 research-focused agents** for hypothesis development and planning
- **1 command** (`/plan-research`) for comprehensive research documentation
- **Output**: Research documentation in `research-os/project/`
- **Focus**: Research hypothesis, literature review, experiment planning

### Engineer Plugin (`plugins/engineer/`)
- **12 engineering agents** organized across specification, implementation, and verification
- **3 commands** (`/new-artifact`, `/create-artifact`, `/implement-artifact`)
- **Output**: Implemented artifacts in `research-os/artifacts/YYYY-MM-DD-*/`
- **Focus**: Professional spec-driven development with verification

## Architecture & Workflow

The dual-plugin system separates research planning from engineering implementation:

### Researcher Plugin Workflow
```
RESEARCH PLANNING → Creates research-os/project/
├─ research-journal.md (iterative refinement history)
├─ related-work.md (literature review)
├─ mission.md (project mission and vision statement)
├─ roadmap.md (experiment phases with dependencies)
└─ tech-stack.md (technical requirements)
```

### Engineer Plugin Workflow
```
1. SPECIFICATION → Creates research-os/artifacts/YYYY-MM-DD-artifact-name/
   ├─ planning/
   │   ├─ initialization.md (raw idea)
   │   ├─ requirements.md (gathered requirements)
   │   └─ visuals/ (reference images)
   ├─ spec.md (detailed specification)
   └─ tasks.md (strategic task breakdown)

2. IMPLEMENTATION → Updates artifact folder with:
   └─ implementation/ (reports per task group)

3. VERIFICATION → Adds to artifact folder:
   └─ verification/ (verification reports)

4. FINAL OUTPUT → Complete documented implementation
```

### Integration Flow
Research outputs from the Researcher plugin can inform artifact development in the Engineer plugin, but each plugin operates independently.

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

### Researcher Plugin Commands
```bash
/plan-research
```
Initiates comprehensive research planning workflow. Creates `research-os/project/` with:
- Research journal (iterative refinement)
- Related work analysis
- Mission statement (project vision and goals)
- Experiment roadmap
- Technical stack documentation

### Engineer Plugin Commands
```bash
/new-artifact [feature-description]
```
Initializes a new artifact specification in `research-os/artifacts/YYYY-MM-DD-artifact-name/`.
- Gathers requirements through targeted questions
- Processes visual assets if provided
- Creates planning documentation

```bash
/create-artifact
```
Generates detailed specification and task breakdown from gathered requirements.
- Analyzes requirements and context
- Creates comprehensive spec.md
- Generates strategic tasks.md with agent assignments

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

## Implementation Specialists (Engineer Plugin)

The Engineer plugin includes 5 specialized implementers, each with defined areas:

- **api-engineer**: API endpoints, controllers, business logic, request/response
- **database-engineer**: Migrations, models, schemas, database queries
- **ui-designer**: UI components, layouts, styling, responsive design
- **testing-engineer**: Test files, test coverage, fixtures
- **prompt-engineer**: Agentic workflows, orchestration, sub-agent prompts

## File Conventions

### Research Outputs
- Always create in `research-os/project/`
- Use standard filenames: research-journal.md, related-work.md, mission.md, roadmap.md, tech-stack.md

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

#### For Researcher Plugin
1. Create agent definition in `plugins/researcher/agents/`
2. Follow YAML frontmatter pattern
3. Focus on research-oriented capabilities
4. Update plugin.json if needed

#### For Engineer Plugin
1. Create agent definition in `plugins/engineer/agents/`
2. Follow YAML frontmatter pattern
3. Define clear areas of specialization
4. Place in appropriate subdirectory (specification/, implementers/, verifiers/)

### Adding New Commands

#### For Researcher Plugin
1. Create command in `plugins/researcher/commands/`
2. Focus on research workflow phases
3. Delegate to research agents via Task tool
4. Output to `research-os/project/`

#### For Engineer Plugin
1. Create command in `plugins/engineer/commands/`
2. Define phase-based workflow (spec/implement/verify)
3. Delegate to engineering agents via Task tool
4. Output to `research-os/artifacts/`

### Extending the Plugins
- **Researcher Plugin**: Add more research methodologies, literature review tools, hypothesis validation
- **Engineer Plugin**: Add more implementation specialists, verification frameworks, or domain-specific agents
- **Both**: Maintain clear separation of concerns between research and engineering

## Current State

The system is fully functional with two production-ready plugins:

### Researcher Plugin
- **Status**: Production-ready
- **Agents**: 5 research-focused agents
- **Command**: `/plan-research`
- **Output**: Comprehensive research documentation
- **Use Case**: Research planning, hypothesis development, literature review

### Engineer Plugin
- **Status**: Production-ready
- **Agents**: 12 engineering agents across 3 phases
- **Commands**: `/new-artifact`, `/create-artifact`, `/implement-artifact`
- **Output**: Implemented code with specifications
- **Features**: Standards enforcement, automatic code checking (ruff), verification framework

## Dual-Plugin Integration

### Using Plugins Together
While each plugin operates independently, they can be used sequentially:

1. **Research First** (Researcher Plugin):
   - Run `/plan-research` to develop research hypothesis
   - Generate roadmap and technical requirements
   - Document experiment phases

2. **Then Implement** (Engineer Plugin):
   - Use `/new-artifact` to start implementation
   - Reference research outputs from `research-os/project/`
   - Build artifacts based on research roadmap

### Independent Usage
Each plugin can also be used standalone:
- **Researcher Only**: For pure research planning without implementation
- **Engineer Only**: For traditional software development with spec-driven approach

### File Organization
- **Research outputs**: `research-os/project/`
- **Engineering artifacts**: `research-os/artifacts/YYYY-MM-DD-*/`
- **User standards**: `~/.research-os/standards/` (customizable)

## Ressources

To fully understand how the marketplace, plugin and components (slash commands, hooks, subagents and skills) work, check out

https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
https://docs.claude.com/en/docs/claude-code/plugins-reference
https://docs.claude.com/en/docs/claude-code/slash-commands
https://docs.claude.com/en/docs/claude-code/sub-agents
https://docs.claude.com/en/docs/claude-code/skills
https://docs.claude.com/en/docs/claude-code/hooks