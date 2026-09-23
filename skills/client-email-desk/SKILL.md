---
name: client-email-desk
description: Drafts the first version of the technical client replies that eat an afternoon, in the firm's tone, with every uncertain point flagged for a human rather than answered confidently. Use when replying to a client question, drafting a technical email, answering a tax or accounting query by email, or clearing an inbox of client questions.
---

# Client email desk

First drafts of the replies that eat an afternoon. Not sent by the AI. Drafted, so the partner
edits rather than composes.

## The one rule

**Never state a technical position the model worked out on its own.** Tax and accounting
answers depend on jurisdiction, year, entity type and facts the email does not contain. A
confident wrong answer in writing to a client is a professional problem, not a typo.

Every technical point in a draft is one of three things, and the draft says which:

| Marking | Meaning |
|---|---|
| Plain text | A fact from the client's own data or a previous email in the thread |
| `[CONFIRM]` | A technical position that a qualified human must verify before sending |
| `[NEED]` | Information that is missing and has to be asked for |

A draft with no `[CONFIRM]` markers on a technical question is a draft that has overstepped.

## Step 1: read the whole thread

Ask for the full thread, not the last message. Clients repeat questions, and the answer given
three emails ago is binding whether or not anyone remembers it.

Check specifically:
- Has this been answered before in the thread?
- Did the firm already commit to a position or a date?
- Is the question actually two questions?

## Step 2: classify the email

| Type | Approach |
|---|---|
| Factual about their own data | Answer from the ledger. Cite the figure and its source. |
| Process, "what do I do next" | Answer plainly. Usually low risk. |
| Technical, tax or accounting treatment | Draft the shape of the answer, mark every position `[CONFIRM]`. |
| Scope, "is this included" | Do not answer. Flag for the engagement partner. |
| Complaint or fee dispute | Do not draft. Say so and stop. |

The last two matter. A cheerful AI-drafted reply to a complaint is how a small problem becomes
a formal one.

## Step 3: match the firm's tone

Ask for two or three previously sent replies and match them: greeting, sign-off, sentence
length, whether the firm uses first names, how it delivers bad news. Do not impose a house
style, the firm has one.

## Step 4: draft

```
Subject: Re: [their subject]

Hi [name],

[Direct answer to the question asked, first line. Not a preamble.]

[The detail, short paragraphs, one point each.]

[CONFIRM] The treatment above assumes [X]. Verify against [year, jurisdiction]
before sending.

[NEED] To be certain, I need [specific thing].

[Firm's usual sign-off]
```

Rules:
- Answer the question asked, in the first line. Clients scroll.
- One email, one topic. If they asked two questions, draft two replies and say so.
- Never invent a deadline, a rate or a threshold. Mark it `[NEED]` and ask.
- No apology for the delay unless the user says there was one.
- Do not attach or promise anything the user has not confirmed exists.

## Step 5: report before handing over

```
DRAFTED, 3 of 5 emails

  Ready to review
    Baker Joinery, question about the August invoice
    Hale Interiors, process question about the portal

  Drafted with confirmations needed
    Cloudhost, VAT treatment on the subscription, 2 [CONFIRM] markers

  Not drafted
    Paperworks, fee dispute. Needs the engagement partner, not a draft.
    Marsh Ltd, asks whether audit is in scope. Scope question, partner decision.
```

## What this skill does not do

- **It does not send email.** The Xero connection has no email tool, and this is deliberate
  anyway. Every reply is a draft a human sends.
- **It does not give tax advice.** It drafts the shape and marks what needs verifying.
- **It does not handle complaints or fee disputes.** It routes them to a person.
- **It does not decide scope.** That is an engagement partner decision.
