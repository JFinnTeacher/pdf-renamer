# PDF Renamer Help

PDF Renamer renames a batch of PDF files and writes a **Title** (and optionally an **Author**) into each file's metadata, using naming patterns you define once for the whole batch.

## Quick start

1. **Add PDFs:** click **Add Folder...** or **Add Files...** in the Batch panel, or drag PDFs or folders onto the window.
2. **Enter a title pattern** such as `Chapter {n} - {title}` and click **Apply to All**. The preview under the field shows the result for the first file.
3. **Check the Status column.** Anything shown in red needs fixing before you run (see *Status column* below).
4. Click **Run** (or press Ctrl+Enter).

Each file is renamed to its new title plus `.pdf`, and the new title is written into the PDF's Title metadata.

### Setting the Title and Author without renaming

To change only the metadata and keep every filename as it is, untick **Rename files to match their Title** in the Batch panel before you click Run. The Title and Author columns are still written into each PDF, but no file is renamed. Files can then share the same title without being flagged as duplicates. The setting is remembered.

A file whose name already matches its title also has its Title and Author updated, even when renaming is switched on.

## Naming patterns

A pattern is ordinary text with placeholders in curly braces:

| Placeholder | Replaced with |
|---|---|
| `{n}` | The first number in the original filename, e.g. `7` from `scan7.pdf` |
| `{title}` | The file's current value in the Title column |
| `{author}` | The file's current value in the Author column |
| `{name}` | The whole original filename, without `.pdf` |
| `{part1}`, `{part2}`, ... | A piece of the original filename (see *Titles from the filename* below) |

Click a placeholder button under the patterns to insert it into whichever pattern field you last clicked in.

### Titles from the filename

To build the title from pieces of the filename, choose where the name is divided using **Divide filename into parts at**. The default divides at a dash or an underscore. You can also pick a dash, an underscore, a space, a full stop, any of these, or **Custom**, where you type the characters to divide at (include a space to divide at spaces too).

For example, `Smith_2024_Report.pdf` divided at `_` gives `{part1}` = `Smith`, `{part2}` = `2024` and `{part3}` = `Report`, so the pattern `{part3} ({part2}) - {part1}` gives `Report (2024) - Smith`.

- The line under the options shows how the first file in the list is divided, so you can check which part is which.
- Spaces around each part are removed, and empty parts are skipped, so `Smith - 2024 - Report` divided at `-` gives `Smith`, `2024` and `Report`.
- A part number past the end gives nothing, e.g. `{part4}` is blank for a name with three parts.
- To keep the whole filename as the title, use `{name}`.
- Changing the divider updates every title that uses a pattern. Presets remember the divider too.

**Leading zeros:** set **Pad {n} with leading zeros to** to make numbers a fixed width, e.g. 3 digits turns `7` into `007`, which keeps files in order when sorted by name. To pad differently in one pattern, write the format out in the pattern, e.g. `{n:02d}`; that takes priority over the box.

**Author pattern:** works the same way and fills the Author column. If a file's Author is left blank, its existing Author metadata is kept as it was. Other metadata (Subject, Keywords, dates) is always kept.

**Tip:** `{title}` uses the Title column as it is *now*. Applying `Part {n} - {title}` twice gives `Part 1 - Part 1 - ...`. If that happens, click **Reset** or re-add the files.

Characters that Windows doesn't allow in filenames (`< > : " / \ | ? *`) are removed from the filename automatically. The Title metadata keeps them.

## Presets

Presets save your title pattern, author pattern, leading-zeros setting and filename divider under a name.

- **Save as Preset...** saves the current fields. Using an existing name replaces that preset (you'll be asked first).
- **Choose a preset** from the drop-down to fill the fields, then click **Apply to All**.
- **Delete** removes the selected preset.

## The file list

- **Edit a cell** by double-clicking it (or selecting it and pressing F2). You can edit Title Pattern, Title, Author Pattern and Author for individual files. Editing a file's Title Pattern recalculates its Title.
- **Move Up / Move Down** (Alt+Up / Alt+Down) change the order files are processed in.
- **Remove** (or the Delete key) takes the selected file off the list. It doesn't delete the file.
- **Clear List** removes every file from the list. **Reset** also clears the patterns and the log.
- **Resize columns** by dragging the lines between the column headings. The widths are remembered. To undo your changes, use **Settings > Reset Column Widths**.
- **Hover over a filename** to see its full path.

## Status column

Before you run, the Status column predicts what will happen to each file:

| Status | Meaning |
|---|---|
| ready | Will be renamed as shown |
| unchanged | The file keeps its name; only its Title and Author metadata are updated |
| suffix | The name is taken, so a number will be added, e.g. `Title (2).pdf` |
| overwrite | An existing file with this name will be replaced |
| **no title** (red) | The title is empty, or has only characters that can't be used in a filename |
| **duplicate** (red) | Another file in the list would get the same name |
| **exists** (red) | A different file already has this name |

Hover over a status to see details. The Batch panel shows how many problems there are of each kind. Hover over that summary for what each kind means and how to fix it, or click **Show the first one** to jump to it in the list. If you click Run with problems remaining, you'll be asked whether to continue; files with problems are skipped or fail.

After a run, the Status column shows the result: **renamed**, **copied**, **updated** (metadata changed, name kept), **skipped** or **failed**. The log has the details.

**Every file says duplicate?** Some downloaded PDFs all have the same Title metadata, such as a website name, so every file would get the same name. Apply the title pattern `{name}` to start from the filename instead, or set **Settings > Starting title** to the filename before adding the files.

## Settings

Open **⚙ Settings** (Ctrl+,) to change:

- **If the new name is taken:** skip the file, add a number, or overwrite the existing file.
- **Save renamed files:** rename in place (replaces the originals), or save renamed copies to an output folder (keeps the originals).
- **Include subfolders** when adding a folder.
- **Sort new files by:** name with numbers in order (`scan2` before `scan10`), alphabetical, or date modified.
- **Starting title:** what fills the Title column when you add a file. Choose the PDF's existing Title metadata, the filename, or blank.
- **Theme:** follow Windows, light, or dark. The **Dark Mode / Light Mode** button in the top right switches quickly.
- **Reset Column Widths** puts the file list's columns back to their defaults.

## The log

The log records every action with a timestamp.

- **Resize** it by dragging the line between the file list and the log.
- **Hide Log / Show Log** collapses it to give the file list more room.
- **Export Log...** (Ctrl+Shift+E) saves it as a text file. **Clear** empties it.

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| Ctrl+O | Add files |
| Ctrl+Shift+O | Add folder |
| Ctrl+Enter | Run |
| Alt+Up / Alt+Down | Move the selected file up / down |
| Delete | Remove the selected file from the list |
| F2 or double-click | Edit the selected cell |
| Ctrl+, | Settings |
| Ctrl+Shift+E | Export the log |
| F1 | Open this help |

## Good to know

- **Renaming in place replaces the original file.** For important files, use *Save renamed copies to an output folder* in Settings, or keep a backup.
- Each new PDF is fully written before the original is removed, so a failure part-way through won't leave a half-written file.
- Click **About** for the version number, licence (CC BY-NC-SA 4.0) and a link to the source code.
- Your settings, presets, patterns and window layout are saved to `%APPDATA%\PDF Renamer\settings.ini`. Delete that file to start from the defaults.
