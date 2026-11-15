"""Generates cosmic.svg, the Cosmic app icon: a spiral galaxy whose outer arm forms the letter C.

Original work for the Cosmic fork; no reference artwork was used. Run: python -I make_icon.py
"""

import math
import random
from pathlib import Path

SIZE = 512
CX = CY = 256.0


def fmt(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def polygon(outer, inner) -> str:
    pts = outer + list(reversed(inner))
    head = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    return head + "".join(f"L{fmt(x)} {fmt(y)}" for x, y in pts[1:]) + "Z"


def tapered_band(radius_at, angle_at, width_at, steps=160) -> str:
    """A band along a curve: angle and radius per parameter s in [0, 1], half-width per s."""
    outer, inner = [], []
    for i in range(steps + 1):
        s = i / steps
        a, r, w = angle_at(s), radius_at(s), width_at(s)
        outer.append((CX + (r + w) * math.cos(a), CY + (r + w) * math.sin(a)))
        inner.append((CX + (r - w) * math.cos(a), CY + (r - w) * math.sin(a)))
    return polygon(outer, inner)


def c_arm() -> str:
    # The C: from the upper-right (-40 deg) anticlockwise on screen to the lower-right (-320 deg).
    start, end = math.radians(-40), math.radians(-320)
    return tapered_band(
        radius_at=lambda s: 150 + 6 * math.sin(math.pi * s),
        angle_at=lambda s: start + (end - start) * s,
        width_at=lambda s: 5 + 31 * math.sin(math.pi * s) ** 0.7,
    )


def dust_arm() -> str:
    # A faint outer arm hugging the left of the C.
    start, end = math.radians(-115), math.radians(-245)
    return tapered_band(
        radius_at=lambda s: 196 + 4 * s,
        angle_at=lambda s: start + (end - start) * s,
        width_at=lambda s: 1 + 7 * math.sin(math.pi * s),
    )


def inner_arm(phase: float) -> str:
    sweep = math.radians(250)
    return tapered_band(
        radius_at=lambda s: 14 + 78 * s,
        angle_at=lambda s: phase - sweep * s,
        width_at=lambda s: 11 * (1 - s) ** 0.8 + 1.2,
        steps=90,
    )


def stars() -> str:
    rng = random.Random(20261115)
    out = []
    while len(out) < 34:
        x, y = rng.uniform(30, 482), rng.uniform(30, 482)
        d = math.hypot(x - CX, y - CY)
        if 100 < d < 200 and not (x > CX + 60 and abs(y - CY) < 90):
            continue  # keep the C band clean; the opening may hold stars
        if d < 105:
            continue
        r = rng.choice([0.9, 1.1, 1.4, 1.8, 2.4])
        o = rng.uniform(0.45, 1.0)
        out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="#fff" opacity="{o:.2f}"/>')
    return "\n    ".join(out)


def svg() -> str:
    c = c_arm()
    arms = [inner_arm(math.radians(p)) for p in (0, 180)]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" width="{SIZE}" height="{SIZE}">
  <title>Cosmic</title>
  <defs>
    <clipPath id="tile"><rect width="512" height="512" rx="112"/></clipPath>
    <radialGradient id="space" cx="0.42" cy="0.45" r="0.75">
      <stop offset="0" stop-color="#2a1660"/>
      <stop offset="0.55" stop-color="#140b38"/>
      <stop offset="1" stop-color="#070419"/>
    </radialGradient>
    <linearGradient id="arm" x1="0" y1="80" x2="0" y2="432" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#5ee7ff"/>
      <stop offset="0.5" stop-color="#9d6bff"/>
      <stop offset="1" stop-color="#ff4fc8"/>
    </linearGradient>
    <radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#fffbea"/>
      <stop offset="0.35" stop-color="#ffd98a" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#ff9adf" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <g clip-path="url(#tile)">
    <rect width="512" height="512" fill="url(#space)"/>
    {stars()}
    <path d="{dust_arm()}" fill="#b9a4ff" opacity="0.35" filter="url(#soft)"/>
    <path d="{c}" fill="url(#arm)" opacity="0.75" filter="url(#glow)"/>
    <path d="{c}" fill="url(#arm)"/>
    <g fill="#e8dcff" opacity="0.85">
      <path d="{arms[0]}"/>
      <path d="{arms[1]}"/>
    </g>
    <circle cx="256" cy="256" r="58" fill="url(#core)"/>
    <circle cx="256" cy="256" r="11" fill="#fffdf5"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    Path(__file__).with_name("cosmic.svg").write_text(svg(), encoding="utf-8")
