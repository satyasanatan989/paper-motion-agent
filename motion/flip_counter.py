"""
Mechanical Antique Split-Flap Flip Counter Component.
Emulates tactile retro train station and vintage scoreboards in papercraft aesthetic.
"""

def generate_flip_counter_html(
    title: str,
    digits: list = ["1", "0", "0"],
    suffix: str = "K+",
    subtitle: str = "CASUALTIES IN BATTLE"
) -> str:
    """Generates the HTML card for an antique mechanical flip counter."""
    tiles = "".join(f'<div class="flip-tile">{d}</div>' for d in digits)
    return f"""
    <div class="ancient-metric-card" style="width: 720px; margin-top: 20px;">
      <div class="ancient-metric-title">{title}</div>
      <div class="flip-row">
        {tiles}
        <div style="font-family: 'Cinzel', serif; font-size: 54px; font-weight: 700; color: #9B111E;">{suffix}</div>
      </div>
      <div class="ancient-metric-sub">{subtitle}</div>
    </div>
    """
