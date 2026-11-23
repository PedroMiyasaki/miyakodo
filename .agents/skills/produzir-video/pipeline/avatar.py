"""Avatar 2D do Pedro, na paleta Miyakodo, para o modo sem gravação.

O desenho usa assets/pedro-frame.jpg como referência de rosto: cabelo
escuro ondulado, sobrancelha fechada, barba curta e uma pinta.
Não é o mascote Carlos.
"""


def avatar_svg() -> str:
    return """
<svg id="av-svg" viewBox="0 0 200 230" width="100%" height="100%" aria-label="Avatar do Pedro">
  <ellipse cx="100" cy="214" rx="62" ry="10" fill="#280e03" opacity="0.12"/>
  <g id="av-rig">
    <path d="M62 176 C62 214 138 214 138 176 L128 168 L72 168 Z" fill="#280e03"/>
    <path d="M78 168 H122 V198 H78 Z" fill="#c9856a"/>
    <ellipse cx="100" cy="104" rx="84" ry="90" fill="#280e03"/>
    <ellipse cx="46" cy="118" rx="12" ry="16" fill="#f0c7b0" stroke="#280e03" stroke-width="3"/>
    <ellipse cx="154" cy="118" rx="12" ry="16" fill="#f0c7b0" stroke="#280e03" stroke-width="3"/>
    <ellipse cx="100" cy="112" rx="64" ry="72" fill="#f3d0bc" stroke="#280e03" stroke-width="4"/>
    <path d="M38 96 C48 28 78 18 100 34 C122 16 160 30 164 98 C150 46 124 28 100 48 C74 26 50 48 38 96 Z" fill="#280e03"/>
    <path d="M58 78 C70 58 86 66 92 84 C78 70 66 74 58 78 Z" fill="#280e03"/>
    <path d="M142 78 C130 58 114 66 108 84 C122 70 134 74 142 78 Z" fill="#280e03"/>
    <g id="av-brows">
      <path d="M62 92 Q78 80 96 90" fill="none" stroke="#280e03" stroke-width="7" stroke-linecap="round"/>
      <path d="M104 90 Q124 78 140 94" fill="none" stroke="#280e03" stroke-width="7" stroke-linecap="round"/>
    </g>
    <g id="av-eyes">
      <ellipse cx="78" cy="112" rx="13" ry="8" fill="#f6f4ee" stroke="#280e03" stroke-width="3"/>
      <ellipse cx="124" cy="112" rx="13" ry="8" fill="#f6f4ee" stroke="#280e03" stroke-width="3"/>
      <ellipse cx="78" cy="112" rx="5.5" ry="5.5" fill="#280e03"/>
      <ellipse cx="124" cy="112" rx="5.5" ry="5.5" fill="#280e03"/>
      <rect id="av-lid-l" x="64" y="102" width="28" height="16" rx="8" fill="#f3d0bc" opacity="0"/>
      <rect id="av-lid-r" x="110" y="102" width="28" height="16" rx="8" fill="#f3d0bc" opacity="0"/>
    </g>
    <path d="M100 118 C108 132 112 140 100 146 C90 140 92 130 100 118 Z" fill="#e0b09a"/>
    <path d="M64 146 C70 176 130 176 136 146 C124 164 78 164 64 146 Z" fill="#280e03" opacity="0.82"/>
    <circle cx="58" cy="128" r="2.4" fill="#6a3b2a"/>
    <g id="av-mouth">
      <path id="av-mouth-closed" d="M82 156 Q100 166 118 156" fill="none" stroke="#280e03" stroke-width="4" stroke-linecap="round"/>
      <ellipse id="av-mouth-open" cx="100" cy="160" rx="13" ry="7" fill="#280e03"/>
    </g>
  </g>
</svg>
""".strip()


def avatar_motion(duration: float, emphasis_times: list[float], moves: list[dict]) -> dict:
    blinks = [t for t in (0.35, 2.6, 4.9, 7.4, 10.2, 12.8, 15.1, 17.6) if t < duration - 0.2]
    return {
        "blinks": blinks,
        "lifts": [round(t, 4) for t in emphasis_times if 0 <= t < duration],
        "moves": moves,
        "bob_repeats": max(1, int(duration / 0.9)),
    }
