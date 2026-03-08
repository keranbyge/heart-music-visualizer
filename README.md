# Heart Animation with Lyrics

A beautiful rotating heart animation with synchronized lyrics, created using Python and Pygame.

## Features

- Rotating spiral heart mesh animation using parametric equations
- Synchronized lyrics display
- Glowing neon effect with transparent overlapping lines
- Background music playback (macOS)
- Smooth 60 FPS animation

## Requirements

- Python 3.x
- pygame

## Installation

```bash
pip install pygame
```

## Usage

1. Place your audio file as `song.mp3` in the project directory
2. Create a `lyrics.txt` file with timestamps and lyrics (see format below)
3. Run the program:

```bash
python heart_mesh_animation.py
```

## Lyrics Format

Create a `lyrics.txt` file with the following format:

```
0  First line of lyrics
3  Second line of lyrics
6  Third line of lyrics
```

Where the number is the timestamp in seconds when the lyric should appear.

## Controls

- Close the window or press Ctrl+C to stop the animation and music

## Heart Equation

The heart shape is generated using the parametric equations:
- x = 16 sin³(t)
- y = 13 cos(t) − 5 cos(2t) − 2 cos(3t) − cos(4t)
