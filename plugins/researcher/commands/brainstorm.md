## Brainstorm Research Idea

You are helping to brainstorm and iteratively refine a research idea through critical assessment, related work analysis, and focused questioning. This command orchestrates a multi-phase workflow that:

- **Assesses the Idea**: Analyzes the initial idea with extensive related work research
- **Refines the Assessment**: Critically evaluates and improves the assessment to focus on key concerns
- **Engages the User**: Presents clarifying questions and incorporates responses
- **Updates the Idea**: Rewrites idea.md with improvements based on user feedback

This iterative process can be repeated multiple times to progressively refine the research concept.

### PHASE 1: Initial Idea Assessment

Use the **idea-assessment** agent to analyze the idea in `research-os/project/idea.md` and create a comprehensive assessment.

The idea-assessment agent will:
- Read the initial idea from `research-os/project/idea.md`
- Perform extensive related work searches
- Create `research-os/project/research-journal.md` documenting the exploration
- Create `research-os/project/assessment.md` with detailed critique and questions

**Important**: Ensure `research-os/project/idea.md` exists before starting. If it doesn't exist, inform the user:
```
Please create research-os/project/idea.md with your research idea first, then run /brainstorm again.
```

### PHASE 2: Assessment Refinement

Use the **assessment-refiner** agent to critically evaluate and improve the assessment.

The assessment-refiner agent will:
- Read `research-os/project/assessment.md`
- Verify claims and assertions through additional research
- Identify which concerns are substantive vs. minor distractions
- Rewrite `research-os/project/assessment.md` with a refined, focused assessment
- Prioritize the most critical questions and recommendations

### PHASE 3: Extract and Present Top Questions to User

After the refined assessment is complete:

1. Read `research-os/project/assessment.md`
2. Provide a short overall assessment (2-3 sentences)
2. Identify the **three most pressing and crucial questions** from the assessment that would have the greatest impact on improving and clarifying the research project
3. For each of the three questions, provide:
   - The question itself
   - Context explaining why this question is critical
   - A potential solution or answer based on the assessment and related work

4. Present these to the user in a clear, organized format:

```
## Assessment summary
[A short 2-3 sentence summary of the overall assessment. Be constructive but also very clear about potential shortcomings or unclear design decisions]

Based on the assessment, here are the three most crucial questions to refine your research idea:

## Question 1: [Question text]

**Why this matters:**
[Context explaining the importance and impact of this question - 2-3 sentences]

**Potential approach:**
[A concrete, actionable suggestion or potential answer based on the assessment and related work - 2-3 sentences]

## Question 2: [Question text]

**Why this matters:**
[Context explaining the importance and impact of this question]

**Potential approach:**
[A concrete, actionable suggestion or potential answer]

## Question 3: [Question text]

**Why this matters:**
[Context explaining the importance and impact of this question]

**Potential approach:**
[A concrete, actionable suggestion or potential answer]

---

Please provide your thoughts on these questions and the proposed approaches. Your responses will guide the refinement of your research idea.
```

5. Wait for the user to provide their responses to the questions.

### PHASE 4: Update research-os/project/idea.md with Refined Vision

Once the user provides their responses:

1. Read the current `research-os/project/idea.md`
2. Read the refined `research-os/project/assessment.md`
3. Incorporate the user's responses to the clarifying questions
4. Write an updated, more focused version of `research-os/project/idea.md` that:
   - Maintains the core vision but with greater clarity
   - Addresses the key concerns raised in the assessment
   - Integrates insights from the user's responses
   - Reflects a more refined understanding of positioning in the field
   - Includes specific improvements based on recommendations
   - Is focused and concise

The updated `research-os/project/idea.md` should be substantially improved while staying true to the original intent.

### PHASE 5: Completion Message

Display to the user:

```
Your idea has been refined based on the assessment and your responses!

The following files have been updated:
✓ research-os/project/idea.md (refined research idea)
✓ research-os/project/assessment.md (critical assessment)
✓ research-os/project/research-journal.md (related work exploration)

You can now:
1. Review the updated research-os/project/idea.md to see the refined version
2. Run /brainstorm again for another iteration of refinement
3. When satisfied with the idea, run /plan-research to create a full research plan

Each iteration of /brainstorm will deepen the analysis and sharpen the focus.
```

## Output

Upon completion of one brainstorm iteration, the following files should have been created/updated:

- `research-os/project/idea.md` - Refined research idea incorporating feedback and user responses
- `research-os/project/assessment.md` - Refined critical assessment with prioritized concerns
- `research-os/project/research-journal.md` - Documentation of related work exploration

The user can then iterate by running `/brainstorm` again, which will reassess the refined idea and continue the improvement cycle.
