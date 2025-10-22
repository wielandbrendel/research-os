# Research-OS

**An agentic research engineering ecosystem for Claude Code**

Research-OS is an orchestration system built on top of Claude Code that combines rigorous research planning with spec- and test-driven engineering. It provides a structured workflow for transforming research ideas into fully implemented, production-ready code through spec- and test-driven development principles with sophisticated context engineering.

## Overview

Research-OS separates the cognitive work of research planning from the execution work of engineering implementation through two specialized, marketplace-compatible plugins that can be used independently or together:

- **Researcher Plugin**: Focuses on hypothesis development, literature review, and experiment planning
- **Engineer Plugin**: Handles spec-driven development with implementation and verification workflows

This separation enables:
- Clear distinction between "what to build" (research) and "how to build it" (engineering)
- Reusable research artifacts that inform multiple implementations
- Professional development practices with automated verification
- Sophisticated context engineering through standards and templates

## Key Features

### 🔬 Research-First Development
- Systematic hypothesis refinement and validation
- Comprehensive literature review and related work analysis
- Experiment roadmap with dependency tracking
- Mission-driven project planning

### 🏗️ Spec-Driven Implementation
- Requirements gathering with visual asset support
- Detailed specification generation
- Strategic task breakdown with agent assignments
- Automated verification and testing

### 🤖 Multi-Agent Orchestration
- 19 specialized agents across research and engineering domains
- Intelligent task delegation based on agent expertise
- Parallel execution for independent tasks
- Context passing between agents via file artifacts

### 📐 Standards & Quality
- Customizable coding standards and conventions
- Automatic code quality checks (via ruff)
- Test-driven development support
- Comprehensive documentation at every phase

## Installation

Research-OS is compatible with the Claude Code marketplace and plugin system. Add this marketplace to Claude Code:

```bash
/plugin marketplace add wielandbrendel/research-os
```

Then browse and install individual plugins (commands or agents):

```bash
/plugin
```

