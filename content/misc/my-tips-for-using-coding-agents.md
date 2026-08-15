---
title: "My Tips for Using Coding Agents"
date: 2025-09-28
slug: "my-tips-for-using-coding-agents"
aliases:
  - /blog/my-tips-for-using-coding-agents
summary: "A few practices that make working with coding agents more efficient."
---

As I progress in my PhD studies in Information Systems, my coding work keeps
getting more diverse. It spans data processing, regression analysis, web-based
dynamic experiments, and LLM fine-tuning. Many of these would have taken a
tremendous amount of time to learn before the age of LLMs. Thanks to coding
agents, things are much easier now.

However, coding agents are far from perfect. I have spent too much time
debugging. Over time, I have learned some practices that make the work more
efficient. I wrote this post to summarize a few tips that help me. I am not
claiming originality; I learned them from many places (e.g., Ethan Mollick's
posts).

**Use an AI agent instead of a web-based LLM.** The ability to look up scripts
in large codebases and modify them directly makes an agent much more useful
than a web-based LLM (e.g., ChatGPT). I use Cursor and find it good.

**Check intermediate steps.** Large codebases take too long to read line by
line. Blind trust is also a mistake. I take a results-driven approach. I print
important intermediate steps and examine them.

**Use another LLM to inspect the code.** This builds on the previous point. Ask
a second LLM to outline the logic of the script and review it. Many times you
will find the agent added something you do not want.

**When bugs stick, print more and loop.** Some bugs take many iterations. When
that happens, I ask the agent to add more debugging prints. Then I ask it to
fix the issue by reading those prints.

**Reset when the context gets long.** Do not underestimate the performance drop
when the context grows. I typically start a new window when about 40% of the
context window is used.

**Read source code before you customize.** This is especially useful when
modifying functions embedded in large packages (e.g., a Trainer package
designed to fine-tune LLMs like `trl.GRPOTrainer`). Direct modification can
cause inconsistency and lead to bugs. I ask the agent to inspect the source
code and explain the structure. Then I ask for targeted revisions.

**Expect change!** AI evolves. Many of these tips will matter less. That is a
good thing. I hope that day arrives soon. :)
