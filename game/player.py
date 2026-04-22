class Player:
    """Track player state and gameplay tuning values."""

    BASE_RECOVERY_PER_SECOND = 0.006
    CARDIO_RECOVERY_BONUS_PER_LEVEL = 0.015
    BASE_CLICK_HEART_GAIN = 0.05
    INSULATION_REDUCTION_PER_LEVEL = 0.006
    MIN_CLICK_HEART_GAIN = 0.01
    BASE_MONEY_PER_CLICK = 1

    def __init__(self) -> None:
        self.health_level = 0.0
        self.dead = False
        self.shop_open = False
        self.money = 100000000
        self.upgrade_levels = {"insulation": 0, "cardio": 0, "coupon": 0}

    def get_recovery_per_second(self) -> float:
        """Return passive recovery speed from base + cardio levels."""
        return self.BASE_RECOVERY_PER_SECOND + self.upgrade_levels["cardio"] * self.CARDIO_RECOVERY_BONUS_PER_LEVEL

    def update_passive_recovery(self, dt: float) -> None:
        """Recover heart attack level while alive."""
        if self.dead:
            return
        self.health_level = max(0.0, self.health_level - self.get_recovery_per_second() * dt)

    def get_click_heart_gain(self) -> float:
        """Return heart attack gain from a can click after insulation."""
        reduced_gain = self.BASE_CLICK_HEART_GAIN - self.upgrade_levels["insulation"] * self.INSULATION_REDUCTION_PER_LEVEL
        return max(self.MIN_CLICK_HEART_GAIN, reduced_gain)

    def get_money_per_click(self) -> int:
        """Return money earned on can click including coupon levels."""
        return self.BASE_MONEY_PER_CLICK + self.upgrade_levels["coupon"]

    def apply_can_click(self) -> bool:
        """Apply click rewards/damage and return True if this click caused death."""
        if self.dead:
            return False

        self.money += self.get_money_per_click()
        self.health_level = min(1.0, self.health_level + self.get_click_heart_gain())

        if self.health_level >= 1.0:
            self.mark_dead()
            return True
        return False

    def reset_progress_on_death(self) -> None:
        """Reset progression that should be lost on death."""
        self.money = 0
        self.upgrade_levels = {"insulation": 0, "cardio": 0, "coupon": 0}

    def mark_dead(self) -> None:
        """Set dead state and clear progress for the run."""
        self.dead = True
        self.shop_open = False
        self.reset_progress_on_death()

    def restart_after_death(self) -> None:
        """Return to alive state for a fresh run."""
        self.health_level = 0.0
        self.dead = False
        self.shop_open = False
