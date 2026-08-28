# Timestamps

OpenTimestamps proofs for released archive files (doc 50 §6.3).

A proof commits the SHA-256 of *specific bytes* to the Bitcoin blockchain. It is
not a proof about a URL or a git tag — only about a file's exact content. Each
proof here is taken over **the file uploaded to Zenodo**, not the tarball GitHub
generates on demand: GitHub's generated archives are not guaranteed to be
byte-stable over time, whereas a published Zenodo file is immutable. Verification
is therefore reproducible by anyone: download the file from its Zenodo record,
hash it, and check it against the `.ots` proof.

Per doc 50 §6.3 the proof for release *N* is committed in release *N+1*, because
the proof cannot exist until the file it covers has been published.

| Proof | Covers | Zenodo record | SHA-256 |
|---|---|---|---|
| `slice-cooling-v1.3.tar.gz.ots` | `slice-cooling-v1.3.tar.gz` | [10.5281/zenodo.22134961](https://doi.org/10.5281/zenodo.22134961) | `0453af5e89ed350dde9e29560f98922f48bf6763ad53ac50584dad0989f72f4d` |

Verify with:

```bash
ots verify slice-cooling-v1.3.tar.gz.ots -f <the-file-from-zenodo>
```

---
Part of an open defensive-publication release: hardware CERN-OHL-P v2, text
CC-BY-4.0, scripts MIT. No patents sought or held.
