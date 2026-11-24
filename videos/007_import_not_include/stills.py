"""Save one PNG per beat of a rendered preview.

    python stills.py <video.mp4> <stills.json> <output folder>

The scene writes stills.json: a list of [clip name, seconds], the moment just
before each beat is cleared.
"""

import json
import sys
from pathlib import Path

import av


def main(video, stills, out_dir):
    wanted = json.loads(Path(stills).read_text())
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with av.open(video) as container:
        stream = container.streams.video[0]
        pending = list(wanted)
        for frame in container.decode(stream):
            if not pending:
                break
            name, seconds = pending[0]
            if frame.time >= seconds:
                path = out / f"{len(wanted) - len(pending) + 1:02d}-{name}.png"
                frame.to_image().save(path)
                print(path)
                pending.pop(0)


if __name__ == "__main__":
    main(*sys.argv[1:4])
