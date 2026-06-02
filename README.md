# alfred-save-image

An Alfred workflow that saves the image on your clipboard to a folder you choose.

## Install

1. Build the workflow (or use the prebuilt one in `dist/`):
   ```sh
   python3 build.py
   ```
2. Double-click `dist/Save Pasted Image.alfredworkflow` to install it into Alfred.

> Requires Alfred with the **Powerpack** (workflows are a Powerpack feature).

## Use

1. Copy any image (screenshot, image in a browser, etc.) so it's on your clipboard.
2. Open Alfred and type the keyword:
   ```
   savePastedImage
   ```
3. A folder picker appears — choose where to save.
4. The image is written there as `pasted-image-YYYY-MM-DD_HH-MM-SS.png`, and a
   notification confirms the path.

If there's no image on the clipboard, you'll get a notification telling you so.

## How it works

The workflow is a single keyword wired to an AppleScript action. The script
([`src/save-pasted-image.applescript`](src/save-pasted-image.applescript)):

- reads the clipboard as PNG (falling back to TIFF),
- prompts for a destination folder with the native picker,
- writes the bytes to a timestamped `.png` file.

`build.py` assembles the `info.plist` and zips it into the installable
`.alfredworkflow` bundle under `dist/`.
