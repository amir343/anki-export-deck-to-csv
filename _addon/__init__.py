import csv
from collections import defaultdict
from datetime import datetime

from aqt import mw
from aqt.qt import QAction, QFileDialog, QMessageBox, QInputDialog


def safe_filename(name: str) -> str:
    return name.replace("::", "__").replace("/", "_").replace("\\", "_").strip()


def export_single_deck_to_csv():
    col = mw.col

    # In Anki 24.06.x this returns DeckNameId objects (not tuples)
    deck_name_ids = col.decks.all_names_and_ids()
    if not deck_name_ids:
        QMessageBox.information(mw, "Export Deck", "No decks found.")
        return

    deck_names = sorted([dni.name for dni in deck_name_ids])

    deck_name, ok = QInputDialog.getItem(
        mw,
        "Select Deck",
        "Choose a deck to export:",
        deck_names,
        0,
        False
    )
    if not ok or not deck_name:
        return

    path, _ = QFileDialog.getSaveFileName(
        mw,
        "Save CSV",
        safe_filename(deck_name) + ".csv",
        "CSV Files (*.csv)"
    )
    if not path:
        return

    note_ids = col.find_notes(f'deck:"{deck_name}"')
    if not note_ids:
        QMessageBox.information(mw, "Export Deck", f"No notes found in deck:\n{deck_name}")
        return

    try:
        # Gather notes and union of field names across note types in that deck
        notes = []
        field_names = []

        for nid in note_ids:
            note = col.get_note(nid)
            notes.append(note)
            field_names.extend(note.keys())

        field_names = list(dict.fromkeys(field_names))

        header = ["deck", "note_id", "date_added"] + field_names + ["Tags"]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for note in notes:
                created_iso = datetime.fromtimestamp(note.id / 1000).isoformat()
                row = [deck_name, note.id, created_iso]

                for fname in field_names:
                    row.append(note[fname] if fname in note else "")

                row.append(" ".join(note.tags))
                writer.writerow(row)

        QMessageBox.information(
            mw,
            "Export Complete",
            f"Exported {len(notes)} notes from:\n{deck_name}"
        )

    except Exception as e:
        QMessageBox.critical(mw, "Export Failed", str(e))


action = QAction("Export Deck to CSV", mw)
action.triggered.connect(export_single_deck_to_csv)
mw.form.menuTools.addAction(action)
