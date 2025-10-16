#!/usr/bin/env python3
"""Generate an Autocanonizer-compatible analysis profile for a local audio file."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import librosa
import numpy as np


# Analysis constants
HOP_LENGTH = 512
SEGMENT_MIN_DURATION = 0.08  # seconds
DEFAULT_TIME_SIGNATURE = 4
TATUMS_PER_BEAT = 3
SILENCE_DB = -60.0
MIN_SECTION_DURATION = 2.0


@dataclass
class Quantum:
    start: float
    duration: float
    confidence: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "start": float(self.start),
            "duration": float(self.duration),
            "confidence": float(self.confidence),
        }


def normalize(values: np.ndarray) -> np.ndarray:
    """Scale values into [0, 1] with safe fallback."""
    if values.size == 0:
        return values
    vmin = float(np.min(values))
    vmax = float(np.max(values))
    if math.isclose(vmin, vmax):
        return np.ones_like(values) * 0.5
    return (values - vmin) / (vmax - vmin)


def compute_beats(y: np.ndarray, sr: int) -> Tuple[List[Quantum], np.ndarray, float]:
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP_LENGTH)
    tempo, beat_frames = librosa.beat.beat_track(
        onset_envelope=onset_env, sr=sr, hop_length=HOP_LENGTH
    )
    tempo = float(np.atleast_1d(tempo)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP_LENGTH)
    strengths = onset_env[beat_frames] if beat_frames.size else np.array([])
    confidences = normalize(strengths) if strengths.size else np.array([])

    duration = librosa.get_duration(y=y, sr=sr)
    beats = []
    for idx, start in enumerate(beat_times):
        end = (
            beat_times[idx + 1]
            if idx + 1 < len(beat_times)
            else duration
        )
        beats.append(
            Quantum(
                start=start,
                duration=max(end - start, 1e-5),
                confidence=float(confidences[idx] if idx < len(confidences) else 0.7),
            )
        )
    return beats, beat_times, tempo


def derive_bars(
    beats: List[Quantum],
    beat_times: np.ndarray,
    duration: float,
    time_signature: int = DEFAULT_TIME_SIGNATURE,
) -> List[Quantum]:
    bars: List[Quantum] = []
    for i in range(0, len(beats), time_signature):
        start = beats[i].start
        if i + time_signature < len(beats):
            end = beats[i + time_signature].start
        else:
            end = duration
        conf_slice = [b.confidence for b in beats[i : i + time_signature]]
        confidence = float(np.mean(conf_slice)) if conf_slice else 0.7
        bars.append(
            Quantum(
                start=start,
                duration=max(end - start, 1e-5),
                confidence=confidence,
            )
        )
    return bars


def derive_tatums(
    beats: List[Quantum],
    duration: float,
    tatums_per_beat: int = TATUMS_PER_BEAT,
) -> List[Quantum]:
    tatums: List[Quantum] = []
    for beat in beats:
        step = beat.duration / tatums_per_beat
        for sub in range(tatums_per_beat):
            start = beat.start + sub * step
            end = start + step if sub < tatums_per_beat - 1 else beat.start + beat.duration
            tatums.append(
                Quantum(
                    start=start,
                    duration=max(end - start, 1e-5),
                    confidence=beat.confidence,
                )
            )
    # ensure final tatum hits track end
    if tatums:
        tatums[-1].duration = max(duration - tatums[-1].start, 1e-5)
    return tatums


def estimate_sections(
    y: np.ndarray,
    sr: int,
    duration: float,
    desired_sections: int,
    bars: List[Quantum],
) -> List[Quantum]:
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=HOP_LENGTH)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=HOP_LENGTH)
    features = np.vstack(
        (librosa.util.normalize(chroma), librosa.util.normalize(mfcc))
    )

    n_frames = features.shape[1]
    k = max(2, min(desired_sections, n_frames))
    labels = librosa.segment.agglomerative(features.T, k=k)
    boundaries = [0]
    for idx in range(1, len(labels)):
        if labels[idx] != labels[idx - 1]:
            boundaries.append(idx)
    boundaries.append(n_frames - 1)
    boundaries = sorted(set(boundaries))
    raw_times = librosa.frames_to_time(boundaries, sr=sr, hop_length=HOP_LENGTH)
    times: List[float] = [0.0]
    for idx in range(1, len(raw_times)):
        current = float(raw_times[idx])
        delta = current - times[-1]
        is_last = idx == len(raw_times) - 1
        if delta < MIN_SECTION_DURATION and not is_last:
            continue
        times.append(current)
    if times[-1] < duration:
        times.append(duration)
    sections: List[Quantum] = []
    for idx, start in enumerate(times[:-1]):
        end = times[idx + 1]
        duration = max(float(end - start), 1e-5)
        new_section = Quantum(
            start=float(start),
            duration=duration,
            confidence=1.0,
        )
        if sections and new_section.duration < MIN_SECTION_DURATION:
            # merge into previous section
            prev = sections[-1]
            prev_end = prev.start + prev.duration
            prev.duration = max(prev_end, new_section.start + new_section.duration) - prev.start
        else:
            sections.append(new_section)
    # pad last section to end if needed
    if sections:
        last = sections[-1]
        last.duration = max(duration - last.start, 1e-5)
    if len(sections) >= max(2, desired_sections // 2):
        return sections

    # Fallback: derive sections from bar groups
    if not bars:
        return [Quantum(0.0, duration, 1.0)]

    target_sections = max(2, min(desired_sections, len(bars)))
    bars_per_section = max(1, len(bars) // target_sections)
    fallback_sections: List[Quantum] = []
    idx = 0
    while idx < len(bars):
        bar = bars[idx]
        start = float(bar.start if idx > 0 else 0.0)
        end_idx = min(len(bars) - 1, idx + bars_per_section - 1)
        end_bar = bars[end_idx]
        end = float(end_bar.start + end_bar.duration)
        fallback_sections.append(
            Quantum(
                start=start,
                duration=max(end - start, 1e-5),
                confidence=0.8,
            )
        )
        idx += bars_per_section

    if fallback_sections:
        fallback_sections[-1].duration = max(
            duration - fallback_sections[-1].start, 1e-5
        )
    return fallback_sections or [Quantum(0.0, duration, 1.0)]


def compute_segments(
    y: np.ndarray,
    sr: int,
    duration: float,
) -> List[Dict[str, object]]:
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP_LENGTH)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        hop_length=HOP_LENGTH,
        backtrack=True,
    )

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=HOP_LENGTH)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=HOP_LENGTH)
    rms = librosa.feature.rms(y=y, hop_length=HOP_LENGTH)[0]

    boundaries: List[int] = [0]
    boundaries.extend(sorted(set(int(b) for b in onset_frames)))
    end_frame = int(math.ceil(duration * sr / HOP_LENGTH))
    boundaries.append(end_frame)
    boundaries = sorted(boundaries)

    onset_strength_norm = normalize(onset_env)
    segments: List[Dict[str, object]] = []
    for start_frame, end_frame in zip(boundaries[:-1], boundaries[1:]):
        if end_frame <= start_frame:
            end_frame = start_frame + 1
        start_time = librosa.frames_to_time(start_frame, sr=sr, hop_length=HOP_LENGTH)
        end_time = librosa.frames_to_time(end_frame, sr=sr, hop_length=HOP_LENGTH)
        duration_sec = max(end_time - start_time, SEGMENT_MIN_DURATION)

        frame_slice = slice(start_frame, end_frame)
        seg_mfcc = mfcc[:, frame_slice]
        seg_chroma = chroma[:, frame_slice]
        seg_rms = rms[frame_slice]
        seg_onset_strength = onset_strength_norm[frame_slice]

        if seg_mfcc.size == 0:
            seg_mfcc = mfcc[:, start_frame : start_frame + 1]
        if seg_chroma.size == 0:
            seg_chroma = chroma[:, start_frame : start_frame + 1]
        if seg_rms.size == 0:
            seg_rms = np.array([0.0])
        if seg_onset_strength.size == 0:
            seg_onset_strength = np.array([0.5])

        timbre = np.mean(seg_mfcc[1:13, :], axis=1)
        pitches = np.mean(seg_chroma, axis=1)
        pitches = pitches / np.sum(pitches) if np.sum(pitches) > 0 else pitches

        loudness = librosa.amplitude_to_db(seg_rms, ref=1.0)
        loud_start = float(loudness[0]) if loudness.size else SILENCE_DB
        max_idx = int(np.argmax(loudness)) if loudness.size else 0
        loud_max = float(loudness[max_idx]) if loudness.size else SILENCE_DB
        loud_max_time = (
            librosa.frames_to_time(start_frame + max_idx, sr=sr, hop_length=HOP_LENGTH)
            - start_time
        )

        confidence = float(np.mean(seg_onset_strength))

        segments.append(
            {
                "start": float(start_time),
                "duration": float(duration_sec),
                "confidence": confidence,
                "loudness_start": loud_start,
                "loudness_max": loud_max,
                "loudness_max_time": float(max(loud_max_time, 0.0)),
                "pitches": [float(v) for v in pitches.tolist()],
                "timbre": [float(v) for v in timbre.tolist()],
            }
        )

    # force final segment to land exactly on track end
    if segments:
        last = segments[-1]
        last["duration"] = float(max(duration - last["start"], SEGMENT_MIN_DURATION))
    return segments


def estimate_key(chroma: np.ndarray) -> Tuple[int, int]:
    """Return (key_index, mode) where key_index is 0=C ... 11=B."""
    # Temperley-style key profiles (Krumhansl-Schmuckler)
    major_profile = np.array(
        [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
    )
    minor_profile = np.array(
        [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
    )
    chroma_mean = np.mean(chroma, axis=1)
    if np.allclose(chroma_mean.sum(), 0):
        return 0, 1
    scores_major = [
        np.correlate(np.roll(major_profile, i), chroma_mean, mode="valid")[0]
        for i in range(12)
    ]
    scores_minor = [
        np.correlate(np.roll(minor_profile, i), chroma_mean, mode="valid")[0]
        for i in range(12)
    ]
    major_key = int(np.argmax(scores_major))
    minor_key = int(np.argmax(scores_minor))
    if max(scores_major) >= max(scores_minor):
        return major_key, 1
    return minor_key, 0


def build_profile(
    audio_path: Path,
    track_id: str,
    title: str,
    artist: str,
    audio_url: str,
    output_path: Path,
) -> Dict[str, object]:
    y, sr = librosa.load(audio_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    beats, beat_times, tempo = compute_beats(y, sr)
    if not beats:
        # fallback: create a simple evenly spaced grid
        grid = np.linspace(0, duration, num=max(int(duration * 2), 2), endpoint=False)
        beats = [
            Quantum(
                start=float(t),
                duration=float(min(duration - t, duration / len(grid))),
                confidence=0.5,
            )
            for t in grid
        ]
        beat_times = np.array([b.start for b in beats])
        tempo = 60.0 / beats[0].duration if beats and beats[0].duration > 0 else 120.0

    bars = derive_bars(beats, beat_times, duration)
    tatums = derive_tatums(beats, duration)

    desired_sections = max(2, min(12, len(beats) // 8 or 2))
    sections = estimate_sections(y, sr, duration, desired_sections, bars)
    segments = compute_segments(y, sr, duration)

    chroma_full = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=HOP_LENGTH)
    key_index, mode = estimate_key(chroma_full)
    loudness_global = float(np.mean(librosa.amplitude_to_db(np.abs(y), ref=1.0)))

    profile = {
        "response": {
            "status": {"code": 0, "message": "OK"},
            "track": {
                "id": track_id,
                "title": title,
                "artist": artist,
                "status": "complete",
                "info": {"url": audio_url},
                "audio_summary": {
                    "duration": float(duration),
                    "tempo": float(tempo),
                    "time_signature": DEFAULT_TIME_SIGNATURE,
                    "key": int(key_index),
                    "mode": int(mode),
                    "loudness": loudness_global,
                    "analysis_sample_rate": sr,
                },
                "analysis": {
                    "version": "local-1.0",
                    "sample_rate": sr,
                    "counts": {
                        "sections": len(sections),
                        "bars": len(bars),
                        "beats": len(beats),
                        "tatums": len(tatums),
                        "segments": len(segments),
                    },
                    "sections": [s.as_dict() for s in sections],
                    "bars": [b.as_dict() for b in bars],
                    "beats": [b.as_dict() for b in beats],
                    "tatums": [t.as_dict() for t in tatums],
                    "segments": segments,
                },
            },
        }
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as sink:
        json.dump(profile, sink, indent=2)
    return profile


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an Infinite Jukebox compatible analysis profile."
    )
    parser.add_argument("--audio", required=True, type=Path, help="Path to the audio file.")
    parser.add_argument("--track-id", required=True, help="Identifier used in go.html?trid=...")
    parser.add_argument("--title", default=None, help="Human friendly track title.")
    parser.add_argument("--artist", default="(unknown artist)", help="Artist name.")
    parser.add_argument(
        "--audio-url",
        default=None,
        help="Public or relative URL the web app can stream. Defaults to the audio path basename.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Destination JSON path. Defaults to data/<track_id>.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audio_path = args.audio.resolve()
    if not audio_path.exists():
        raise SystemExit(f"Audio file not found: {audio_path}")

    track_id = args.track_id
    title = args.title or audio_path.stem
    audio_url = args.audio_url or audio_path.name
    output_path = args.output or Path("data") / f"{track_id}.json"

    profile = build_profile(
        audio_path=audio_path,
        track_id=track_id,
        title=title,
        artist=args.artist,
        audio_url=audio_url,
        output_path=output_path,
    )

    print(f"Wrote analysis to {output_path}")
    print(
        f"Track: {profile['response']['track']['title']} "
        f"({profile['response']['track']['audio_summary']['duration']:.2f}s)"
    )


if __name__ == "__main__":
    main()
