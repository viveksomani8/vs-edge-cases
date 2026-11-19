"""Lay the narration clips onto a silent render and check the result.

Usage:
    python mux_narration.py <silent_video.mp4> <narration_timeline.json> <output.mp4>

The timeline is written by scene.py: a list of [clip_name, start_s, end_s],
where clip_name is the file stem in audio/ ("01".."25", "hook", "outro").
"""

import json
import sys
from pathlib import Path

import av
import numpy as np

RATE = 44100
AUDIO_DIR = Path(__file__).parent / "audio"


def decode_mono(path, rate=RATE):
    """Return a clip (or a video's audio track) as float samples in [-1, 1]."""
    resampler = av.AudioResampler(format="s16", layout="mono", rate=rate)
    parts = []
    with av.open(str(path)) as container:
        for frame in container.decode(audio=0):
            parts += [r.to_ndarray().ravel() for r in resampler.resample(frame)]
        parts += [r.to_ndarray().ravel() for r in resampler.resample(None)]
    return np.concatenate(parts).astype(np.float64) / 32768


def build_track(timeline, seconds):
    track = np.zeros(int(seconds * RATE) + RATE)
    for clip, start, _end in timeline:
        samples = decode_mono(AUDIO_DIR / f"{clip}.mp3")
        at = int(start * RATE)
        track[at:at + len(samples)] += samples[: len(track) - at]
    return np.clip(track, -1, 1)


def mux(video, track, output):
    pcm = (track * 32767).astype(np.int16)
    to_aac = av.AudioResampler(format="fltp", layout="mono", rate=RATE)
    with av.open(str(video)) as src, av.open(str(output), "w") as dst:
        v_in = src.streams.video[0]
        v_out = dst.add_stream_from_template(v_in)
        a_out = dst.add_stream("aac", rate=RATE, layout="mono")
        for packet in src.demux(v_in):
            if packet.dts is not None:
                packet.stream = v_out
                dst.mux(packet)
        for i in range(0, len(pcm), 1024):
            frame = av.AudioFrame.from_ndarray(pcm[i:i + 1024].reshape(1, -1), format="s16", layout="mono")
            frame.sample_rate = RATE
            frame.pts = i
            for resampled in to_aac.resample(frame):
                dst.mux(a_out.encode(resampled))
        dst.mux(a_out.encode(None))


def verify(output, timeline):
    """Every clip must be audible in the output during its scheduled window."""
    audio = decode_mono(output, rate=16000)
    missing = []
    for clip, start, end in timeline:
        window = audio[int(start * 16000):int(end * 16000)]
        rms = float(np.sqrt(np.mean(window ** 2))) if len(window) else 0.0
        if rms < 0.01:
            missing.append(clip)
    return len(audio) / 16000, missing


def main(video, timeline_path, output):
    timeline = json.loads(Path(timeline_path).read_text())
    with av.open(str(video)) as src:
        seconds = float(src.duration) / av.time_base
    mux(video, build_track(timeline, seconds), output)
    audio_seconds, missing = verify(output, timeline)
    print(f"video {seconds:.1f}s, audio {audio_seconds:.1f}s, clips {len(timeline)}, missing {missing or 'none'}")
    expected = len(list(AUDIO_DIR.glob("*.mp3")))
    return 1 if missing or len(timeline) != expected else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