For more details on the Claude Code plugin system, see the [official documentation](https://docs.claude.com/en/docs/claude-code/plugins)

## Usage

### Phase 0: Idea Brainstorming (Optional but Recommended)

Start by brainstorming and refining your initial research idea:

**Step 1:** Create `research-os/project/idea.md` with your initial research concept:
```markdown
# Initial Research Idea

[Your research idea, hypothesis, or problem statement]
```

**Step 2:** Run the brainstorm command:
```bash
/brainstorm
```

This iterative refinement command will:
1. **Assess your idea**: Perform extensive related work research and create a critical assessment
2. **Refine the assessment**: Verify claims and focus on substantive concerns
3. **Present key questions**: Extract the 3 most crucial questions with context and potential approaches
4. **Update your idea**: Incorporate your responses to improve `idea.md`

Output is created in `research-os/project/`:
- `idea.md` - Your refined research idea (updated after each iteration)
- `assessment.md` - Critical assessment with strengths, weaknesses, and recommendations
- `research-journal.md` - Related work exploration and searches

**Iterate:** Run `/brainstorm` multiple times to progressively refine your research concept. Each iteration deepens the analysis and sharpens the focus.

When satisfied with your refined idea, proceed to full research planning with `/plan-research`.

### Phase 1: Research Planning

Develop your comprehensive research vision with the Researcher plugin:

```bash
/plan-research
```

This comprehensive command will:
1. Guide you through iterative hypothesis refinement
2. Research related work and existing solutions
3. Create a compelling mission statement
4. Generate an experiment roadmap with phases
5. Document technical requirements

Output is created in `research-os/project/`:
- `research-journal.md` - Iterative refinement history
- `related-work.md` - Literature review and analysis
- `mission.md` - Project vision and goals
- `roadmap.md` - Phased experiment plan
- `tech-stack.md` - Technical requirements

### Phase 2: Engineering Implementation

Use the Engineer plugin to implement your research vision:

#### 1. Initialize a new artifact
```bash
/new-artifact [feature-description]
```
- Gathers requirements through targeted questions
- Processes visual references if provided
- Creates initial planning documentation

#### 2. Create detailed specifications
```bash
/create-artifact
```
- Analyzes requirements and context
- Generates comprehensive `spec.md`
- Creates strategic `tasks.md` with agent assignments

#### 3. Implement the artifact
```bash
/implement-artifact
```
- Delegates to specialized implementation agents
- Executes tasks in parallel where possible
- Runs verification workflows
- Produces implementation reports

Output is organized in `research-os/artifacts/YYYY-MM-DD-artifact-name/`:
```
├── planning/
│   ├── initialization.md    # Raw idea capture
│   ├── requirements.md      # Gathered requirements
│   └── visuals/            # Reference images
├── spec.md                  # Detailed specification
├── tasks.md                 # Task breakdown with assignments
├── implementation/          # Implementation reports per task
└── verification/           # Verification reports
```

## Agent Ecosystem

### Researcher Plugin Agents (7)
- **idea-assessment**: Critical assessment of research ideas with extensive related work analysis
- **assessment-refiner**: Meta-analysis and refinement of research assessments for maximum utility
- **gather-research-info**: Iterative research hypothesis development
- **create-research-mission**: Mission statement and vision crafting
- **create-experiment-roadmap**: Experiment planning with dependencies
- **document-tech-stack**: Technical requirements documentation

### Engineer Plugin Agents (12)

#### Specification Agents (5)
- **spec-initializer**: Project initialization and setup
- **spec-researcher**: Requirements gathering and analysis
- **spec-writer**: Detailed specification creation
- **spec-verifier**: Specification validation
- **task-list-creator**: Strategic task breakdown

#### Implementation Specialists (5)
- **api-engineer**: API endpoints, controllers, business logic
- **database-engineer**: Migrations, models, schemas
- **ui-designer**: UI components, styling, responsive design
- **testing-engineer**: Test files, coverage, fixtures
- **prompt-engineer**: Agentic workflows, orchestration

#### Verification Agents (2)
- **backend-verifier**: Database and API validation
- **frontend-verifier**: UI/UX verification
- **implementation-verifier**: End-to-end verification

## Standards & Customization

Research-OS uses a sophisticated standards system that can be customized per user or project.

### Default Standards Location
The Engineer plugin includes default standards in `plugins/engineer/standards/`:
- `global/` - Coding style, conventions, error handling
- `testing/` - Unit tests, coverage requirements

### User Customization
Create your own standards in `~/.research-os/standards/`:

```bash
~/.research-os/standards/
├── global/
│   ├── coding-style.md
│   ├── conventions.md
│   ├── error-handling.md
│   └── tech-stack.md
└── testing/
    ├── coverage.md
    └── unit-tests.md
```

### How Standards Work
1. **Automatic Copying**: When initializing a new project, standards from `~/.research-os/standards/` are automatically copied as a starting point
3. **Project-Specific**: Each project can modify its local standards without affecting global defaults
4. **Inheritance**: Projects start with user standards, falling back to plugin defaults if not customized

## Workflow Examples

### Example: Building a Research Tool
```bash
# Phase 0: Brainstorming (Optional but Recommended)
# Create research-os/project/idea.md with initial concept
/brainstorm
# Performs critical assessment with related work analysis
# Presents 3 key questions with potential approaches
# Refines research-os/project/idea.md based on your responses
# (Can iterate multiple times)

# Phase 1: Research Planning
/plan-research
# Develops hypothesis for novel visualization approach
# Researches existing tools and methods
# Creates roadmap for validation experiments

# Phase 2: Implementation
/new-artifact interactive-visualization-dashboard
# Gathers specific requirements
# Processes mockups and wireframes

/create-artifact
# Generates detailed specs
# Creates task breakdown

/implement-artifact
# Implements with specialized agents
# Verifies functionality
```

## Architecture Benefits

### Separation of Concerns
- **Research Phase**: Focus on "what" and "why"
- **Engineering Phase**: Focus on "how" and implementation details
- **Clear handoff points** between phases via documented artifacts

### Context Engineering
- **Templates**: Reusable workflows and patterns
- **Standards**: Consistent coding practices across projects
- **File Artifacts**: Explicit context passing between agents
- **Documentation**: Comprehensive records at every step

### Quality Assurance
- **Spec-Driven**: Implementation follows detailed specifications
- **Test-Driven**: Testing requirements defined upfront
- **Verification**: Automated checks at multiple levels
- **Code Quality**: Automatic linting and formatting (ruff)

## Advanced Features

### Hooks System
Both plugins support Claude Code hooks for automation:
- **File creation hooks**: Trigger on new file creation
- **Code checking hooks**: Run ruff on Python files
- **Custom workflows**: Extensible hook system

### Parallel Execution
- Independent tasks run concurrently
- Intelligent scheduling based on dependencies
- Optimized for multi-agent workflows

### Visual Asset Processing
- Support for mockups and wireframes
- Image analysis for UI requirements
- Reference storage in planning directories

## Contributing

Research-OS is designed to be extended. You can:

### Add New Agents
1. Create agent definition in appropriate plugin's `agents/` directory
2. Follow YAML frontmatter pattern
3. Define clear specialization areas
4. Update plugin.json if needed

### Add New Commands
1. Create command in plugin's `commands/` directory
2. Define phase-based workflow
3. Delegate to appropriate agents
4. Maintain separation between research and engineering

### Extend Standards
1. Add new standard categories in `~/.research-os/standards/`
2. Agents will automatically reference them
3. Share standard sets with your team

## Philosophy

Research-OS embodies several key principles:

1. **Research Before Implementation**: Think deeply before coding
2. **Specification as Contract**: Clear specs prevent scope creep
3. **Agent Specialization**: Each agent excels in its domain
4. **Documentation as First-Class**: Every decision is documented
5. **Standards Enable Scale**: Consistency across projects
6. **Verification Builds Trust**: Automated checks ensure quality

## Support

- **Documentation**: Built-in CLAUDE.md provides detailed guidance
- **Issues**: Report bugs at [github.com/wielandbrendel/research-os/issues](https://github.com/wielandbrendel/research-os/issues)
- **Claude Code Help**: Use `/help` in Claude Code interface
- **Plugin Documentation**: See [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code/plugins)

## License

[Add appropriate license information]

---

Built with ❤️ for the Claude Code ecosystem.