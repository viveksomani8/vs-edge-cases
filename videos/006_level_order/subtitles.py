"""Write an .srt subtitle file from narration.py and a clip timeline.

Usage:
    python subtitles.py <timeline.json> <output.srt>

The cue splitting is 001_dutch_flag/make_subtitles.py, given this video's
script with the spoken spellings replaced by the real names.
"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "001_dutch_flag"))

import make_subtitles
from narration import NARRATION, SUBTITLE_SPELLINGS


def written(text):
    for spoken, real in SUBTITLE_SPELLINGS:
        text = text.replace(spoken, real).replace(spoken.capitalize(), real)
    return text


make_subtitles.NARRATION = {name: written(text) for name, text in NARRATION.items()}

if __name__ == "__main__":
    make_subtitles.main(*sys.argv[1:3])
