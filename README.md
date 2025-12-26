# Anki Export Deck to CSV

A small Anki add-on that adds a Tools menu item to export a selected deck’s notes to a CSV file.

## What it does

In Anki, you get a new menu item:

**Tools → Export Deck to CSV**

When you run it, the add-on:
1. Prompts you to choose a deck
2. Prompts you to choose where to save a `.csv`
3. Exports every note in that deck to the CSV (UTF-8)

## CSV output format

The first row is a header:

- `deck`
- `note_id`
- `date_added` (derived from the note id timestamp)
- one column per field name (union of all fields across note types used in the deck)
- `tags` (space-separated)

Notes:
- Field values are exported as stored in Anki and may include HTML.
- If a note does not have a particular field (because the deck contains multiple note types), that cell is left blank.

## Installation

### Option A: Install from a local folder
1. In Anki: **Tools → Add-ons → View Files**
2. Copy the add-on folder into `addons21/`
3. Restart Anki

### Option B: Install from a `.ankiaddon` file
If you build a `.ankiaddon` release, users can install it by double-clicking the file (or via the Anki add-ons UI), then restarting Anki.

## Compatibility

Developed against Anki 24.06.x.

## Development

This repository contains the add-on source under `_addon/`.

Typical workflow:
- edit `_addon/__init__.py`
- restart Anki to test

## License

MIT
