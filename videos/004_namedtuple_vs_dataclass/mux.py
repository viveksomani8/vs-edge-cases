"""Lay this video's narration clips onto a silent render and check the result.

Usage:
    python mux.py <silent_video.mp4> <timeline.json> <output.mp4>

Works for the main video and the Short: the timeline written by the scene names
the clips (audio/<name>.mp3). The mixing itself is 001_dutch_flag/mux_narration.py.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "001_dutch_flag"))

import av

import mux_narration

mux_narration.AUDIO_DIR = HERE / "audio"


def main(video, timeline_path, output):
    timeline = json.loads(Path(timeline_path).read_text())
    unrecorded = [name for name, *_ in timeline if not (HERE / "audio" / f"{name}.mp3").exists()]
    if unrecorded:
        print(f"Not recorded yet: {', '.join(unrecorded)}")
        return 1
    with av.open(str(video)) as src:
        seconds = float(src.duration) / av.time_base
    mux_narration.mux(video, mux_narration.build_track(timeline, seconds), output)
    audio_seconds, missing = mux_narration.verify(output, timeline)
    print(f"video {seconds:.1f}s, audio {audio_seconds:.1f}s, clips {len(timeline)}, missing {missing or 'none'}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
