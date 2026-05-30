"""
PACE — Helper Utilities
"""


def format_pace(sec_per_km: float) -> str:
    """Convert seconds-per-km to mm'ss\" string."""
    if sec_per_km <= 0:
        return "--'--\""
    total = int(sec_per_km)
    m, s = divmod(total, 60)
    return f"{m}'{s:02d}\""


def format_duration(seconds: int) -> str:
    """Convert seconds to h:mm:ss or mm:ss string."""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def calculate_pace(duration_seconds: int, distance_km: float) -> int:
    """Return pace in seconds per km (int)."""
    if distance_km <= 0:
        return 0
    return round(duration_seconds / distance_km)


def vo2_level(vo2: int) -> tuple[str, str]:
    """Return (level_label, description) for a VO2 max value."""
    if vo2 >= 60:
        return "Elite", "Top 5% of your age group"
    if vo2 >= 52:
        return "Superior", "Top 18% of your age group"
    if vo2 >= 44:
        return "Excellent", "Above average fitness"
    if vo2 >= 37:
        return "Good", "Average fitness"
    return "Fair", "Room for improvement"
