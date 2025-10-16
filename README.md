# The Autocanonizer (Local Edition)

[The Autocanonizer](http://static.echonest.com/autocanonizer/index.html "") is a web app that
turns any song into a canon by playing the original track against a time-offset copy of itself.

The original implementation relied on the now-defunct Echo Nest analysis service. This fork adds
a local analysis pipeline so you can generate the JSON profile the web app expects for any audio
file you provide.

## Project layout

- `templates/visualizer.html` - modern visualization/player page (tries `data/<trid>.json` before hitting
the legacy Echo Nest CDN).
- `analysis/analyze_track.py` - Python script that generates a compatible analysis profile.
- `analysis/ARCHITECTURE.md` - notes on the feature-extraction pipeline.
- `analysis/requirements.txt` - Python dependencies for the analyser.
- `data/` - default output directory for generated JSON files.

## Generate an analysis profile

1. **Install dependencies**
   ```bash
   python -m pip install --user -r analysis/requirements.txt
   ```
2. **Run the analyser** (replace the arguments with your own metadata):
   ```bash
   python analysis/analyze_track.py \
     --audio "Juice WRLD - Junkie (Unreleased) (OG).mp3" \
     --track-id TRLOCALJUNKIE \
     --title "Juice WRLD - Junkie (OG)" \
     --artist "Juice WRLD" \
     --audio-url "Juice WRLD - Junkie (Unreleased) (OG).mp3"
   ```
   This writes `data/TRLOCALJUNKIE.json`, which mirrors the structure produced by the Echo Nest
   uploader (sections, bars, beats, tatums, segments, and summary metadata).

## Run the full web experience

1. Install the new dependencies (only once):
   ```bash
   python -m pip install --user -r analysis/requirements.txt
   ```
   > You'll also need `ffmpeg` on your PATH if you plan to pull tracks from YouTube.

2. Start the Flask server:
   ```bash
   python app.py
   ```
   This serves everything - the new landing page, generated media, and the modern visualizer modes.

3. Open `http://localhost:5000/` and you'll be greeted by the redesigned landing page (black base, oxblood red primary, salmon pink accents). From there you can:
   - Upload your own audio file, or
   - Paste a YouTube link (the server uses `yt-dlp` to download it temporarily).

4. Pick **Autocanonizer** or **Eternal Jukebox**:
   - Autocanonizer launches the dual-voice canon (`mode=canon`).
   - Eternal Jukebox keeps a single voice looping with intelligent jumps (`mode=jukebox`).

Every processed track is analysed via the local pipeline and stored under `data/<track_id>.json`; audio lives in `uploads/` so the browser can stream it back.

## How the local analysis works

`analysis/analyze_track.py` uses `librosa` to approximate the Echo Nest feature set:

- Beat/tempo tracking -> bars, beats, tatums (triplet subdivisions).
- Agglomerative segmentation over MFCC + chroma features -> coarse sections.
- Onset detection + per-frame features -> fine-grained segments with timbre, pitch class profile,
  loudness envelope, and confidence.
- Beat-synchronous context stacking + self-similarity search -> canon alignment diagnostics (recommended offsets, per-beat partner indices).
- Simple Krumhansl-Schmuckler key detection for `audio_summary` metadata.

See `analysis/ARCHITECTURE.md` for deeper implementation notes and extension ideas.
