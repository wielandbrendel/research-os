## Make Research Presentation Slides

You are orchestrating a comprehensive workflow to create a professional research presentation. This command guides the user through information gathering, outline creation, refinement, review, and final slide generation.

---

## PHASE 1: Information Gathering & Setup

### Step 1.1: Check for Existing Presentations

First, check if any presentations already exist in `research-os/presentations/`:

```bash
ls -la research-os/presentations/ 2>/dev/null || echo "No presentations directory exists yet"
```

If presentations exist:
- List them clearly to the user
- Use the **AskUserQuestion** tool to ask: "I found existing presentations. Would you like to:"
  - Option 1: "Edit an existing presentation" (user will then specify which one)
  - Option 2: "Copy an existing presentation as starting point" (user will then specify which one)
  - Option 3: "Start from scratch"

If the user chooses Option 1 or 2, they should provide the folder name in their "Other" response.

### Step 1.2: Gather Presentation Parameters

Use the **AskUserQuestion** tool to collect essential information. Ask ALL of these questions unless the user has already provided this information in their initial argument ($ARGUMENTS). Do not ask these questions all at once, but go through each question one-by-one and use the **AskUserQuestion** tool to collect the answer.

**Question 1 - Audience Background**:
- Header: "Audience"
- Question: "Who will be attending this presentation?"
- Options:
  - "General public" → "Non-experts with no domain knowledge; focus on impact and intuition"
  - "Domain researchers" → "Conference or workshop attendees from diverse backgrounds within the field"
  - "Specialists" → "Experts already proficient in this specific research area"
  - "Mixed audience" → "Combination of experts and non-experts"
- multiSelect: false

**Question 2 - Talk Length**:
- Header: "Duration"
- Question: "How long is the presentation (in minutes)?"
- Options:
  - "4-5 minutes" → "Lightning talk"
  - "5-10 minutes" → "Pitch talk or brief update"
  - "15-20 minutes" → "Standard conference talk"
  - "30-45 minutes" → "Invited talk or detailed seminar"
  - "60+ minutes" → "Lecture, tutorial, or thesis defense"
- multiSelect: false

**Question 3 - Talk Format**:
- Header: "Format"
- Question: "What is the main format / direction of the talk?"
- Options:
  - "Informal talk" → "More informal talks in research labs"
  - "Conference talk" → "Standard conference talk"
  - "Pitch" → "Short pitch event for scientific audiences"
  - "Science Slam" → "Science slam talk for general audiences"
  - "Public Lecture" → "Longer public presentations for general audiences"
  - "Children's Lecture" → "A presentation for younger children"
  - "60+ minutes" → "Lecture or tutorial"
- multiSelect: false

**Question 4 - Presentation Focus**:
- Header: "Focus"
- Question: "What should the presentation emphasize?"
- Options:
  - "Wider impact" → "Emphasize motivation, applications, and real-world significance"
  - "Technical details" → "Focus on methodology, implementation, and technical contributions"
  - "Overall results" → "Highlight findings, experiments, and quantitative outcomes"
  - "Vision and motivation" → "Stress the big picture, problem importance, and future potential"
- multiSelect: true

**Question 5 - Presentation Name** (optional):
- Header: "Name"
- Question: "What should we name this presentation folder? (Leave blank to auto-generate from project name)"
- Options:
  - "Auto-generate" → "Use general format (pitch, keynote, conference oral, informal talk)"
  - "Custom name" → "User will provide name in Other field"
- multiSelect: false

### Step 1.3: Create Presentation Directory

Based on the user's responses:

1. Determine the presentation folder name:
   - If user provided a custom name: use it (sanitize: lowercase, replace spaces with hyphens)
   - If user chose "Edit existing": use the existing folder path they provided
   - If user chose "Copy existing": create new folder with today's date + name variant
   - If auto-generate: use the general format (pitch, keynote, conference oral, informal talk) for naming the folder

2. Create the directory structure:
```
research-os/presentations/{YYYYMMDD}_{presentation_name}/
```

Where `{YYYYMMDD}` is today's date and `{presentation_name}` is the determined name.

3. If the user chose "Copy existing", copy the contents of the existing presentation folder into the new folder.

4. Confirm to the user:
```
Created presentation folder: research-os/presentations/{YYYYMMDD}_{presentation_name}/

Proceeding with:
- Audience: {audience}
- Duration: {length} minutes
- Focus: {focus_areas}
```

---

## PHASE 2: Generate Initial Outline

Use the **Task** tool to launch the `presentation-outline-architect` agent with the following prompt:

```
Create a comprehensive presentation outline for research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md.

Context:
- Goal: {infer from focus areas, e.g., "conference talk emphasizing technical details"}
- Audience: {audience from Phase 1}
- Length: {length from Phase 1} minutes

Please analyze the entire research-os/project/ directory (idea.md, mission.md, roadmap.md, related_work.md) and any available artifacts in research-os/artifacts/ to understand the project stage and available results.

Create a slide-by-slide outline that:
1. Matches the audience sophistication level
2. Fits within the time constraint
3. Emphasizes: {focus_areas from Phase 1}
4. Automatically detects project maturity (early/mid/late stage) and adapts the narrative accordingly

Save the output to research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md.
```

