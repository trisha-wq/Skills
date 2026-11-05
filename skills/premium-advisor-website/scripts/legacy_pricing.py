"""Apply the approved Legacy Stories guidebook price without editing baselines."""
POLICY = 'legacy-guidebook-price-v1'


def apply_legacy_pricing(code):
    return code.replace('Leverage Your Guidebook For $97', 'Leverage Your Guidebook For $59')
