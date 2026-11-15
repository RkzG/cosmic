"""Applies the Cosmic display rebrand to upstream EffectCraft files.

Every change to an upstream file that the rebrand needs lives here, so a sync with upstream stays
simple: on a merge conflict in one of these files, take upstream's version and run this script
again. Each edit is exact and idempotent. An edit whose anchor is gone (upstream changed the line)
is reported and the script exits non-zero, so nothing is silently skipped.

Run from the repository root: python -I cosmic/tools/rebrand.py [--check]
  --check   change nothing; exit 1 if any edit is still missing or an anchor is gone
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def exact(old: str, new: str, count: int = 1):
    """Replace `old` with `new`, expecting `count` occurrences (or none once applied)."""

    def apply(text: str):
        # Checked first: some replacements contain their anchor (a line added after it).
        if new in text:
            return text, "already applied"
        found = text.count(old)
        if found != count:
            return None, f"expected {count} x {old!r}, found {found}"
        return text.replace(old, new), "applied"

    return apply


def lines(pattern: str, old: str, new: str, count: int):
    """In every line matching `pattern`, replace `old` with `new`; expect `count` such lines."""
    rx = re.compile(pattern, re.MULTILINE)

    def apply(text: str):
        hits = rx.findall(text)
        if not hits and count:
            done = re.compile(pattern.replace(re.escape(old), re.escape(new)), re.MULTILINE).findall(text)
            if len(done) == count:
                return text, "already applied"
        if len(hits) != count:
            return None, f"expected {count} lines matching {pattern!r}, found {len(hits)}"
        return rx.sub(lambda m: m.group(0).replace(old, new), text), "applied"

    return apply


def remove(pattern: str, count: int):
    """Delete every match of the multi-line `pattern`; expect `count` matches (or none once applied).

    Used for catalog rows that the rebrand leaves unused: the i18n tests reject stale rows. If
    upstream rewords such a row, the stale-row test fails and names it.
    """
    rx = re.compile(pattern, re.MULTILINE)

    def apply(text: str):
        hits = rx.findall(text)
        if not hits:
            return text, "already applied"
        if len(hits) != count:
            return None, f"expected {count} matches of {pattern!r}, found {len(hits)}"
        return rx.sub("", text), "applied"

    return apply


EDITS = {
    # Settings, shortcuts, crash recovery and logs: never shared with an installed EffectCraft.
    "crates/host/src/app_dirs.rs": [
        exact("//!    everything in `<exe dir>/EffectCraftData`,", "//!    everything in `<exe dir>/CosmicData`,"),
        exact(
            "//! 3. The platform convention: macOS `~/Library/Application Support/EffectCraft`, Windows\n"
            "//!    `%APPDATA%\\EffectCraft`, Linux `$XDG_CONFIG_HOME/effectcraft` or `~/.config/effectcraft`.",
            "//! 3. The platform convention: macOS `~/Library/Application Support/Cosmic`, Windows\n"
            "//!    `%APPDATA%\\Cosmic`, Linux `$XDG_CONFIG_HOME/cosmic` or `~/.config/cosmic`.\n"
            "//!\n"
            "//! Cosmic fork: the folder names differ from upstream EffectCraft so the two apps never share\n"
            "//! settings, shortcuts or crash recovery (see cosmic/docs/UPSTREAM-PATCHES.md).",
        ),
        exact('pub const PORTABLE_DATA_DIR: &str = "EffectCraftData";', 'pub const PORTABLE_DATA_DIR: &str = "CosmicData";'),
        exact("    /// `<exe dir>/EffectCraftData`.", "    /// `<exe dir>/CosmicData`."),
        exact('h.join("Library/Application Support/EffectCraft")', 'h.join("Library/Application Support/Cosmic")'),
        exact('PathBuf::from(a).join("EffectCraft"))', 'PathBuf::from(a).join("Cosmic"))'),
        exact('.map(|c| c.join("effectcraft"))', '.map(|c| c.join("cosmic"))'),
        exact('root.join("home/Library/Application Support/EffectCraft")', 'root.join("home/Library/Application Support/Cosmic")'),
        exact('root.join("appdata").join("EffectCraft"));', 'root.join("appdata").join("Cosmic"));'),
        exact('root.join("home/.config/effectcraft")', 'root.join("home/.config/cosmic")'),
        exact('assert_eq!(dir, exe.join("EffectCraftData"));', 'assert_eq!(dir, exe.join("CosmicData"));'),
    ],
    # Window title, message boxes and the runtime window/Dock icon.
    "apps/effectcraft/src/main.rs": [
        exact('.with_title("EffectCraft")', '.with_title("Cosmic")'),
        exact('        "EffectCraft",\n        options,', '        "Cosmic",\n        options,'),
        exact('"EffectCraft diagnostic report"', '"Cosmic diagnostic report"'),
        exact('"EffectCraft: graphics device lost"', '"Cosmic: graphics device lost"'),
        exact('file_dialogs::message("EffectCraft", message);', 'file_dialogs::message("Cosmic", message);'),
        exact(
            'include_bytes!("../../../assets/app-icon/hicolor/256x256/apps/ai.storyteller.effectcraft.png")',
            'include_bytes!("../../../cosmic/assets/app-icon/cosmic-256.png")',
        ),
        exact(
            'include_bytes!("../../../assets/app-icon/effectcraft-macos-512.png")',
            'include_bytes!("../../../cosmic/assets/app-icon/cosmic-macos-512.png")',
        ),
    ],
    "apps/effectcraft/src/crash_report.rs": [
        # One line after the rename: rustfmt joins the shorter statement.
        exact(
            "    let incident =\n"
            '        if confirmed_exit { "EffectCraft stopped unexpectedly." } else { "EffectCraft lost its diagnostic control channel; process exit is not confirmed." };',
            '    let incident = if confirmed_exit { "Cosmic stopped unexpectedly." } else { "Cosmic lost its diagnostic control channel; process exit is not confirmed." };',
        ),
        exact("If EffectCraft has closed, reopen it", "If Cosmic has closed, reopen it"),
    ],
    # The Windows executable's icon and version information.
    "apps/effectcraft/build.rs": [
        exact("../../assets/app-icon/effectcraft.ico", "../../cosmic/assets/app-icon/cosmic.ico", count=2),
        exact('.set("ProductName", "EffectCraft")', '.set("ProductName", "Cosmic")'),
        exact(
            '.set("FileDescription", "EffectCraft motion graphics and visual effects")',
            '.set("FileDescription", "Cosmic video editor (based on EffectCraft)")',
        ),
        exact(
            '"Copyright (c) 2026 The EffectCraft contributors. MIT OR Apache-2.0."',
            '"Copyright (c) 2026 The EffectCraft contributors and the Cosmic contributors. MIT OR Apache-2.0."',
        ),
    ],
    # Help > About (Windows/Linux) and the macOS app menu entry.
    "crates/engine/src/cmd/frontend.rs": [
        exact('fe!("app.about", "About EffectCraft...",', 'fe!("app.about", "About Cosmic...",'),
    ],
    "crates/engine/src/menus.rs": [
        exact("  About EffectCraft... | app.about", "  About Cosmic... | app.about"),
        exact("  [!mac] About EffectCraft... | app.about", "  [!mac] About Cosmic... | app.about"),
    ],
    # The menu translations of that entry, and the About dialog title / header tooltip.
    "crates/ui-egui/src/i18n.rs": [
        lines(r'^    \("app\.about", "About EffectCraft\.\.\.", .*$', "EffectCraft", "Cosmic", 13),
    ],
    "crates/ui-egui/src/i18n/ui.rs": [
        lines(r'^    \("About EffectCraft", .*$', "EffectCraft", "Cosmic", 11),
        # The About dialog's old description is replaced by cosmic_brand::ABOUT_BLURB.
        remove(r'^    \(\n        "A clean-room, open-source compositor for motion graphics[^\n]*\n[^\n]*\n    \),\n', 11),
    ],
    "crates/ui-egui/src/lib.rs": [
        exact("pub(crate) mod a11y;\n", "pub(crate) mod a11y;\npub(crate) mod cosmic_brand;\n"),
    ],
    # The header's About button and the logo in the Tools bar and About dialog.
    "crates/ui-egui/src/header.rs": [
        exact('"About EffectCraft"', '"About Cosmic"', count=2),
        exact(
            "/// The ArtCraft mark as supplied in `docs/brand` (the README's and getartcraft.com's logo; used\n"
            "/// unmodified, see `docs/brand/LICENSE-brand.txt`).\n"
            'static ARTCRAFT_MARK: &[u8] = include_bytes!("../../../docs/brand/artcraft-mark.png");',
            "/// Cosmic fork: the Cosmic logo replaces the ArtCraft mark, which the ArtCraft brand terms\n"
            "/// (`docs/brand/LICENSE-brand.txt`) require modified versions to remove.\n"
            "static ARTCRAFT_MARK: &[u8] = crate::cosmic_brand::LOGO_PNG;",
        ),
    ],
    # The window title once a project is open ("Cosmic - <project>"), and its integration test.
    "crates/ui-egui/src/panels/unsaved.rs": [
        exact(
            'format!("EffectCraft - {doc}{}", if app.session.is_dirty() { " *" } else { "" })',
            'format!("{} - {doc}{}", crate::cosmic_brand::NAME, if app.session.is_dirty() { " *" } else { "" })',
        ),
    ],
    "crates/ui-egui/tests/it/ui_window_title.rs": [
        exact('starts_with("EffectCraft - ")', 'starts_with("Cosmic - ")', count=2),
    ],
    "crates/ui-egui/src/panels/dialogs.rs": [
        exact('modal(ctx, "About EffectCraft",', 'modal(ctx, "About Cosmic",'),
        exact(
            'Align2::LEFT_CENTER, "EffectCraft", Tokens::semibold(24.0), Color32::WHITE);',
            "Align2::LEFT_CENTER, crate::cosmic_brand::NAME, Tokens::semibold(24.0), Color32::WHITE);",
        ),
        exact(
            'format!("Version {}  •  Motion graphics & VFX in pure Rust", env!("CARGO_PKG_VERSION")),',
            'format!("Version {}  •  {}", env!("CARGO_PKG_VERSION"), crate::cosmic_brand::TAGLINE),',
        ),
        exact(
            'ui.label(tr("A clean-room, open-source compositor for motion graphics and visual effects: native on macOS, Windows and Linux, and in the browser. Part of the ArtCraft family of creative apps."));',
            "ui.label(crate::cosmic_brand::ABOUT_BLURB);",
        ),
    ],
}


def main() -> int:
    check = "--check" in sys.argv[1:]
    failed = pending = 0
    for rel, edits in EDITS.items():
        path = ROOT / rel
        raw = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        text = raw.replace("\r\n", "\n")
        for i, edit in enumerate(edits, 1):
            new_text, status = edit(text)
            if new_text is None:
                failed += 1
                print(f"FAIL  {rel} #{i}: {status}")
                continue
            if status == "applied":
                pending += 1
            print(f"{'todo' if check and status == 'applied' else 'ok  '}  {rel} #{i}: {status}")
            if not check:
                text = new_text
        if not check:
            out = text.replace("\n", "\r\n") if crlf else text
            if out != raw:
                path.write_bytes(out.encode("utf-8"))
    if failed:
        print(f"\n{failed} edit(s) could not be applied: upstream changed those lines. Update EDITS.")
        return 1
    if check and pending:
        print(f"\n{pending} edit(s) not applied yet. Run without --check.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
