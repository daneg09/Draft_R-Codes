# How to use this (plain English)

This is the draft R-Codes turned into data an AI model can read. You don't need to code to use it. You need an AI tool that can open a folder of files, and the details of your proposal.

It's a quick, unofficial experiment. The draft isn't in force, the WAPC's published PDFs govern, and nothing it tells you is planning advice.

## What you can ask it

Three kinds of question work well.

**Check a design.** "Assess this single house on a 600 m² R20 lot against the draft R-Codes." It works through each relevant clause and tells you what complies, what doesn't and what it still needs to know.

**Look something up.** "What does the draft say about garage setbacks for a single house at R30?" You get the requirement with the clause number and the page in the draft.

**Find out what you need.** "What information do I need before you can assess a grouped dwelling?" Handy before you brief a designer or pull a plan set together.

## Step 1. Get a copy

1. Go to https://github.com/daneg09/Draft_R-Codes
2. Click the green **Code** button, then **Download ZIP**.
3. Unzip it somewhere you'll find it again.

You don't need a GitHub account for this.

## Step 2. Open it in an AI tool

Use an AI tool that can work with a folder on your computer. Claude Code and the Claude desktop app both can. Give it access to the folder you just unzipped.

A plain chat window where you upload one or two documents won't work as well. The tool needs to move around the folder and open the parts it needs.

## Step 3. Ask your question

Copy this and fill in the brackets:

> Use the draft R-Codes edition in this folder. Follow the instructions in edition/SKILL.md.
>
> Assess this proposal against the draft:
> - Dwelling type: [single house / grouped dwelling / apartments]
> - R-Code: [e.g. R20]
> - Location: [Perth and Peel, or regional]
> - Lot size: [e.g. 15 m x 30 m, 450 m²]
> - Design: [describe it, or attach the plans]

The more you give it up front, the less it has to ask. Useful details include:

- setbacks to the street and each side and rear boundary
- building height and number of storeys
- garage position and setback
- open space and outdoor living area
- trees and landscaping
- windows, decks or balconies facing a neighbour

## Step 4. Answer its questions

It won't guess. If it needs a measurement you haven't given, it will say "cannot tell" and ask for it. Give it the number and it carries on.

If it reads measurements off your plans, check them. Plan reading is the weakest part of the process. It should tell you which numbers it read itself.

## Step 5. Read the result

Every clause gets one of these outcomes:

| Outcome | What it means |
|---|---|
| Meets | Your design satisfies that clause. |
| Does not meet | It doesn't. The report names the merit criteria it would be assessed against instead. |
| Cannot tell | A measurement is missing. It names what's needed. |
| Not applicable | The clause doesn't apply to your R-Code or dwelling type. |
| Not evaluated | The clause needs a planner's judgement. It quotes the text and leaves the call to you. |

At the top you'll see the overall pathway:

- **Deemed exempt** means every testable clause is met.
- **Merit assessment** means at least one isn't, so those elements would be assessed on merit.
- **Undetermined** means it's still waiting on missing information.

Each finding cites the clause and the page in the draft, so you can check it against the PDF yourself.

## What it can't do

- It only covers the draft R-Codes. It doesn't include the current R-Codes, so it can't compare old against new.
- It doesn't hold local planning policies, schemes, local development plans or structure plans. If one applies to your site, give it the clause and it will check whether the draft lets that clause vary the requirement.
- It doesn't have maps. You need to tell it the R-Code, whether you're in Perth and Peel or regional, and whether you're near a train station or high-frequency bus route (this affects parking).
- Every value has been checked once against the draft, by AI. No person has reviewed it yet. Some clauses are flagged where the draft itself is unclear, and the report will point these out.

## Found a mistake?

Please tell me. Open an issue at https://github.com/daneg09/Draft_R-Codes/issues (you'll need a free GitHub account). Say which clause is wrong, what the draft says, and the page number.

If you spot something in the draft that doesn't add up, it's worth raising in your submission too. Consultation closes 26 February 2027.

## For developers

If you write code, the engine runs in Python 3.11 or later. The main README has the commands, and `docs/DEVELOPING.md` has the detail.
