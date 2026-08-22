#!/usr/bin/env python3
"""Materialize an admitted unit from the frozen Lega v1.01 authority.

The constants below are deliberately exact.  Adding a unit requires first
computing its canonical record and asset identities from the already frozen
coordinator snapshot, then reviewing those identities before admission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
SNAPSHOT = LANE / "authority" / "coordinator-snapshot-20260821" / "snapshot"
RECORDS = SNAPSHOT / "records.canonical.json"
EPUB = LANE / "authority" / "archives" / "lega-v1.01.epub"

UNIT_SPECS = {
    "O005-LEGA-V101-CH01": {
        "record_id": 25,
        "modified_gmt": "2026-03-27T02:08:36",
        "record_bytes": 37918,
        "record_sha256": "0286cb444c7f2f4a2db83865f948d3d3dc00147e2280fa665a1abc68ad804826",
        "assets": [
            {
                "path": "assets/modeling-cycle-source.png",
                "epub_member": "EPUB/assets/Modeling_Cycle-1024x508.png",
                "bytes": 75844,
                "sha256": "29c1df3263dd7fe76769803e54c23ddcd198198e86edbfd7e4d6f0c618f708e3",
            }
        ],
    },
    "O005-LEGA-V101-CH02": {
        "record_id": 27,
        "modified_gmt": "2026-03-27T02:10:41",
        "record_bytes": 39193,
        "record_sha256": "428a143edeec7843d3f4a2e2f02e5aa50fcde2cff366ca976988ecfa4191e69b",
        "assets": [
            {
                "path": "assets/the-wave-source.png",
                "epub_member": "EPUB/assets/The_Wave.png",
                "bytes": 80026,
                "sha256": "9abe8e17abd593811c14a1d6ea72b3ff727682ba58d000a87ece4056332769b6",
            }
        ],
    },
    "O005-LEGA-V101-PT02": {
        "record_id": 28,
        "modified_gmt": "2024-06-29T02:57:03",
        "record_bytes": 2296,
        "record_sha256": "03ead95b0ebcfb470c92bb7e48a85ce45d7639ec0aafb00f981eaf90ffd3f1e9",
        "assets": [],
    },
    "O005-LEGA-V101-CH03": {
        "record_id": 38,
        "modified_gmt": "2026-03-27T02:14:38",
        "record_bytes": 128063,
        "record_sha256": "240a00176ea39c067c36393facf35308bdbee11925dbc293bad2ce33ca9c339c",
        "assets": [
            {
                "path": "assets/nonlinear-pendulum-source.png",
                "epub_member": "EPUB/assets/Fig_NLP-1-300x268.png",
                "bytes": 11678,
                "sha256": "10bd1a917faadd58ab70645455e2ce9f092bc3f9833e50aee83ac2e89be9783a",
            },
            {
                "path": "assets/phase-portrait-1-source.png",
                "epub_member": "EPUB/assets/PP_NLP-1024x806.png",
                "bytes": 247117,
                "sha256": "e9483fbe666497aab3695456eecf5ce4ffce0440db2605c37c3a257d0b2e70de",
            },
            {
                "path": "assets/phase-portrait-2-source.png",
                "epub_member": "EPUB/assets/PP2_NLP-1024x763.png",
                "bytes": 297538,
                "sha256": "5c42026faf31e340f38829471db0a9f22a76bb467fff2508f1490f62bc2949f0",
            },
            {
                "path": "assets/phase-portrait-construction-source.png",
                "epub_member": "EPUB/assets/PP2b_NLP-1024x993.png",
                "bytes": 258152,
                "sha256": "4df4090e177969f1c911ee9f1edb6ebaa734bf724e69def16ef94f9b929e8479",
            },
            {
                "path": "assets/phase-portrait-3-source.png",
                "epub_member": "EPUB/assets/PP3_NLP-1024x765.png",
                "bytes": 379047,
                "sha256": "6392b654687eadb3d547d99db7069694f0cdb91671ace0082fd164817305e6d5",
            },
            {
                "path": "assets/potential-1-source.png",
                "epub_member": "EPUB/assets/Mech_pot1-1-300x218.png",
                "bytes": 10087,
                "sha256": "d846bc553c4c59aa388697a521a9f0a935a869a96f6f8ef8e2bbe7b58e0a2388",
            },
            {
                "path": "assets/potential-2-source.png",
                "epub_member": "EPUB/assets/Mech_pot2-1-300x166.png",
                "bytes": 9208,
                "sha256": "0983ed663132286f874444b322707167ef402bf32a270a9bd24802b76539b74c",
            },
            {
                "path": "assets/potential-3-source.png",
                "epub_member": "EPUB/assets/Mech_pot3-1-300x271.png",
                "bytes": 13587,
                "sha256": "4aa716e47c4efdf46750e0fa4e1c3883f75ab63abdda7705685b986c1244070e",
            },
            {
                "path": "assets/potential-4-source.png",
                "epub_member": "EPUB/assets/Mech_pot4-1-300x160.png",
                "bytes": 9734,
                "sha256": "ed6153fffcb4ac0dca7b2372c062277ec67b2ffc5f7c17a0bb238c0febb7397d",
            },
        ],
    },
    "O005-LEGA-V101-CH04": {
        "record_id": 39,
        "modified_gmt": "2026-03-19T21:51:57",
        "record_bytes": 71697,
        "record_sha256": "a1a31a51f76e7b4f74b8ed302b112acaad6bd87b0b9b5cb134676c5205b03e55",
        "assets": [
            {
                "path": "assets/stone-collision-source.png",
                "epub_member": "EPUB/assets/Stone_coll-300x248.png",
                "bytes": 20409,
                "sha256": "89bd0040e8b3667dab192d6209c1933d25e85d8950ea14e014d3909244551c80",
            },
            {
                "path": "assets/stone-potential-source.png",
                "epub_member": "EPUB/assets/Stone_Pot-300x300.png",
                "bytes": 9016,
                "sha256": "e38c1e539565bfab8a128d8269d36b4983d9710b8affe5cc94a29060bed04dc6",
            },
        ],
    },
    "O005-LEGA-V101-PT03": {
        "record_id": 40,
        "modified_gmt": "2024-06-29T02:57:20",
        "record_bytes": 5758,
        "record_sha256": "e0c7435af2c60d11f80eef9924934c335c93100cd86de57170820560797f9576",
        "assets": [],
    },
    "O005-LEGA-V101-CH05": {
        "record_id": 48,
        "modified_gmt": "2026-03-27T02:27:32",
        "record_bytes": 119420,
        "record_sha256": "7f276a994f78af2af02d5bdd39b9566a50f5e3b09b25351c70cdff50736c66be",
        "assets": [
            {
                "path": "assets/redhawk-count-source.png",
                "epub_member": "EPUB/assets/Redhawk_US_1-105-300x213.png",
                "bytes": 10733,
                "sha256": "6026cbadc87a030ce119b009551d8a9428b9af51083bd708832ef7dbcea676cd",
            },
            {
                "path": "assets/redhawk-rate-source.png",
                "epub_member": "EPUB/assets/Redhawk_US_1-105_rate-300x213.png",
                "bytes": 17230,
                "sha256": "5a181a42c3cf709bc906ac372d2d173c6afd57ed34e426a92e22a718a87cc97e",
            },
            {
                "path": "assets/redhawk-return-source.png",
                "epub_member": "EPUB/assets/Redhawk_US_1-105_1stR-300x213.png",
                "bytes": 14910,
                "sha256": "3b348b9c541b763ac802525038fa5f5dc7c5d8580c3b319479bbabc9732b7d5e",
            },
            {
                "path": "assets/cobweb-iterations-source.png",
                "epub_member": "EPUB/assets/Iterations-287x300.png",
                "bytes": 16413,
                "sha256": "97ea2323b18b6bcae1ef4ab0b89bf5e589654f8dc7ff757dbb2c587e15bf30dc",
            },
            {
                "path": "assets/logistic-bifurcation-source.png",
                "epub_member": "EPUB/assets/Logistic1a-300x241.png",
                "bytes": 25987,
                "sha256": "4768b2076566ba00ee818166b9053836cb0166eea81545eaf5962e92aaf0dc7b",
            },
            {
                "path": "assets/logistic-bifurcation-zoom-source.png",
                "epub_member": "EPUB/assets/Logistic2a-300x239.png",
                "bytes": 58787,
                "sha256": "13fb09c5410c24f15085e872ecc9e4967a8c05b41f3f7e5104141ce6868431d3",
            },
            {
                "path": "assets/one-dimensional-stability-source.png",
                "epub_member": "EPUB/assets/Gen_stable-300x220.png",
                "bytes": 13876,
                "sha256": "8f7964291a6dc3b3bcc5a9c26ceacaae491f9478c29a2705eec672f7e3ce2c3e",
            },
        ],
    },
    "O005-LEGA-V101-CH06": {
        "record_id": 53,
        "modified_gmt": "2026-03-27T02:30:16",
        "record_bytes": 63377,
        "record_sha256": "cdcc1c12fc5c0245ffbb94c6cfdc706570f50540bb6719d78e1391f282b114de",
        "assets": [
            {
                "path": "assets/predator-prey-damped-source.png",
                "epub_member": "EPUB/assets/CLV_PP1-1024x784.png",
                "bytes": 261588,
                "sha256": "5f714f9670a8a634d3f6e41571e4be8423b53a7991f4ce3ea159c54c439a72df",
            },
            {
                "path": "assets/predator-prey-closed-source.png",
                "epub_member": "EPUB/assets/CLV_PP2-1024x777.png",
                "bytes": 291998,
                "sha256": "12c7e47611611ad9bdbf822d0ecac1abd5a54b3302aeff9cd037bd9a0d42f6c3",
            },
            {
                "path": "assets/competition-coexistence-source.png",
                "epub_member": "EPUB/assets/CCS_PP1-1024x769.png",
                "bytes": 238694,
                "sha256": "4eea679f5d3449746b333e429c8be8c2340348f130a705fe2e05597b8c76f765",
            },
            {
                "path": "assets/competition-exclusion-source.png",
                "epub_member": "EPUB/assets/CCS_PP2-1024x770.png",
                "bytes": 244184,
                "sha256": "2675913333eaecef42fbec40ec78f24a3ea555217ade399bb159e2c5c5739c53",
            },
        ],
    },
    "O005-LEGA-V101-CH07": {
        "record_id": 57,
        "modified_gmt": "2026-03-19T20:23:36",
        "record_bytes": 48627,
        "record_sha256": "dcf828ca5ce0c58ced8eb5203dfd1b5a949bd6af3b9c000017a6dd133bb58d2f",
        "assets": [
            {
                "path": "assets/sir-phase-source.png",
                "epub_member": "EPUB/assets/CSIR_PP-1024x760.png",
                "bytes": 269240,
                "sha256": "6fb4ddda16dc32455db64ec8211e561260118f5a2994aa88b503a179d851c08b",
            },
            {
                "path": "assets/endemic-phase-1-source.png",
                "epub_member": "EPUB/assets/CESIR_PP1-1024x759.png",
                "bytes": 307592,
                "sha256": "20862c9a7ae87d9d6cc5d3c00a5ea855ee7c7a786cd832e40b6aebf8acbb63af",
            },
            {
                "path": "assets/endemic-phase-2-source.png",
                "epub_member": "EPUB/assets/CESIR_PP2-1024x759.png",
                "bytes": 288503,
                "sha256": "e1b4360292dceb3d403cc54cc1b76cf1b45d80a9331acdad6a2f460d77eb9058",
            },
        ],
    },
    "O005-LEGA-V101-PT04": {
        "record_id": 58,
        "modified_gmt": "2026-03-17T22:14:18",
        "record_bytes": 6589,
        "record_sha256": "75d370fb729c39ba436eb1a91f5876291ef4c0487235b968d8a0a0002481f232",
        "assets": [],
    },
    "O005-LEGA-V101-CH08": {
        "record_id": 62,
        "modified_gmt": "2026-03-24T21:29:34",
        "record_bytes": 60372,
        "record_sha256": "1c9f5f1ec75756f23720a3ef5d278302de0957347a59dde6f8021d3a970d7656",
        "assets": [
            {
                "path": "assets/brusselator-phase-source.png",
                "epub_member": "EPUB/assets/BR_PP-1024x685.png",
                "bytes": 169478,
                "sha256": "957ba0e2af31820eb0224add944508da2a1ab42135ea43450854880e38d8c9f4",
            },
            {
                "path": "assets/brusselator-time-series-source.png",
                "epub_member": "EPUB/assets/BR_PPt-1024x876.png",
                "bytes": 129573,
                "sha256": "0244fe5655d13b710978c4ee42ed84556d4cbc5124d3a60fe7c3d4ca9e2c5e7c",
            },
            {
                "path": "assets/oregonator-phase-source.png",
                "epub_member": "EPUB/assets/COR2_PP-1024x671.png",
                "bytes": 140277,
                "sha256": "052645103df598f8feac0be17dfbf64f6525bf6d44f798f9bccfc10c269a548b",
            },
        ],
    },
    "O005-LEGA-V101-CH09": {
        "record_id": 196,
        "modified_gmt": "2026-03-19T20:10:36",
        "record_bytes": 65160,
        "record_sha256": "e53b35acf85334d2df48124211843b08b7ca1e9e9ca8c91465f215dfbb219c2a",
        "assets": [
            {
                "path": "assets/diffusion-random-walk-source.png",
                "epub_member": "EPUB/assets/Diffusion-300x261.png",
                "bytes": 37521,
                "sha256": "4659e7a659e47069360aedfe1f6a6511516e8c99d96ccc9421d5edc34e33648e",
            },
            {
                "path": "assets/fisher-traveling-wave-phase-1-source.png",
                "epub_member": "EPUB/assets/TW_PP1.png",
                "bytes": 126169,
                "sha256": "a3080ea906a114bc538bb27ca30c22a40953ee77eeda75537a7f120e44e45366",
            },
            {
                "path": "assets/fisher-traveling-wave-phase-2-source.png",
                "epub_member": "EPUB/assets/TW_PP2.png",
                "bytes": 115933,
                "sha256": "17bb5d8b4b0f3f0b34e68a7276290020c7b34f3592df1ca307769bdea591bbcb",
            },
        ],
    },
    "O005-LEGA-V101-CH10": {
        "record_id": 194,
        "modified_gmt": "2026-03-19T20:11:05",
        "record_bytes": 49768,
        "record_sha256": "fbabaa5ed87f7b1e1a2a851555b2e0b7b37d3398a6450b67ffb73efcdb614f06",
        "assets": [
            {
                "path": "assets/pattern-collage-source.png",
                "epub_member": "EPUB/assets/Collage-200x300.png",
                "bytes": 120120,
                "sha256": "ed55c4ad09e5b4f1746dabf66aa87509538bcf76bcbc442650a4925ea47006ba",
            },
            {
                "path": "assets/swift-hohenberg-patterns-source.png",
                "epub_member": "EPUB/assets/SH1-300x141.png",
                "bytes": 59364,
                "sha256": "f92c04b397d388f84a31737b72dfbfdf89a14df4210e7cbf3c41fcf2f8b8958a",
            },
            {
                "path": "assets/pattern-growth-rates-source.png",
                "epub_member": "EPUB/assets/Pat_growth-1-300x142.png",
                "bytes": 8974,
                "sha256": "a49ff56eba92cc8f74400b6925443a63a4bcdbe95afd477c51f386f038abf32c",
            },
        ],
    },
    "O005-LEGA-V101-PT05": {
        "record_id": 409,
        "modified_gmt": "2024-07-04T01:20:04",
        "record_bytes": 1664,
        "record_sha256": "ccc3b6a575bf84e7ae94d3b3f5320e59279b088bede008e0e99bb423821a05c8",
        "assets": [],
    },
    "O005-LEGA-V101-CH11": {
        "record_id": 410,
        "modified_gmt": "2026-03-19T20:11:37",
        "record_bytes": 29468,
        "record_sha256": "762b7d0825a0669bc603f74b7d9b4c183a5e862dc594d3f9d467788397be31ce",
        "assets": [],
    },
    "O005-LEGA-V101-CH12": {
        "record_id": 413,
        "modified_gmt": "2026-03-19T19:53:52",
        "record_bytes": 31922,
        "record_sha256": "fa1364a307b033035bce94975db0667edf3b8d208e73b4e07882b090cafab377",
        "assets": [],
    },
}


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_checked(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"refusing to overwrite different bytes: {path}")
    path.write_bytes(data)


def checked_bytes(data: bytes, *, size: int, digest: str, label: str) -> bytes:
    if len(data) != size or sha256(data) != digest:
        raise RuntimeError(f"{label} does not match admitted authority")
    return data


def prepare(unit_id: str) -> dict:
    spec = UNIT_SPECS[unit_id]
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    matches = [record for record in records if record.get("id") == spec["record_id"]]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one record {spec['record_id']}, found {len(matches)}"
        )
    record = matches[0]
    record_bytes = checked_bytes(
        canonical_json(record),
        size=spec["record_bytes"],
        digest=spec["record_sha256"],
        label=f"canonical {unit_id} record",
    )
    if record.get("modified_gmt") != spec["modified_gmt"]:
        raise RuntimeError(f"unexpected {unit_id} modification instant")
    content = record.get("content") or {}
    raw = content.get("raw")
    rendered = content.get("rendered")
    if not isinstance(raw, str) or not isinstance(rendered, str):
        raise RuntimeError(f"{unit_id} lacks raw/rendered semantic source")
    raw_bytes = raw.encode("utf-8")
    rendered_bytes = rendered.encode("utf-8")

    unit = LANE / "authority" / "units" / unit_id
    write_checked(unit / "source-record.canonical.json", record_bytes)
    write_checked(unit / "content.raw.en.html", raw_bytes)
    write_checked(unit / "content.rendered.en.html", rendered_bytes)

    asset_rows = []
    with zipfile.ZipFile(EPUB) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"EPUB CRC failure at {bad}")
        for asset in spec["assets"]:
            data = checked_bytes(
                archive.read(asset["epub_member"]),
                size=asset["bytes"],
                digest=asset["sha256"],
                label=f"{unit_id} asset {asset['epub_member']}",
            )
            write_checked(unit / asset["path"], data)
            asset_rows.append(
                {
                    "path": asset["path"],
                    "bytes": len(data),
                    "sha256": sha256(data),
                    "epub_member": asset["epub_member"],
                }
            )

    manifest = {
        "schema": "o005-unit-authority-v1",
        "unit_id": unit_id,
        "source_record_id": spec["record_id"],
        "source_modified_gmt": spec["modified_gmt"] + "Z",
        "record": {
            "path": "source-record.canonical.json",
            "bytes": len(record_bytes),
            "sha256": sha256(record_bytes),
        },
        "content_raw": {
            "path": "content.raw.en.html",
            "bytes": len(raw_bytes),
            "sha256": sha256(raw_bytes),
        },
        "content_rendered": {
            "path": "content.rendered.en.html",
            "bytes": len(rendered_bytes),
            "sha256": sha256(rendered_bytes),
        },
        "assets": asset_rows,
    }
    payload = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    write_checked(unit / "AUTHORITY_MANIFEST.json", payload)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("unit_id", choices=sorted(UNIT_SPECS))
    args = parser.parse_args()
    print(json.dumps(prepare(args.unit_id), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
