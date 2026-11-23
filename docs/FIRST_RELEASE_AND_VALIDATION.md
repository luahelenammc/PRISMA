# First release and validation

Status: 0.1.0-rc.1, public release candidate. Repository publication does not by itself establish a tagged GitHub release, installed skill, independent agents or empirical effectiveness. Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/build_packages.py
python scripts/build_packages.py --check
```

The 16 P-series tests are deterministic synthetic contract checks of the reference gate. They verify decision boundaries on supplied input, not actual model quality, source authenticity or independent judgment. Before publication: review documentation and code, inspect the output against each scenario, verify license/attribution, run tests and package checks on the destination, publish only public-safe artifacts, read back canonical URL and HEAD, check downstream links, and register actual release evidence. Do not publish private test fixtures. A verified ZIP supports offline use; it does not install a skill or run an autonomous service. Manual installation remains host-dependent.
