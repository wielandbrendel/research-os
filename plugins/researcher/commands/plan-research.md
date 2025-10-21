## Research Planning Process

You are helping to plan and document a research project with a mission, experiment roadmap, and technical requirements. This will include:

- **Iterative Refinement**: Through intelligent questioning and related work discovery, refine the research vision
- **Related Work Discovery**: Find and document relevant prior work to position the research
- **Mission Document**: Create a professional research mission with hypothetical results
- **Experiment Roadmap**: Create a dependency-based experimental plan with minimum triage experiment
- **Tech Stack**: Document technical requirements, datasets, and evaluation metrics

This process will create these files in `research-os/project/` directory.

After each phase (described below), stop the process and wait for the user to explicitly allow you to continue.
When you start a new phase, read the generated files from previous phases again to make sure that no changes by the user have been overlooked.

### PHASE 1: Iterative Research Refinement & Related Work Discovery

Use the **@gather-research-info** subagent to iteratively refine the research idea and create comprehensive documentation.

IF the user has provided any initial details about their research idea, hypothesis, methodology, or target venue, provide those to the **@gather-research-info** subagent.

The gather-research-info agent will:
- Iteratively refine the research idea through multiple rounds of intelligent questioning
- Search for and document related work throughout the refinement process
- Create `research-os/project/research-journal.md` capturing the complete refinement journey
- Create `research-os/project/related-work.md` consolidating all discovered literature

Stop and ask the user if the generated content is all right.

### PHASE 2: Create Research Mission

Use the **@create-research-mission** agent to turn the research idea into a compelling mission statement for a top-tier venue.

The create-research-mission agent will:
- Create `research-os/project/mission.md` with positioned mission and hypothetical results

Stop and ask the user if the generated content is all right.

### PHASE 3: Create Experiment Roadmap

The create-experiment-roadmap agent will:
- Create `research-os/project/roadmap.md` with experiment dependencies and minimum triage experiment

### PHASE 4: Document Technical Stack

The document-tech-stack agent will:
- Create `research-os/project/tech-stack.md` documenting frameworks, datasets, and metrics

Stop and ask the user if the generated content is all right.

### PHASE 5: Final Validation

Verify all files created successfully:

```bash
# Validate all research planning files exist
for file in research-journal.md related-work.md mission.md roadmap.md tech-stack.md; do
    if [ ! -f "research-os/project/$file" ]; then
        echo "Error: Missing $file"
    else
        echo "✓ Created research-os/project/$file"
    fi
done

echo "Research planning complete! Review your research documentation in research-os/project/"
```

### PHASE 6: Display Results

Display to the user:
- Confirmation of files created
- Summary of the research vision and differentiation
- Overview of experiment phases with minimum triage experiment
- Key related work identified

Output to user:

"Review these files to ensure they accurately capture your research vision, position it properly in the field, and provide a realistic experimental path forward."

## Output

Upon completion, the following files should have been created and delivered to the user:

- `research-os/project/research-journal.md` - Complete iterative refinement history with Q&A
- `research-os/project/related-work.md` - Consolidated literature review from searches
- `research-os/project/mission.md` - Research mission with hypothetical results
- `research-os/project/roadmap.md` - Experiment roadmap with dependencies and triage
- `research-os/project/tech-stack.md` - Technical requirements and evaluation protocols