**Important**: Pass the gathered parameters (goal, audience, length) clearly to the agent.

Wait for the agent to complete before proceeding.

---

## PHASE 3: Refine the Outline

Use the **Task** tool to launch the `presentation-outline-reviewer` agent with the following prompt:

```
Review and improve the presentation outline at research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md.

Please:
1. Analyze the outline for clarity, storyline, and climax positioning
2. Review the project context in research-os/project/ to ensure accurate representation
3. Enhance visual elements and narrative flow
4. Maximize the presentation's impact for a {audience} audience with focus on {focus_areas}

Rewrite research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md with your improvements.

Focus on:
- Strong opening hook
- Clear narrative arc with strategic climax
- Specific visual recommendations (diagrams, charts, images)
- Smooth transitions between sections
- Memorable conclusion
```

Wait for the agent to complete before proceeding.

---

## PHASE 4: User Review Checkpoint

After the outline has been refined, present a summary to the user:

```markdown
## Presentation Outline Complete

I've created and refined a presentation outline for you:

**Location**: `research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md`

**Summary**:
- Total slides: {estimated_slide_count}
- Structure: {brief_narrative_description}
- Visual elements: {count_of_diagrams/charts/images}
- Key climax: {main_result_or_insight_highlighted}

**Next Step**:

Please review the outline at the path above. Once you're satisfied with the structure and content, I'll generate the actual presentation slides using the pptx skill.

Would you like to:
1. Review the outline and let me know if any changes are needed
2. Proceed directly to slide generation
3. Make specific edits before generation
```

Use the **AskUserQuestion** tool:
- Header: "Next Step"
- Question: "How would you like to proceed?"
- Options:
  - "Generate slides now" → "Proceed to Phase 5 immediately"
  - "I need to review first" → "Wait for user to review and provide feedback"
  - "Make specific changes" → "User will describe changes in Other field"
- multiSelect: false

**If user requests changes**:
- Make the requested edits to `outline.md`
- Ask again if they're ready to generate slides

**If user chooses "Generate slides now"**:
- Proceed to Phase 5

---

## PHASE 5: Generate Presentation Slides

Once the user approves the outline, use the **Skill** tool to invoke the pptx skill and ULTRATHINK:

```
Use the pptx skill to generate a professional presentation from research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md.

Instructions for the pptx skill:
1. Read the outline.md file carefully
2. Create slides following the structure exactly
3. For each slide:
   - Pull referenced images from artifacts/ directories
   - Generate charts and diagrams as specified
   - Create graphics for visual elements (no placeholders!)
4. Apply professional formatting appropriate for research presentations
5. Save the final presentation as research-os/presentations/{YYYYMMDD}_{presentation_name}/presentation.pptx

Context: This is a {length}-minute {audience} presentation focusing on {focus_areas}.
```

**Important**:
- NO PLACEHOLDERS for visuals - all diagrams and charts must be generated
- Pull all images directly from artifact paths specified in outline.md
- Ensure visual quality is publication-ready

---

## PHASE 6: Completion Message

Once slides are generated, display:

```markdown
## Presentation Complete!

Your research presentation has been created:

**Files created**:
✓ research-os/presentations/{YYYYMMDD}_{presentation_name}/outline.md
✓ research-os/presentations/{YYYYMMDD}_{presentation_name}/presentation.pptx

**Presentation details**:
- Duration: {length} minutes
- Audience: {audience}
- Focus: {focus_areas}
- Total slides: {count}

**Next steps**:
1. Open the .pptx file and review the slides
2. Practice your delivery timing
3. Customize any visuals or animations as needed
4. Run /make-slides again if you want to create a variant (e.g., shorter version, different audience)

The presentation is ready for your review!
```

---

## Important Notes

### Directory Checking
Before any phase that references `research-os/project/`, verify these files exist:
- If `research-os/project/idea.md` or `research-os/project/mission.md` don't exist, inform the user:
  ```
  No research project found. Please run /plan-research first to establish your project,
  or create research-os/project/idea.md with your research concept.
  ```

### Error Handling
- If agents fail, provide clear error messages and suggest troubleshooting steps
- If the pptx skill encounters missing assets, list them and ask user how to proceed
- If existing presentation folders are corrupted or incomplete, offer to start fresh

### Flexibility
- Users can exit at any phase and resume later
- The outline.md file can be manually edited between Phase 3 and Phase 5
- Multiple presentations can be created from the same project

---

## Design Philosophy

This command follows a **human-in-the-loop** approach:
1. Gather requirements explicitly (no defaults)
2. Let specialized agents do deep work autonomously
3. Provide a review checkpoint before expensive operations
4. Deliver production-ready output

The workflow balances automation with user control, ensuring the final presentation aligns with the researcher's vision while leveraging AI for structure, refinement, and generation.
