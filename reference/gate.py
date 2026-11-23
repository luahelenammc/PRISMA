"""Deterministic precondition gate. Declarations require operator verification."""
from dataclasses import dataclass, field

MODES = {'lens','mask','table','mirror','counterproof','world','reception'}
CLASSES = {'public','fictional','archetype','functional','mirror','private'}

@dataclass(frozen=True)
class Request:
    mode: str
    profile_class: str = 'functional'
    active: bool = True
    simple: bool = False
    sources: tuple = ()
    explicit_mask: bool = False
    consent: bool = False
    high_risk: bool = False
    identifiable: bool = False
    educational: bool = False
    canon_conflict: bool = False
    canon_ratified: bool = False
    domain: str = 'generic'
    independent_agents_verified: bool = False
    write_authorized: bool = False
    readback_verified: bool = False
    local_authority_allows: bool = True
    disagreements: tuple = ()
    internet: bool = True
    moon_source: bool = True
    proposed: bool = True

@dataclass(frozen=True)
class Decision:
    route: str
    label: str
    persistence: str = 'READ_ONLY'
    independence: str = 'not_verified'
    disagreements: tuple = ()
    governance: str = 'local_source'
    candidate: bool = True
    reasons: tuple = ()


def evaluate(r: Request) -> Decision:
    """Check declared routing constraints; never performs mutations or verifies truth."""
    def out(route, label, *reasons, persistence='READ_ONLY', candidate=True):
        return Decision(route, label, persistence,
                        'verified_by_operator' if r.independent_agents_verified else 'not_verified',
                        r.disagreements, 'local_source', candidate, reasons)
    if not r.active or r.simple:
        return out('direct', 'unverified', 'no_material_simulation_need')
    if r.mode not in MODES or r.profile_class not in CLASSES:
        return out('blocked', 'insufficient_basis', 'unknown_mode_or_class')
    if not r.local_authority_allows:
        return out('blocked', 'insufficient_basis', 'local_authority_denies')
    if r.high_risk:
        if r.identifiable or r.profile_class not in {'functional','archetype'} or not r.educational:
            return out('blocked', 'insufficient_basis', 'high_risk_privacy_or_mandate')
        return out('synthetic_educational', 'hypothesis', 'not_evidence_or_record')
    if r.profile_class == 'private':
        return out('functional_fallback', 'hypothesis', 'private_identity_not_simulated')
    if r.mode == 'mirror' or r.profile_class == 'mirror':
        if r.mode != 'mirror' or r.profile_class != 'mirror' or not r.consent or not r.sources:
            return out('blocked', 'insufficient_basis', 'mirror_requires_consent_and_source')
    if r.mode == 'mask' and not r.explicit_mask:
        return out('blocked', 'insufficient_basis', 'explicit_fiction_request_required')
    if r.profile_class == 'public' and r.mode != 'mask' and not r.sources:
        return out('functional_fallback', 'insufficient_basis', 'named_public_lens_requires_source')
    if r.profile_class == 'fictional' and not r.sources:
        return out('blocked', 'insufficient_basis', 'canon_or_explicit_synthetic_source_required')
    if r.canon_conflict and not r.canon_ratified:
        return out('candidate_only', 'labeled_fiction', 'canon_conflict_requires_ratification')
    label = {'mask':'labeled_fiction','world':'labeled_fiction','lens':'supported_interpretation',
             'mirror':'hypothesis','table':'hypothesis','counterproof':'hypothesis','reception':'hypothesis'}[r.mode]
    if r.mode == 'lens' and not r.sources:
        label = 'insufficient_basis'
    # Explicitly no write action; the receipt is only a representation of operator-declared state.
    persistence = 'READ_ONLY'
    if r.write_authorized:
        persistence = 'readback_declared' if r.readback_verified else 'pending_unverified'
    return out(r.mode, label, 'source_and_output_review_required', persistence=persistence)
