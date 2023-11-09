"""Progress bar utility."""

from dataclasses import dataclass


@dataclass
class Bar:
    """Knowing estimated computation time (can be any unitless arbitrary value),
    update a loading bar on each call given current remaining time.
    """

    total: int
    message: str = "Progress"
    advanced: int = 0

    def advance(self, step):
        """Print simple loading bar, just knowing remaining time estimate."""
        self.advanced = min(self.total, self.advanced + step)
        ratio = 100 * self.advanced / self.total
        progress = round(0.5 * ratio)
        display = "█" * progress + "-" * (50 - progress)
        print(f"{self.message:<10}: |{display}| {ratio:.1f}% Complete",
              end="\r")

    def complete(self):
        """Complete the progress bar."""
        self.advance(self.total - self.advanced)

    def __del__(self):
        """Re-prompt the bar one last time."""
        self.advance(0)
        print()
