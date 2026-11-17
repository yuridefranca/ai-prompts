# explain-task — HTML format

Adapted from [src-duelbits/skills/explain-task/FORMAT.md](../../../src-duelbits/skills/explain-task/FORMAT.md) — the mobile-first HTML spec is unchanged; only the repo-specific examples (stack names, ticket prefix) are generalized.

One long page. No tabs for top-level structure. Self-contained: CSS and JavaScript inline, images as data URIs.

Write with the clarity and flow of Martin Kleppmann, making it engaging and written in classic style. Transitions between sections should be smooth.

## Mobile-first

The phone is the primary surface. Desktop can get wider type; nothing may require hover or a wide canvas.

- `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Body text ≥ 16px; line-height ~1.5; max-width ~40rem; padding that survives a thumb
- Quiz options and in-page links: tap target ≥ 44px
- Images: `max-width: 100%; height: auto`
- Stage rail: wrap, don't horizontally scroll
- Sticky top bar: feature slug + current stage only
- Color contrast sufficient for outdoor reading

## Page skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{feature slug}: {one-line title}</title>
  <style>/* inline CSS */</style>
</head>
<body>
  <!-- artifact-status header as an HTML comment — see ../../schemas/artifact-status.md § Non-markdown artifacts -->
  <header class="top">
    <p class="kicker">{feature slug} · {stage} · {date}</p>
    <h1>{The problem, in one line}</h1>
  </header>
  <nav class="stages" aria-label="Workspace progress"><!-- six stages --></nav>
  <nav class="toc"><!-- jump links --></nav>
  <main>
    <!-- sections below -->
  </main>
  <script>/* quiz + details helpers */</script>
</body>
</html>
```

The `{feature slug}` is `INDEX.md`'s `feature:` field — not a ticket ID, since the flows don't assume a specific tracker.

## Sections (in order)

1. **Where we are** — six-stage rail + one sentence on the next step (first run: confirm an approach, not implementation).
2. **How this codebase works here** — skippable `<details>` for readers who already know the area. Source: `AGENTS.md`, `.ai-rules/project.md`, or direct exploration.
3. **The problem** — who feels it, what is wrong, why this change exists. Toy data. No class names.
4. **What it looks like** — **Problem** screenshots, then **Current** screenshots (today's product). HTML phone-frame if a capture is missing. Caption every figure Problem / Current / Proposed.
5. **Ways we can solve it** — each alternative in simple terms so the reader can check the logic. If more than one exists, list them, mark Recommended, and wait. Proposed screenshots live here, not in Current.
6. **Watch outs** — required. Logic flaws, business impact, other features. Helps pick an alternative. See below.
7. **Code** — omit until an approach is confirmed **and** the stage is **Build** (phase 6.x). Then a high-level walkthrough grouped so a new joiner can follow, not a file-by-file diff. Use `<pre>` (see Code blocks).
8. **Quiz** — five interactive multiple-choice questions.
9. **Next step** — first run: "Which approach should we take?" Later: reflects whichever flow phase comes next.

Use callouts (a styled `<aside>`) for definitions, edge cases, and "if this is missing we cannot know X".

## Diagram families

Pick a small number and reuse them. No ASCII diagrams. Simple HTML/CSS only.

1. **Person journey** — user, this repo's system, any third party, as labeled cards with arrows and example values.
2. **Stack hop** — the repo's own request→service→persistence chain (or event chain). At phase 0.5 this is your best guess before `3.0-component-map.md`/`3.2-data-flow.md` exist; redraw accurately once they do (Clarify update). Highlight the hop this change touches; keep the rest muted.
3. **Phone frame** — a simplified UI the user would see. Use it when a design export or browser capture is unavailable, and as a caption overlay when it is.

System diagrams must include example data, not empty boxes.

## Ways we can solve it

Place this immediately after **What it looks like**. Each alternative is an `<article>`:

```html
<section id="approaches">
  <h2>Ways we can solve it</h2>
  <p>Check the logic here before any code.</p>
  <article class="approach-card recommended">
    <p class="kicker">Recommended</p>
    <h3>{Name the approach without a class name}</h3>
    <p><strong>What would change.</strong> {for the user}</p>
    <p><strong>What would stay the same.</strong></p>
    <p><strong>Main risk.</strong> {tie to a watch-out}</p>
  </article>
</section>
```

No routes, file paths, or type names. If there is only one honest approach, say so — do not invent a second.

## Watch outs

Place this immediately after **Ways we can solve it**. Style it so a thumb-scroll cannot miss it: a short intro, the stack-hop diagram with affected hops highlighted, then 2–5 cards.

Each card is an `<article>` (not a bullet dump):

```html
<section id="watch-outs">
  <h2>Watch outs</h2>
  <p>If this change is wrong, here is who feels it and what else it can disturb.</p>
  <!-- stack hop with the touched hops highlighted -->
  <article class="watch-card">
    <h3>{Watch for — one line}</h3>
    <p><strong>Logic flaw.</strong> {how the request or code can be wrong}</p>
    <p><strong>Who feels it.</strong> {user / support / another team / …}</p>
    <p><strong>Other features.</strong> {name real systems this repo touches}</p>
    <p><strong>If we get this wrong.</strong> {one-sentence business outcome}</p>
    <p class="source">{Request / code path / uncertain}</p>
  </article>
</section>
```

Card CSS: full width on a phone, clear border, extra padding, tap-friendly. Use a warning background for money/permissions/auth; a calmer info background for "confirm at the next gate." Do not use color alone.

Do not write "be careful in general." If you have no sourced watch-out, say that in a callout and name what you still need to trace.

## Code blocks

Always use `<pre>` tags. If you use a custom styled div instead, it **must** have `white-space: pre-wrap` in its CSS, or the browser will collapse all newlines into a single line.

Before saving, scan each code block in the HTML source and confirm its CSS includes `white-space: pre` or `pre-wrap`.

Keep snippets short. Annotate *why*, not every line.

## Quiz

Five questions. Medium difficulty: you need to understand the substance, not trivia or gotchas.

Until **Build**, questions are about the **problem**, the **current vs proposed** screens, **and at least one watch-out or "which approach" question**. After **Build**, one or two may involve the seam you actually changed.

Each item:

- A prompt
- Three or four options as `<button type="button">`
- Click → mark correct/incorrect and show a short explanation

Do not reveal the answer until they tap. Keyboard and screen-reader: buttons, not clickable `<div>`s.

This quiz is separate from the flow's own `┌ CHECKS` boxes (see [../../templates/artifact-template.md](../../templates/artifact-template.md)) — CHECKS are for the dev at a gate, this quiz is for a future reader of the walkthrough. Don't conflate them or try to generate one from the other.

## Images

```html
<figure>
  <img src="data:image/png;base64,..." alt="What the user sees on the affected screen" />
  <figcaption>Problem | Current | Proposed — {one sentence}.</figcaption>
</figure>
```

`alt` describes the user-visible situation. Never embed secrets, PII, or production payloads.

Save the source image under `.ai-workflow/[feature]/assets/` as well.
