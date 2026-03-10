from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

class TierProgression(BaseModel):
    current_tier: int
    next_tier: int
    eligible_challenges: List[dict]  # Simplified for now
    total_tiers: int

class TierStatistics(BaseModel):
    total_tiers: int
    tier_statistics: dict

class ScaledRulesResponse(BaseModel):
    challenge_id: UUID
    base_multiplier: float
    base_rules: dict
    scaled_rules: dict