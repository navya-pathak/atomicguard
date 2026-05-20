# Public Repo Checklist

Use this before pushing the showcase repo.

## Must Keep Public
- README with project goal, your role, and outcomes
- Runnable demo script and one sample input
- Architecture or flow documentation
- Dependency list and setup steps

## Must Keep Private
- Any patient-level or potentially identifying data
- Internal or employer-owned assets
- Cloud credentials, access tokens, policies
- Private model weights trained on restricted data
- Large raw experiment dumps and backup files

## Attribution and Ownership
- Add a license in the final public repo (for example Apache-2.0 or MIT).
- Add CITATION.cff if you want citation-style attribution.
- Use signed tags/releases if you want stronger provenance.

## Final Safety Checks
- Search for accidental secrets before pushing.
- Confirm no restricted files match your git status.
- Verify demo runs end to end from a clean clone.
