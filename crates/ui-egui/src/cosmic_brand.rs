//! Cosmic fork branding: the name, logo and About text the desktop app shows in place of
//! EffectCraft's. Upstream files reach these through the one-line hooks that
//! `cosmic/tools/rebrand.py` applies (listed in `cosmic/docs/UPSTREAM-PATCHES.md`).

/// The app's display name.
pub const NAME: &str = "Cosmic";

/// The line under the name in the About dialog.
pub const TAGLINE: &str = "AI-assisted video editor";

/// The About dialog's description. The ArtCraft brand terms let a fork say, in plain text, that
/// it is based on EffectCraft by the ArtCraft team, but not present itself as an ArtCraft product.
pub const ABOUT_BLURB: &str = "Cosmic is a video editor with AI as a collaborator, based on EffectCraft by the ArtCraft team. \
     It is not made, sponsored or endorsed by the ArtCraft team.";

/// The Cosmic app icon (a spiral galaxy forming a C), drawn where EffectCraft drew the ArtCraft
/// mark: the Tools bar and the About dialog. Original work, see `cosmic/assets/app-icon`.
pub static LOGO_PNG: &[u8] = include_bytes!("../../../cosmic/assets/app-icon/cosmic-256.png");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_logo_decodes_as_a_square_png() {
        let img = image::load_from_memory_with_format(LOGO_PNG, image::ImageFormat::Png).unwrap();
        assert_eq!((img.width(), img.height()), (256, 256));
    }

    #[test]
    fn the_about_text_names_cosmic_and_credits_effectcraft() {
        assert_eq!(NAME, "Cosmic");
        assert!(ABOUT_BLURB.contains("based on EffectCraft by the ArtCraft team"));
        assert!(ABOUT_BLURB.contains("not made, sponsored or endorsed"));
    }
}
