# 🔐 File Integrity Monitor

A simple Python utility that detects whether any files in a directory have been **modified, added, or deleted** by comparing their SHA-256 hashes against a saved baseline.

Built for the **Cyber Sec Club**.

---

## How It Works

1. **Baseline** – The tool traverses the target folder (and all subfolders), calculates the SHA-256 hash of each file, and writes `{relative_path: hash}` pairs to `baseline.json`.
2. **Verify** – On re-scan, it recalculates every hash and compares it against the baseline:
   - Path in baseline, missing now → **DELETED**
   - Path in both, hash differs → **MODIFIED**
   - Path exists now, not in baseline → **ADDED**

SHA-256 changes completely if even a single byte of content changes, so the tool detects any content variation.

---

## Features

- ✅ SHA-256 hashing of every file
- ✅ Baseline stored as human-readable JSON
- ✅ Reports **Modified**, **Added**, and **Deleted** files
- ✅ Recursive scanning of nested subfolders (`os.walk`)
- ✅ Paths stored relative to the monitored folder, so it works on any operating system
- ✅ Skips files it can't read (permission errors, file removed mid-scan)
- ✅ Fails gracefully on a missing or corrupted `baseline.json`

---

## Requirements

- Python 3.6+
- No third-party libraries (only `hashlib`, `json`, and `os` from the standard library)

---

## Usage

1. Clone the repo:

   ```bash
   git clone https://github.com/rithwik-nambiar/File-Integrity-Monitor.git
   cd File-Integrity-Monitor
   ```

2. Put the files you want to monitor inside a folder named `subfolder` in the project root.

   > **💡 Want to monitor a different folder?**
   > Open `integrity_monitor.py` and change the `folder` variable at the top of the file:
   >
   > ```python
   > folder = "subfolder"   # change this to any folder path, e.g. "my_documents"
   > ```
   >
   > Run the

3. Run:

   ```bash
   python integrity_monitor.py
   ```

4. Choose an option:

   ```
   ===== FILE INTEGRITY MONITOR =====
   1. Create Baseline
   2. Check for Changes
   ```

---

## Demo

**Step 1: Create the baseline** (option `1`)

```
Baseline created successfully!
Files scanned: 3
```

**Step 2: Tamper with the folder**

- Edit one file
- Add one new file
- Delete one file

**Step 3: Re-scan** (option `2`)

```
===== INTEGRITY REPORT =====
MODIFIED: file1.txt
DELETED : file2.txt
ADDED   : new_file.txt
```

---

## Example `baseline.json`

```json
{
    "file1.txt": "bae26ea7911dcc000c0f59e3276f93cc75171125c2d4bf04add0d96d700e674f",
    "nested\\file3.txt": "e06f0eadeec4734b5666a155ef5e34f8b9f401d2948c36a51aa85e6dfe8ff66d"
}
```

---

## Project Structure

```
.
├── integrity_monitor.py   # the tool
├── baseline.json          # generated on first run
└── subfolder/             # the folder being monitored
```

---

## Limitations

This is a learning project, not a production security product. Known limitations:

- **The baseline is not protected.** Anyone with write access to `baseline.json` can modify it and hide their changes. In real deployments the baseline would be signed (e.g. HMAC) or stored in a read-only, off-disk location.
- **No continuous monitoring.** Changes are only detected when you run a manual check.
- **Content only.** Permissions, ownership, and timestamps are not tracked.
- **Monitored folder is hardcoded** to `subfolder`.
- **Entire files are read into memory** before hashing, which is a problem for large files.

---

## Roadmap

- [ ] HMAC-sign the baseline to detect tampering with `baseline.json` itself
- [ ] Continuous monitoring mode (polling or `watchdog`)
- [ ] CLI arguments (`--folder`, `--baseline`) via `argparse`
- [ ] Read files in chunks for large files
- [ ] Track file permissions and metadata
- [ ] Log reports to a file

---

## License

MIT

---

Written and maintained by **Rithwik Nambiar** - "github.com/rithwik-nambiar](https://github.com/rithwik-nambiar"
