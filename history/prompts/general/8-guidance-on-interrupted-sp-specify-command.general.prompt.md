---
id: 8
title: Guidance on Interrupted sp.specify Command
stage: general
date: 2025-12-02
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 001-project-specification-physical
user: User
command: How do I complete the /sp.specify command if it was interrupted?
labels: ["troubleshooting", "custom-command", "interruption"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - D:\PIAIC HACKATON PRACTICE\hackaton_1\history\prompts\general\\8-guidance-on-interrupted-sp-specify-command.general.prompt.md
tests:

---

## Prompt

How do I complete the /sp.specify command if it was interrupted?

## Response snapshot

The official documentation for Claude Code does not provide specific guidance on how to complete an interrupted custom slash command like /sp.specify. The behavior of such a command upon interruption largely depends on its internal implementation.

To address an interrupted /sp.specify command, I recommend the following steps:

1.  **Examine the `spec.md` file:** Check the `specs/<feature>/spec.md` file (or the expected output file for your specification) to see if any partial content was generated before the interruption. If the content is incomplete or corrupted, you may need to manually clean it up.

2.  **Re-run the `/sp.specify` command:** Often, custom commands are designed to be re-runnable. Try executing `/sp.specify` again with the same arguments. Depending on its implementation, it might resume from where it left off or regenerate the specification from the beginning.

3.  **Investigate the command's definition:** Since `/sp.specify` is a project-specific custom command, its definition might be located within your project's files. You could look in directories like `.specify/commands/` or other configuration files that define project-specific slash commands. Reviewing the script or definition will provide insight into how it handles interruptions and state.

4.  **Check Prompt History Records (PHRs):** If a PHR was created before the interruption, it might contain a snapshot of the command's state or arguments used, which could be helpful for debugging or re-running.

If you find that custom commands in Claude Code lack robust interruption handling, you can use the `/feedback` command to report a feature request for improved resume capabilities.

## Outcome

- ✅ Impact: Provided guidance on handling interrupted custom command.
- 🧪 Tests: N/A
- 📁 Files: Read Claude Code docs map and PHR template. Attempted to glob for sp.specify implementation.
- 🔁 Next prompts: N/A
- 🧠 Reflection: Documentation lacks specific guidance for resuming interrupted custom commands; general troubleshooting provided.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A\n- Prompt variant (if applicable): N/A\n- Next experiment (smallest change to try): N/A\n