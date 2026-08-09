---
name: ste100
description: Write in ASD-STE100 Simplified Technical English. Use when Winston asks for STE, Simplified Technical English, "STE mode", or asks to rewrite, convert, or simplify text into STE. Also triggers on /ste100. With no arguments it activates STE mode for the rest of the session; with text or a file path it rewrites that content into STE.
---

# ASD-STE100 Simplified Technical English

STE is a controlled language: short sentences, active voice, one meaning per
word. This skill has two modes.

1. **Mode toggle** (no arguments): apply the rules below to every
   conversational reply for the rest of the session. Confirm activation in
   one STE-compliant sentence.
2. **Rewrite** (arguments given): treat the arguments as text, or as a path
   to a file that holds the text. Rewrite the content into STE. Return only
   the rewrite. Add notes about the changes only if Winston asks for them.

## Writing rules — apply strictly

- Keep sentences to 20 words or fewer in instructions, 25 or fewer in
  descriptions.
- Keep paragraphs to 6 sentences or fewer. Give each paragraph one topic.
- Use the active voice. Write "The valve controls the flow", not "The flow
  is controlled by the valve".
- Use the imperative for instructions. Write "Run the test", not "The test
  should be run".
- Give one instruction per sentence.
- Put warnings and cautions before the step they apply to, on their own
  line, marked WARNING or CAUTION.
- Use the articles "the", "a", and "an". Do not drop them to save words.
- Use the simple present tense where possible. Avoid "-ing" verb forms when
  a simple form works.

## Vocabulary rules — apply best-effort

- Use each word with one meaning and one part of speech. Example: STE
  approves "test" as a noun only — write "do a test", not "test the pump".
- Prefer STE-approved general words: "start" not "commence", "use" not
  "utilize", "stop" not "terminate", "make sure" not "ensure", "help" not
  "facilitate".
- The licensed STE dictionary (~900 approved words) is not bundled here.
  Apply the writing rules strictly and the vocabulary on a best-effort
  basis. Do not invent restrictions that make the text less clear.

## Technical Names — exempt from the dictionary

Code identifiers, file paths, commands, API and table names, product names,
payer names, and other domain terms are STE Technical Names. Pass them
through unchanged. Do not "simplify" a proper noun or an identifier.

## Scope

- Applies to prose: replies, explanations, and documents when asked.
- Does not apply to code, commit messages, or messages drafted in another
  person's voice (for example slack-respond output), unless Winston
  explicitly extends it.
