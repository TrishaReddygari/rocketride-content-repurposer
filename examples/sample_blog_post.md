# What I learned shipping my first open-source pull request

I'd read about open source for years. Forking, branching, "good first issues," `Fixes #123` — it all made sense in the abstract. The first time I actually opened a PR against a real project's `develop` branch, half of what I thought I knew turned out to be wrong, and the other half turned out to matter much more than I expected.

## The issue picker's paradox

The official advice is: "look for issues labeled `good first issue`." So I did — and found exactly one. The interesting bugs in the recent backlog all turned out to be either assigned to a maintainer or already had a draft PR linked. I wasted twenty minutes drafting a fix for one of them before noticing the linked PR. Lesson: in an active project, the labels are a starting point, not a source of truth. Always read the issue page itself — assignee field, linked PRs, recent comments — before you commit time to a fix.

## The "good first issue" was bigger than it looked

The one available issue was about adding a Python formatter (ruff) to CI. It read like a chore: "run ruff, add a CI step." But once I dug in, the simple acceptance criteria expanded:

- The format pass touched 93 files. Not bad, but big enough that bundling unrelated lint fixes would have made the diff impossible to review.
- The CI workflow was actually three workflows that depended on each other through a "gatekeeper" job. Adding a check meant understanding that pattern, not just appending a step.
- The codebase had 480 *lint* violations on top of the formatting drift. Fixing all of them was tempting — and would have ballooned the PR into something nobody could safely merge.

The right move turned out to be: do the smallest mechanical change that fully solves the *formatting* part, document the *lint* part as a follow-up, and stop. Restraint reads as confidence in a PR review. Sprawl reads as inexperience.

## Three commits, not one

I split the work into three commits in one PR — format pass, CI step, docs update. It's tempting to lump everything into one big "do issue #432" commit, but smaller commits make reviewers' lives easier. They can skim the format pass (mechanical, low-risk) and look hard at the CI step (small, important). I noticed I read other people's PRs the same way.

## Author identity is a one-line gotcha

My first commit went out attached to `me@my-laptop.local` — git's default when you've never set a config. Useless: the commit wouldn't show up under my GitHub profile. I fixed it by setting `user.email` to GitHub's privacy-preserving noreply address (`12345678+username@users.noreply.github.com`) at the **repo level only**, then amending the commit. Two minutes of cleanup that, if I'd shipped it, would have been a small but visible footprint on my OSS history forever.

## What I'd do differently next time

Read every workflow file in `.github/workflows/` before designing my CI step. I added a job that lives at the top level of `ci.yml` and depends on a small subset of other jobs. That's clean. But I almost added it to a different workflow that fires on `pull_request_target` — which would have given my code GitHub's privileged token, and that's a security footgun I would not have understood until much later. Read the YAML. Understand what triggers what. Don't add steps to workflows you haven't traced end-to-end.

## The unglamorous part is the part that ships

Nothing in this PR is exciting. No new feature. No clever algorithm. Just: a formatter that should always have been running, and now is. That's most of what open source maintenance looks like up close. The exciting work gets the headlines; the unglamorous work is what keeps the project shippable.
