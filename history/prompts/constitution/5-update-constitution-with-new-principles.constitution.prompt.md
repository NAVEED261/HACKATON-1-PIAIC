---
id: 5
title: Update Constitution with New Principles
stage: constitution
date: 2025-12-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: update @.specify/memory/constitution.md and improve it:### Subsystem Ownership... (truncated)
labels: ["constitution", "spec-kit-plus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

---

## Prompt

update @.specify/memory/constitution.md and improve it:### Subsystem Ownership
Each subsystem fully owns:
- Its own spec, plan, tasks, implementation docs
- Its own app folder (if applicable)
- Its own CLI scripts and ingestion processes
- Its own ADRs and change log

Subsystems may not modify each other’s files without updating specs and ADRs.
### RAG Safety Rule
The RAG chatbot MUST only answer using the textbook dataset.
If the answer is outside the book scope, it must say:
“I don't have enough context in the textbook to answer this.”

## Response snapshot

Constitution updated to version 1.1.0 (Minor bump: Added "Subsystem Ownership" and "RAG Safety Rule" principles).

**Manual follow-up required:**
Please update the following files to align with the new principles defined in `constitution.md`:
*   `.specify/templates/plan-template.md`
*   `.specify/templates/spec-template.md`
*   `.specify/templates/tasks-template.md`
*   `.specify/templates/commands/sp.constitution.md`
*   `.specify/templates/commands/sp.phr.md`
*   `.specify/templates/commands/sp.specify.md`
*   `.specify/templates/commands/sp.plan.md`
*   `.specify/templates/commands/sp.tasks.md`
*   `.specify/templates/commands/sp.implement.md`
*   `.specify/templates/commands/sp.git.commit_pr.md`
*   `.specify/templates/commands/sp.analyze.md`
*   `.specify/templates/commands/sp.adr.md`
*   `.specify/templates/commands/sp.checklist.md`
*   `.specify/templates/commands/sp.clarify.md`
*   `CLAUDE.md`

**Suggested commit message:**
`docs: feat(constitution): Add Subsystem Ownership and RAG Safety Rule principles (v1.1.0)`

## Outcome

- ✅ Impact: Project constitution updated successfully with new principles and version, summary provided to user.
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Waiting for user to acknowledge or provide further instructions.
- 🧠 Reflection: Successfully processed the user's request to update the constitution, added the specified principles, updated versioning, and outlined necessary follow-up for template alignment.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
