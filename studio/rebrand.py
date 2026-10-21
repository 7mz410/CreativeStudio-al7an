#!/usr/bin/env python3
"""Apply the al7an (Creative Studio) branding on top of upstream SoundCraft.

Only user-visible text is rebranded; crate names, the file format and other internals keep their
upstream names so `git merge upstream/main` stays easy. The script is idempotent: after merging
upstream, resolve any conflicts in favour of upstream and run it again.

    python3 studio/rebrand.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = 'al7an'
REPO = 'https://github.com/7mz410/CreativeStudio-al7an'
SITE = 'https://studio.creative.ps'
APP_SITE = 'https://al7an.studio.creative.ps'
# Persisted names and legal lines; renaming them would lose settings or misstate copyright.
KEEP = ('by the ArtCraft team', 'Application Support/SoundCraft', '/roaming/SoundCraft', 'SoundCraftData', 'the SoundCraft authors', 'SoundCraft contributors', 'SOUNDCRAFT_')
# Persisted names whose literal is just "SoundCraft": eframe's storage name and the Windows settings folder.
PROTECT = ('eframe::run_native(\n        "SoundCraft"', '.join("SoundCraft")')

# (file, upstream text, our text[, marker meaning "already applied"]). The upstream text may also
# be found in its renamed form (after the general rename below).
RULES = [
    # About: our links and credit line, no Discord.
    ('crates/ui-egui/src/panels.rs', 'ui.label("An open-source digital audio workstation from the ArtCraft team.");',
     'ui.label("An open-source digital audio workstation, part of the Creative Studio suite.\\nBuilt on SoundCraft by the ArtCraft team.");', 'part of the Creative Studio suite'),
    ('crates/ui-egui/src/panels.rs', 'ui.hyperlink_to("getartcraft.com/apps/soundcraft", "https://getartcraft.com/apps/soundcraft");',
     f'ui.hyperlink_to("al7an.studio.creative.ps", "{APP_SITE}");', 'al7an.studio.creative.ps'),
    ('crates/ui-egui/src/panels.rs', 'ui.hyperlink_to("Join us on Discord", "https://discord.gg/artcraft");',
     f'ui.hyperlink_to("Source code: github.com/7mz410/CreativeStudio-al7an", "{REPO}");', 'CreativeStudio-al7an'),
    ('crates/clap-host/src/ffi.rs', 'url: c"https://github.com/storytold/soundcraft".as_ptr(),', f'url: c"{REPO}".as_ptr(),'),
    # Web page and packages.
    ('apps/soundcraft-web/index.html', '<title>SoundCraft</title>', f'<title>{NAME}</title>'),
    ('apps/soundcraft-web/index.html', 'Loading SoundCraft&hellip;', f'Loading {NAME}&hellip;', 'ss-scene'),  # the splash replaced the text
    ('packaging/macos/Info.plist.in', '<string>ai.storyteller.soundcraft</string>', '<string>ps.creative.studio.al7an</string>'),
    ('packaging/windows/soundcraft.wxs', '<Property Id="ARPURLINFOABOUT" Value="https://getartcraft.com/apps/soundcraft" />', f'<Property Id="ARPURLINFOABOUT" Value="{APP_SITE}" />'),
    ('packaging/windows/soundcraft.wxs', '<Property Id="ARPURLUPDATEINFO" Value="https://getartcraft.com/apps/soundcraft" />', f'<Property Id="ARPURLUPDATEINFO" Value="{REPO}/releases" />'),
    ('packaging/windows/soundcraft.wxs', '<Property Id="ARPHELPLINK" Value="https://discord.gg/artcraft" />', f'<Property Id="ARPHELPLINK" Value="{REPO}/issues" />'),
    ('packaging/windows/sign.ps1', "'/du', 'https://github.com/storytold/soundcraft'", f"'/du', '{REPO}'"),
    ('packaging/linux/nfpm.yaml', 'homepage: https://getartcraft.com/apps/soundcraft', f'homepage: {APP_SITE}'),
    ('packaging/linux/ai.storyteller.soundcraft.desktop', 'Name=SoundCraft\n', f'Name={NAME}\n'),
    ('packaging/linux/ai.storyteller.soundcraft.metainfo.xml.in', '  <name>SoundCraft</name>', f'  <name>{NAME}</name>'),
    ('packaging/linux/ai.storyteller.soundcraft.metainfo.xml.in', '<url type="homepage">https://getartcraft.com/apps/soundcraft</url>', f'<url type="homepage">{APP_SITE}</url>'),
    ('packaging/linux/ai.storyteller.soundcraft.metainfo.xml.in', '<url type="bugtracker">https://github.com/storytold/soundcraft/issues</url>', f'<url type="bugtracker">{REPO}/issues</url>'),
    ('packaging/linux/ai.storyteller.soundcraft.metainfo.xml.in', '<url type="help">https://github.com/storytold/soundcraft</url>', f'<url type="help">{REPO}</url>'),
    ('packaging/linux/ai.storyteller.soundcraft.metainfo.xml.in', '<url type="contact">https://discord.gg/artcraft</url>', f'<url type="contact">{SITE}</url>'),
]
# Creative Studio: sessions save as `.al7an` (own extension, own document icon); upstream's `.scraft`
# still opens. Same approach as rsm (STUDIO_EXTENSION next to upstream's). Applied by apply_rules.
RULES += [
    ('crates/model/src/session.rs', r'''pub const SESSION_EXTENSION: &str = "scraft";''',
     r'''pub const SESSION_EXTENSION: &str = "scraft";
/// Creative Studio saves sessions as `.al7an`; upstream's `.scraft` still opens.
pub const STUDIO_EXTENSION: &str = "al7an";'''),
    ('crates/model/src/lib.rs', 'MAX_NAME_CHARS, SESSION_EXTENSION, Session,',
     'MAX_NAME_CHARS, SESSION_EXTENSION, STUDIO_EXTENSION, Session,'),
    ('crates/engine/src/io.rs', 'with `.scraft` added when it has no',
     'with `.al7an` added when it has no'),
    ('crates/engine/src/io.rs', 'p.with_extension(soundcraft_model::SESSION_EXTENSION) } else { p }',
     'p.with_extension(soundcraft_model::STUDIO_EXTENSION) } else { p }'),
    ('crates/engine/src/cmd/file.rs', 'p.extension().is_some_and(|x| x != "scraft")',
     'p.extension().is_some_and(|x| x != "scraft" && x != "al7an")'),
    ('crates/engine/src/cmd/file.rs', '    #[test]\n    fn save_copy_leaves_the_open_session_alone() {',
     r'''    #[test]
    fn sessions_save_as_al7an_and_scraft_still_opens() {
        let (mut e, _) = tone_engine();
        let dir = std::env::temp_dir().join(format!("sc-al7an-ext-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        e.execute("session.save_as", &json!({"path": dir.join("Plain").to_string_lossy()})).unwrap();
        assert!(dir.join("Plain.al7an").is_file(), "a name without an extension saves as .al7an");
        let old = dir.join("Old.scraft");
        std::fs::copy(dir.join("Plain.al7an"), &old).unwrap();
        let mut opened = Engine::default();
        opened.execute("session.open", &json!({"path": old.to_string_lossy()})).unwrap();
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn save_copy_leaves_the_open_session_alone() {'''),
    ('apps/soundcraft/src/main.rs', '//! Usage: `soundcraft [--demo] [--control <port>] [--no-audio] [session.scraft | audio files…]`',
     '//! Usage: `soundcraft [--demo] [--control <port>] [--no-audio] [session.al7an | session.scraft | audio files…]`'),
    ('apps/soundcraft/src/main.rs', 'let r = if lower.ends_with(".scraft") {',
     'let r = if lower.ends_with(".scraft") || lower.ends_with(".al7an") {'),
    ('apps/soundcraft/src/main.rs', '"session.open" => d.add_filter("al7an Session", &["scraft"]),',
     '"session.open" => d.add_filter("al7an Session", &["al7an", "scraft"]),'),
    ('apps/soundcraft/src/main.rs', '_ => rfd::FileDialog::new().add_filter("al7an Session", &["scraft"]),',
     '_ => rfd::FileDialog::new().add_filter("al7an Session", &["al7an", "scraft"]),'),
    ('apps/soundcraft-cli/src/main.rs', 'if path.ends_with(".scraft") {',
     'if path.ends_with(".scraft") || path.ends_with(".al7an") {'),
    ('crates/ui-egui/src/windows.rs', '"midi", "scraft"].contains(&ext.as_str()))',
     '"midi", "scraft", "al7an"].contains(&ext.as_str()))'),
    ('apps/soundcraft-web/src/web.rs', 'const SESSION_EXTS: &[&str] = &[io::BUNDLE_EXTENSION, soundcraft_model::SESSION_EXTENSION];',
     'const SESSION_EXTS: &[&str] = &[io::BUNDLE_EXTENSION, soundcraft_model::STUDIO_EXTENSION, soundcraft_model::SESSION_EXTENSION];'),
    ('apps/soundcraft-web/src/web.rs', 'Some("json" | "scraft") => "application/json",',
     'Some("json" | "scraft" | "al7an") => "application/json",'),
    ('packaging/linux/ai.storyteller.soundcraft.desktop', 'MimeType=application/x-soundcraft-session;',
     'MimeType=application/x-al7an-session;application/x-soundcraft-session;'),
    ('packaging/linux/ai.storyteller.soundcraft.mime.xml', '</mime-info>',
     r'''  <mime-type type="application/x-al7an-session">
    <comment>al7an session</comment>
    <sub-class-of type="application/json"/>
    <icon name="ai.storyteller.soundcraft"/>
    <glob pattern="*.al7an"/>
  </mime-type>
</mime-info>'''),
    ('packaging/windows/soundcraft.wxs', '''          </Extension>
        </ProgId>
        <!-- Audio and MIDI files''',
     '''          </Extension>
        </ProgId>
        <!-- .al7an: al7an's own session extension. Its own ProgId, since two Extensions with an "open"
             Verb under one ProgId write the same shell\open\command key (WIX0091). -->
        <ProgId Id="Al7an.Session" Description="al7an Session" Icon="SoundcraftExe" IconIndex="0">
          <Extension Id="al7an" ContentType="application/x-al7an-session">
            <Verb Id="open" Command="Open" TargetFile="SoundcraftExe" Argument="&quot;%1&quot;" />
          </Extension>
        </ProgId>
        <!-- Audio and MIDI files'''),
    ('packaging/windows/soundcraft.wxs', r'''Name=".scraft" Value="" Type="string" />''',
     r'''Name=".scraft" Value="" Type="string" />
        <RegistryValue Root="HKLM" Key="Software\Classes\Applications\soundcraft.exe\SupportedTypes" Name=".al7an" Value="" Type="string" />'''),
    ('packaging/macos/Info.plist.in', '''  <key>UTExportedTypeDeclarations</key>
  <array>
''',
     '''  <key>UTExportedTypeDeclarations</key>
  <array>
    <!-- al7an's session: the same JSON file as .scraft, saved with the .al7an extension. -->
    <dict>
      <key>UTTypeIdentifier</key>
      <string>ps.creative.studio.al7an.session</string>
      <key>UTTypeDescription</key>
      <string>al7an Session</string>
      <key>UTTypeConformsTo</key>
      <array>
        <string>public.data</string>
        <string>public.content</string>
      </array>
      <key>UTTypeIconFile</key>
      <string>al7an-document</string>
      <key>UTTypeTagSpecification</key>
      <dict>
        <key>public.filename-extension</key>
        <array><string>al7an</string></array>
        <key>public.mime-type</key>
        <array><string>application/x-al7an-session</string></array>
      </dict>
    </dict>
'''),
    ('packaging/macos/Info.plist.in', '''<key>CFBundleTypeName</key>
      <string>SoundCraft Session</string>''',
     '''<key>CFBundleTypeName</key>
      <string>al7an Session</string>'''),
    ('packaging/macos/Info.plist.in', '''<key>CFBundleTypeIconFile</key>
      <string>SoundCraft</string>
      <key>LSItemContentTypes</key>
      <array><string>ai.storyteller.soundcraft.session</string></array>''',
     '''<key>CFBundleTypeIconFile</key>
      <string>al7an-document</string>
      <key>LSItemContentTypes</key>
      <array><string>ps.creative.studio.al7an.session</string><string>ai.storyteller.soundcraft.session</string></array>'''),
    ('packaging/macos/package.sh', 'cp "$ROOT/assets/app-icon/soundcraft.icns" "$APP/Contents/Resources/SoundCraft.icns"\n',
     'cp "$ROOT/assets/app-icon/soundcraft.icns" "$APP/Contents/Resources/SoundCraft.icns"\ncp "$ROOT/assets/app-icon/al7an-document.icns" "$APP/Contents/Resources/al7an-document.icns"\n'),
    ('ATTRIBUTION.md', '| `assets/app-icon/icon.svg` |',
     '| `assets/app-icon/al7an-document.svg` | Hamza Abu Ayyash (Creative Studio) | the mzika icon (`file icons/mzika.svg`, the former name of this app) used as the document icon | MIT OR Apache-2.0 | Document icon of `.al7an` sessions |\n'
     '| `assets/app-icon/al7an-document.icns` | Hamza Abu Ayyash (Creative Studio) | `assets/app-icon/al7an-document.svg` rendered with rsvg-convert, packed with iconutil | MIT OR Apache-2.0 | Document icon of `.al7an` sessions |\n'
     '| `assets/app-icon/icon.svg` |'),
    ('studio/CHANGES.md', 'settings folders and the file format keep their upstream names.',
     'settings folders and the session JSON keep their upstream names.'),
    ('studio/CHANGES.md', '- No Discord buttons; community links point to Creative Studio.',
     '- No Discord buttons; community links point to Creative Studio.\n'
     '- Sessions save as `.al7an`, with their own document icon (`assets/app-icon/al7an-document.*`). `.scraft`,\n'
     '  upstream\'s extension, still opens.'),
]
# Text in string literals and catalogs, before the general rename.
LITERALS = []
STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def rename(lit: str) -> str:
    for a, b in LITERALS:
        lit = lit.replace(a, b)
    if any(k in lit for k in KEEP):
        return lit
    return lit.replace('SoundCraft', NAME)


def renamed_code(text: str) -> str:
    held = {f'\0{i}\0': k for i, k in enumerate(PROTECT)}
    for h, k in held.items():
        text = text.replace(k, h)
    text = STRING.sub(lambda m: rename(m.group(0)), text)
    for h, k in held.items():
        text = text.replace(h, k)
    return text


def apply_rules() -> list:
    changed = []
    for rel, a, b, *marker in RULES:
        p = ROOT / rel
        s = p.read_text(encoding='utf-8')
        if marker and marker[0] in s:
            continue
        if a not in s and renamed_code(a) in s:
            a = renamed_code(a)  # the general rename got there first
        if a not in s or (b and a in b and b in s):
            if not b or b in s or renamed_code(b) in s:
                continue  # already applied
            print(f'warning: {rel}: upstream text not found (did upstream change it?): {a[:70]!r}')
            continue
        p.write_text(s.replace(a, b), encoding='utf-8')
        changed.append(rel)
    return changed


def rename_sources() -> list:
    changed = []
    for p in sorted((ROOT / 'crates/ui-egui').rglob('*.rs')) + [q for q in sorted((ROOT / 'crates/engine').rglob('*.rs')) if not q.name.startswith('tests') and 'tests' not in q.parts] + sorted((ROOT / 'apps').rglob('*.rs')):
        s = p.read_text(encoding='utf-8')
        o = renamed_code(s)
        if o != s:
            p.write_text(o, encoding='utf-8')
            changed.append(p.relative_to(ROOT).as_posix())
    plist = ROOT / 'packaging/macos/Info.plist.in'
    s = plist.read_text(encoding='utf-8')
    o = re.sub(r'(<key>CFBundle(?:Display|Executable)?Name</key>\s*<string>)SoundCraft(</string>)', rf'\g<1>{NAME}\2', s)
    if o != s:
        plist.write_text(o, encoding='utf-8')
        changed.append('packaging/macos/Info.plist.in')
    return changed


def main():
    changed = apply_rules() + rename_sources()
    for c in sorted(set(changed)):
        print('rebranded', c)


if __name__ == '__main__':
    main()
