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


def row(key: str) -> str:
    """A one-line panel catalog row `("<key>", "<translation>"),` in i18n/ui.rs."""
    return r'^    \(' + re.escape(f'"{key}"') + r', [^\n]*\),\n'


def menu_row(command: str, label: str) -> str:
    """A one-line menu catalog row `("<command>", "<label>", "<translation>"),` in i18n.rs."""
    return r'^    \(' + re.escape(f'"{command}", "{label}"') + r', [^\n]*\),\n'


# Second pass (Phase 0): the Home screen, header, About links, Help and File menus, dialogs,
# Settings, Learn and the Auto-Save, Log and Presets folders. Cosmic links to its own repository
# and credits EffectCraft; the ArtCraft Discord, website, app page and sibling apps are gone.
MORE = {
    "crates/engine/src/home/links.rs": [
        exact(
            'pub const GITHUB: &str = "https://github.com/storytold/effectcraft";\n'
            'pub const ISSUES: &str = "https://github.com/storytold/effectcraft/issues";',
            "// Cosmic fork: Help, About and Home link to Cosmic's repository; UPSTREAM credits EffectCraft.\n"
            'pub const GITHUB: &str = "https://github.com/RkzG/cosmic";\n'
            'pub const ISSUES: &str = "https://github.com/RkzG/cosmic/issues";\n'
            'pub const UPSTREAM: &str = "https://github.com/storytold/effectcraft";',
        ),
    ],
    "crates/engine/src/cmd/help.rs": [
        exact('cmd!("help.docs", "EffectCraft Help...",', 'cmd!("help.docs", "Cosmic Help...",'),
        exact(
            'cmd!("help.appPage", "EffectCraft Home Page", ["Help"], None, "{}", always, |s, _| open(s, links::APP_PAGE.into())),',
            'cmd!("help.appPage", "Based on EffectCraft", ["Help"], None, "{}", always, |s, _| open(s, links::UPSTREAM.into())),',
        ),
        exact('cmd!("help.github", "EffectCraft on GitHub",', 'cmd!("help.github", "Cosmic on GitHub",'),
        # No longer in the Help menu (a test requires a declared menu path to exist in the tree);
        # the commands stay for scripts and agents.
        exact('cmd!("help.discord", "Join the ArtCraft Discord...", ["Help"],', 'cmd!("help.discord", "Join the ArtCraft Discord...", [],'),
        exact('cmd!("help.website", "ArtCraft Website", ["Help"],', 'cmd!("help.website", "ArtCraft Website", [],'),
    ],
    "crates/engine/src/tests/session.rs": [
        exact(
            'assert_eq!(s.execute("help.github", json!({})).unwrap()["url"], "https://github.com/storytold/effectcraft");',
            'assert_eq!(s.execute("help.github", json!({})).unwrap()["url"], "https://github.com/RkzG/cosmic");',
        ),
        exact(
            'url.strip_prefix("https://github.com/storytold/effectcraft/blob/main/")',
            'url.strip_prefix("https://github.com/RkzG/cosmic/blob/main/")',
        ),
    ],
    "crates/engine/src/tests/aep_import.rs": [
        exact('            "EffectCraft Project...",\n', '            "Cosmic Project...",\n'),
    ],
    "crates/engine/src/menus.rs": [
        exact("  EffectCraft Help... | help.docs", "  Cosmic Help... | help.docs"),
        exact("    EffectCraft Project... | file.importProject", "    Cosmic Project... | file.importProject"),
        remove(r"^  Join the ArtCraft Discord\.\.\. \| help\.discord\n", 1),
        remove(r"^  ArtCraft Website \| help\.website\n", 1),
        exact("  EffectCraft Home Page | help.appPage", "  Based on EffectCraft | help.appPage"),
        exact("  EffectCraft on GitHub | help.github", "  Cosmic on GitHub | help.github"),
    ],
    "crates/engine/src/cmd/import_project.rs": [
        exact('        "EffectCraft Project...",\n        ["File", "Import"],', '        "Cosmic Project...",\n        ["File", "Import"],'),
    ],
    # Menu translations: renamed entries keep their translations with the new name; entries that
    # are gone, or whose meaning changed (Based on EffectCraft), lose their rows.
    "crates/ui-egui/src/i18n.rs": [
        remove(menu_row("help.discord", "Join the ArtCraft Discord..."), 13),
        remove(menu_row("help.website", "ArtCraft Website"), 13),
        remove(menu_row("help.appPage", "EffectCraft Home Page"), 13),
        lines(r'^    \("help\.github", "EffectCraft on GitHub", .*$', "EffectCraft", "Cosmic", 13),
        lines(r'^    \("help\.docs", "EffectCraft Help\.\.\.", .*$', "EffectCraft", "Cosmic", 13),
        lines(r'^    \("file\.importProject", "EffectCraft Project\.\.\.", .*$', "EffectCraft", "Cosmic", 13),
    ],
    "crates/ui-egui/src/i18n/ui.rs": [
        lines(r'^    \("Welcome to EffectCraft", .*$', "EffectCraft", "Cosmic", 11),
        lines(r'^    \("EffectCraft project", .*$', "EffectCraft", "Cosmic", 11),
        lines(r'^    \("EffectCraft on GitHub", .*$', "EffectCraft", "Cosmic", 11),
        lines(r'^    \("Stored, but not used by EffectCraft yet", .*$', "EffectCraft", "Cosmic", 8),
        lines(r'^    \("EffectCraft didn\'t quit normally last time\.", .*$', "EffectCraft", "Cosmic", 11),
        lines(r'^    \(\n        "Hands-on tutorials that run inside EffectCraft\.[^\n]*\n[^\n]*\n    \),$', "EffectCraft", "Cosmic", 2),
        remove(row("Join the ArtCraft Discord"), 11),
        remove(row("Join the ArtCraft community on Discord"), 11),
        remove(row("Discord"), 11),
        remove(row("More ArtCraft apps"), 11),
        remove(row("EffectCraft home page"), 11),
        remove(row("EffectCraft on getartcraft.com"), 5),
        remove(row("ArtCraft website"), 5),
        remove(row("Source code on GitHub"), 5),
    ],
    # Home: welcome, the Recent list's kind, and the Community links.
    "crates/ui-egui/src/panels/home.rs": [
        exact('tr("Welcome to EffectCraft")', 'tr("Welcome to Cosmic")'),
        exact('"EffectCraft project"', '"Cosmic project"', count=3),
        exact(
            "    let links = [\n"
            '        (Icon::Chat, "Join the ArtCraft Discord", "help.discord"),\n'
            '        (Icon::Globe, "getartcraft.com", "help.website"),\n'
            '        (Icon::Globe, "EffectCraft home page", "help.appPage"),\n'
            '        (Icon::Code, "EffectCraft on GitHub", "help.github"),\n'
            "    ];\n"
            "    let sib = effectcraft_engine::links::SIBLINGS;\n",
            "    // Cosmic fork: Cosmic's repository and a credit to EffectCraft; no ArtCraft links or apps.\n"
            '    let links = [(Icon::Code, "Cosmic on GitHub", "help.github"), (Icon::Globe, "Based on EffectCraft", "help.appPage")];\n'
            "    let sib: &[(&str, &str)] = &[];\n",
        ),
        remove(r'^    p\.text\(pos2\(x0, cy \+ 8\.0\), Align2::LEFT_CENTER, tr\("More ArtCraft apps"\), Tokens::ui\(11\.0\), t\.text_faint\);\n    cy \+= 20\.0;\n', 1),
        # The Home test's list of controls: the Discord link is gone.
        remove(r'^            "home\.help\.discord",\n', 1),
    ],
    # Header: no Discord pill or website button; the GitHub button opens Cosmic's repository.
    "crates/ui-egui/src/header.rs": [
        remove(
            r"^    // The pill fits its label \(icon, gap, text\) with even padding: it was a fixed 104 px with the\n"
            r"[\s\S]*?^    rx = discord\.min\.x - 6\.0;\n",
            1,
        ),
        exact(
            "    for (id, icon, tip, cmd) in\n"
            '        [("hdr-github", Icon::Code, "EffectCraft on GitHub", "help.github"), ("hdr-web", Icon::Globe, "EffectCraft on getartcraft.com", "help.appPage")]\n'
            "    {",
            # One button left: a block instead of a loop (clippy: single_element_loop).
            '    let (id, icon, tip, cmd) = ("hdr-github", Icon::Code, "Cosmic on GitHub", "help.github");\n'
            "    {",
        ),
        # The Discord pill was the only user of the painter and of `icons::paint` here.
        exact(
            "/// The Discord pill and the GitHub and website buttons, right to left from `rx`; returns the new `rx`.\n"
            "fn community_buttons(app: &mut EffectcraftApp, ui: &mut egui::Ui, p: &egui::Painter,",
            "/// Cosmic fork: the GitHub button (Cosmic's repository), left of `rx`; returns the new `rx`.\n"
            "fn community_buttons(app: &mut EffectcraftApp, ui: &mut egui::Ui, _p: &egui::Painter,",
        ),
        exact("use crate::icons::{self, Icon};", "use crate::icons::Icon;"),
    ],
    "crates/ui-egui/tests/it/ui_panels.rs": [
        remove(r"^/// #581: the header's Discord pill[\s\S]*?^}\n\n", 1),
    ],
    # About: the same two links as Home.
    "crates/ui-egui/src/panels/dialogs.rs": [
        exact(
            "    let links: [(Icon, &str, &str, &'static str); 4] = [\n"
            '        (Icon::Chat, "Join the ArtCraft Discord", effectcraft_engine::links::DISCORD, "help.discord"),\n'
            '        (Icon::Globe, "ArtCraft website", effectcraft_engine::links::WEBSITE, "help.website"),\n'
            '        (Icon::Sparkle, "EffectCraft home page", effectcraft_engine::links::APP_PAGE, "help.appPage"),\n'
            '        (Icon::Code, "Source code on GitHub", effectcraft_engine::links::GITHUB, "help.github"),\n'
            "    ];",
            "    let links: [(Icon, &str, &str, &'static str); 2] = [\n"
            '        (Icon::Code, "Cosmic on GitHub", effectcraft_engine::links::GITHUB, "help.github"),\n'
            '        (Icon::Sparkle, "Based on EffectCraft", effectcraft_engine::links::UPSTREAM, "help.appPage"),\n'
            "    ];",
        ),
    ],
    # Open/Save dialogs, crash and graphics messages (reports go to Cosmic's issue tracker).
    "apps/effectcraft/src/file_dialogs.rs": [
        exact('"EffectCraft Project"', '"Cosmic Project"', count=4),
    ],
    "apps/effectcraft/src/main.rs": [
        exact("Reopen EffectCraft to recover them.", "Reopen Cosmic to recover them."),
        exact("so EffectCraft has to close.", "so Cosmic has to close."),
        exact(
            '"EffectCraft couldn\'t start its window: {e}\\n\\n{next}Updating the graphics driver often helps. If it keeps happening, please report it at https://github.com/storytold/effectcraft/issues with this message."',
            '"Cosmic couldn\'t start its window: {e}\\n\\n{next}Updating the graphics driver often helps. If it keeps happening, please report it at https://github.com/RkzG/cosmic/issues with this message."',
        ),
        # rustfmt joins the call once its strings are shorter.
        exact(
            "                    file_dialogs::message(\n"
            '                        "Cosmic: graphics device lost",\n'
            '                        format!("The graphics driver stopped responding, so Cosmic has to close.{saved}"),\n'
            "                    );",
            '                    file_dialogs::message("Cosmic: graphics device lost", format!("The graphics driver stopped responding, so Cosmic has to close.{saved}"));',
        ),
    ],
    "apps/effectcraft/build.rs": [
        exact('.set("OriginalFilename", "effectcraft.exe")', '.set("OriginalFilename", "cosmic.exe")'),
        exact('.set("InternalName", "effectcraft")', '.set("InternalName", "cosmic")'),
    ],
    # Settings and Learn.
    "crates/ui-egui/src/panels/settings.rs": [
        exact('tr("Stored, but not used by EffectCraft yet")', 'tr("Stored, but not used by Cosmic yet")'),
        exact("EffectCraft keeps", "Cosmic keeps", count=5),
        exact('tr("Restart EffectCraft to finish")', 'tr("Restart Cosmic to finish")'),
        exact('tr("Needs a newer EffectCraft")', 'tr("Needs a newer Cosmic")'),
        exact('tr("EffectCraft didn\'t quit normally last time.")', 'tr("Cosmic didn\'t quit normally last time.")'),
    ],
    "crates/ui-egui/src/panels/learn.rs": [
        exact("Hands-on tutorials that run inside EffectCraft.", "Hands-on tutorials that run inside Cosmic."),
    ],
    # Folders the user sees on disk.
    "crates/engine/src/settings/autosave.rs": [
        exact('pub const AUTOSAVE_FOLDER: &str = "EffectCraft Auto-Save";', 'pub const AUTOSAVE_FOLDER: &str = "Cosmic Auto-Save";'),
    ],
    "crates/engine/src/system/logging.rs": [
        exact('log_dir(config_dir).join("EffectCraft Log.txt")', 'log_dir(config_dir).join("Cosmic Log.txt")'),
    ],
    "crates/ui-egui/src/panels/effects_presets.rs": [
        exact("/// Where user presets live: `$EC_PRESETS_DIR`, else `~/Documents/EffectCraft/Presets`.", "/// Where user presets live: `$EC_PRESETS_DIR`, else `~/Documents/Cosmic/Presets`."),
        exact('.join("Documents").join("EffectCraft").join("Presets")', '.join("Documents").join("Cosmic").join("Presets")'),
    ],
    "crates/ui-egui/tests/it/ui_presets_folder.rs": [
        exact('join("Documents/EffectCraft/Presets")', 'join("Documents/Cosmic/Presets")'),
    ],
}
for _path, _edits in MORE.items():
    EDITS.setdefault(_path, []).extend(_edits)


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
