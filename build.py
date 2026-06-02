#!/usr/bin/env python3
"""Build the 'Save Pasted Image' Alfred workflow into an installable
.alfredworkflow bundle (a zip containing an info.plist).

Usage:  python3 build.py
Output: dist/Save Pasted Image.alfredworkflow
"""

import os
import plistlib
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src", "save-pasted-image.applescript")
ICON = os.path.join(HERE, "src", "save-image-icon.png")
DIST = os.path.join(HERE, "dist")
OUT = os.path.join(DIST, "Save Pasted Image.alfredworkflow")

# UIDs are arbitrary but must be stable/unique within the workflow.
KEYWORD_UID = "A1B2C3D4-0001-0001-0001-000000000001"
SCRIPT_UID = "A1B2C3D4-0002-0002-0002-000000000002"


def build_plist(applescript: str) -> bytes:
    keyword_object = {
        "uid": KEYWORD_UID,
        "type": "alfred.workflow.input.keyword",
        "version": 1,
        "config": {
            "argumenttype": 2,  # 2 = takes no argument
            "keyword": "savePastedImage",
            "subtext": "Pick a folder and save the clipboard image there",
            "text": "Save Pasted Image",
            "withspace": False,
        },
    }

    # Run via /bin/bash (type 0 — the reliable, well-known language id) and
    # call osascript on the AppleScript file bundled alongside info.plist.
    # Alfred sets the working directory to the workflow folder, so "./" works.
    # This avoids the ambiguous osascript language-type ids in the Run Script
    # dropdown, which is what was silently failing before.
    script_object = {
        "uid": SCRIPT_UID,
        "type": "alfred.workflow.action.script",
        "version": 2,
        "config": {
            "concurrently": False,
            "escaping": 0,
            "script": "/usr/bin/osascript ./save-pasted-image.applescript",
            "scriptargtype": 1,  # 1 = pass input as argv (unused here)
            "scriptfile": "",
            "type": 0,  # 0 = /bin/bash
            "wd": "",
        },
    }

    info = {
        "bundleid": "com.willwashburn.savepastedimage",
        "name": "Save Pasted Image",
        "description": "Save the image on your clipboard to a folder you choose.",
        "createdby": "Will Washburn",
        "category": "Tools",
        "readme": (
            "Type the keyword `savePastedImage` (no argument needed). "
            "You'll be asked to choose a destination folder, and the image "
            "currently on your clipboard is saved there as a timestamped PNG."
        ),
        "webaddress": "",
        "disabled": False,
        "objects": [keyword_object, script_object],
        "connections": {
            KEYWORD_UID: [
                {
                    "destinationuid": SCRIPT_UID,
                    "modifiers": 0,
                    "modifiersubtext": "",
                    "vitoclose": False,
                }
            ]
        },
        "uidata": {
            KEYWORD_UID: {"xpos": 30, "ypos": 30},
            SCRIPT_UID: {"xpos": 300, "ypos": 30},
        },
        "version": "1.0",
    }
    return plistlib.dumps(info)


def main() -> None:
    with open(SRC, "r", encoding="utf-8") as fh:
        applescript = fh.read()

    os.makedirs(DIST, exist_ok=True)
    plist_bytes = build_plist(applescript)

    if os.path.exists(OUT):
        os.remove(OUT)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("info.plist", plist_bytes)
        # The bash action runs `osascript ./save-pasted-image.applescript`,
        # so the script must live inside the bundle at that path.
        zf.write(SRC, "save-pasted-image.applescript")
        # Alfred uses a file literally named icon.png as the workflow's icon.
        if os.path.exists(ICON):
            zf.write(ICON, "icon.png")
        else:
            print(f"WARNING: icon not found at {ICON}; building without it")

    print(f"Built: {OUT}")


if __name__ == "__main__":
    main()
