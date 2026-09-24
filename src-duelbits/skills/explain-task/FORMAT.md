# Explain Task — HTML format

One long page. No tabs for top-level structure. Self-contained: CSS and JavaScript inline, images as data URIs.

Write with the clarity and flow of Martin Kleppmann, making it engaging and written in classic style. Transitions between sections should be smooth.

## Mobile-first

The phone is the primary surface. Desktop can get wider type; nothing may require hover or a wide canvas.

- `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Body text ≥ 16px; line-height ~1.5; max-width ~40rem; padding that survives a thumb
- Quiz options and in-page links: tap target ≥ 44px
- Images: `max-width: 100%; height: auto`
- Stage rail: wrap, don’t horizontally scroll
- Sticky top bar: ticket key + current stage only
- Color contrast sufficient for outdoor reading

## Page skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{Ticket}: {one-line title}</title>
  <style>/* inline CSS */</style>
</head>
<body>
  <header class="top">
    <p class="kicker">{FD-XXXX} · {stage} · {date}</p>
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

## Sections (in order)

1. **Where we are** — six-stage rail + one sentence on the next step (first run: confirm an approach, not `tdd`).
2. **How Clair works here** — skippable `<details>` for readers who already know the area.
3. **The problem** — who feels it, what is wrong, why this ticket exists. Toy data. No class names.
4. **What it looks like** — **Problem** screenshots, then **Current** screenshots (today’s product). HTML phone-frame if a capture is missing. Caption every figure Problem / Current / Proposed.
5. **Ways we can solve it** — each alternative in simple terms so the reader can check the logic. If more than one exists, list them, mark Recommended, and wait. Proposed screenshots live here, not in Current.
6. **Watch outs** — required. Logic flaws, business impact, other features. Helps pick an alternative. See below.
7. **Code** — omit until an approach is confirmed **and** the stage is **Build**. Then a high-level walkthrough grouped so a new joiner can follow, not a file-by-file diff. Use `<pre>` (see Code blocks).
8. **Quiz** — five interactive multiple-choice questions.
9. **Next step** — first run: “Which approach should we take?” Later: `grill this`, `tdd`, `code review`, …

Use callouts (a styled `<aside>`) for definitions, edge cases, and “if this is missing we cannot know X”.

## Diagram families

Pick a small number and reuse them. No ASCII diagrams. Simple HTML/CSS only.

1. **Person journey** — employee, partner, Clair as labeled cards with arrows and example values (`$80`, `employeeKey`, `payday Friday`).
2. **Stack hop** — `partner-portal → partner-flex ← proxy-flex ← SDKs → core-flex → clair-flex`. Highlight the hop this ticket changes; keep the rest muted.
3. **Phone frame** — a simplified UI the employee or partner would see. Use it when Figma/browser capture is unavailable, and as a caption overlay when it is.

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
    <p><strong>What would change.</strong> {employee or partner}</p>
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
    <p><strong>Logic flaw.</strong> {how the ticket or code can be wrong}</p>
    <p><strong>Who feels it.</strong> {employee / partner / Care / …}</p>
    <p><strong>Other features.</strong> {lending, SDK, Kraken, …}</p>
    <p><strong>If we get this wrong.</strong> {one-sentence business outcome}</p>
    <p class="source">{Ticket / code path / uncertain}</p>
  </article>
</section>
```

Card CSS: full width on a phone, clear border, extra padding, tap-friendly. Use a warning background for money/eligibility/auth; a calmer info background for “confirm in grill”. Do not use color alone.

Do not write “be careful in general.” If you have no sourced watch-out, say that in a callout and name what you still need to trace.

## Code blocks

Always use `<pre>` tags. If you use a custom styled div instead, it **must** have `white-space: pre-wrap` in its CSS, or the browser will collapse all newlines into a single line.

Before saving, scan each code block in the HTML source and confirm its CSS includes `white-space: pre` or `pre-wrap`.

Keep snippets short. Annotate *why*, not every line.

## Quiz

Five questions. Medium difficulty: you need to understand the substance, not trivia or gotchas.

Until **Build**, questions are about the **problem**, the **current vs proposed** screens, **and at least one watch-out or “which approach” question**. After **Build**, one or two may involve the seam you actually changed.

Each item:

- A prompt
- Three or four options as `<button type="button">`
- Click → mark correct/incorrect and show a short explanation

Do not reveal the answer until they tap. Keyboard and screen-reader: buttons, not clickable `<div>`s.

## Images

```html
<figure>
  <img src="data:image/png;base64,..." alt="What the employee sees on the home chevron" />
  <figcaption>Problem | Current | Proposed — {one sentence}.</figcaption>
</figure>
```

`alt` describes the user-visible situation. Never embed secrets, PII, or production payloads.

Save the source PNG under `personal/tasks/<kebab-slug>/assets/` as well (see `.cursor/rules/personal-task-artifacts.mdc`). Do not keep a separate INDEX.md — the folder name is the index.
