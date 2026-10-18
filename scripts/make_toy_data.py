#!/usr/bin/env python3
"""
make_toy_data.py - regenerate every toy dataset used in the course.

EVERYTHING HERE IS SYNTHETIC. No real person's or patient's data is used, and
no real outbreak is depicted. Place names are fictional.

The output is deterministic: the same seed gives byte-identical files, so the
committed files in data/ can always be reproduced and audited.

Needs only Python 3.9+ and numpy.

Usage
-----
    python scripts/make_toy_data.py                 # all datasets -> ./data
    python scripts/make_toy_data.py --only seq gwas # a subset
    python scripts/make_toy_data.py --seed 7 --out /tmp/other   # non-canonical data

Datasets: seq, gwas, prs, outbreak, linelist, linux
"""
from __future__ import annotations

import argparse
import csv
import gzip
import math
import shutil
from datetime import date, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SEED = 20261015

# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------
COMP_BASE = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N"}
_COMP_TABLE = str.maketrans("ACGTN", "TGCAN")


def revcomp(s: str) -> str:
    return s.translate(_COMP_TABLE)[::-1]


_BASES = "TCAG"
_AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON = {
    a + b + c: _AAS[16 * i + 4 * j + k]
    for i, a in enumerate(_BASES)
    for j, b in enumerate(_BASES)
    for k, c in enumerate(_BASES)
}

ADAPTER1 = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"  # Illumina TruSeq read 1 adapter
ADAPTER2 = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"  # Illumina TruSeq read 2 adapter


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_gz(path: Path, text: str) -> None:
    """Deterministic gzip (mtime=0, no embedded filename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as gz:
            gz.write(text.encode("utf-8"))


def write_tsv(path: Path, header: list[str], rows: list[list], sep: str = "\t") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=sep, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def wrap(seq: str, width: int = 60) -> str:
    return "\n".join(seq[i : i + width] for i in range(0, len(seq), width))


def erfc_p(z: np.ndarray) -> np.ndarray:
    """Two-sided normal p-value for z-scores, no scipy needed."""
    return np.array([math.erfc(abs(x) / math.sqrt(2.0)) for x in z])


# ==========================================================================
# 1. SEQ  - a 6 kb reference, two genes, three samples of paired-end reads
# ==========================================================================
def build_reference(rng, length=6000):
    probs = np.array([0.275, 0.225, 0.225, 0.275])
    seq = list("".join(rng.choice(list("ACGT"), size=length, p=probs)))
    genes = [
        dict(id="toyR1", start=1001, end=1900, strand="+", stop="TAA", product="hypothetical enzyme"),
        dict(id="toyR2", start=3501, end=4199, strand="-", stop="TGA", product="hypothetical transporter"),
    ]
    sense = sorted(c for c, aa in CODON.items() if aa != "*")
    for g in genes:
        n_codons = (g["end"] - g["start"] + 1) // 3
        codons = ["ATG"] + [sense[int(rng.integers(len(sense)))] for _ in range(n_codons - 2)] + [g["stop"]]
        cds = "".join(codons)
        genomic = cds if g["strand"] == "+" else revcomp(cds)
        seq[g["start"] - 1 : g["end"]] = list(genomic)
        g["cds"] = cds
    return "".join(seq), genes


def cds_coords(g):
    r = list(range(g["start"], g["end"] + 1))
    return r if g["strand"] == "+" else r[::-1]


def pick_snp(ref, g, kind, near_codon):
    coords, cds = cds_coords(g), g["cds"]
    n_codons = len(cds) // 3
    for d in range(0, 300):
        for ci in (near_codon + d, near_codon - d):
            if ci < 1 or ci >= n_codons - 1:
                continue
            codon = cds[3 * ci : 3 * ci + 3]
            order = [2, 0, 1] if kind == "synonymous" else [0, 1, 2]
            for p in order:
                for nb in "ACGT":
                    if nb == codon[p]:
                        continue
                    new = codon[:p] + nb + codon[p + 1 :]
                    a0, a1 = CODON[codon], CODON[new]
                    ok = (
                        (kind == "synonymous" and a0 == a1)
                        or (kind == "missense" and a0 != a1 and "*" not in (a0, a1))
                        or (kind == "nonsense" and a1 == "*" and a0 != "*")
                    )
                    if ok:
                        gpos = coords[3 * ci + p]
                        galt = nb if g["strand"] == "+" else COMP_BASE[nb]
                        return dict(
                            pos=gpos, ref=ref[gpos - 1], alt=galt, type="SNV", gene=g["id"],
                            consequence={"synonymous": "synonymous_variant", "missense": "missense_variant",
                                         "nonsense": "stop_gained"}[kind],
                            effect=f"p.{a0}{ci + 1}{a1}",
                            note=f"codon {ci + 1} {codon}>{new} ({g['strand']} strand gene)",
                        )
    raise RuntimeError("no SNP found")


def intergenic_snp(ref, pos, rng):
    r = ref[pos - 1]
    alt = str(rng.choice([b for b in "ACGT" if b != r]))
    return dict(pos=pos, ref=r, alt=alt, type="SNV", gene="", consequence="intergenic_variant", effect="", note="")


def make_deletion(ref, start0, k):
    i = start0
    while i > 0 and ref[i - 1] == ref[i + k - 1]:
        i -= 1
    return dict(pos=i, ref=ref[i - 1 : i + k], alt=ref[i - 1], type="DEL")


def make_insertion(ref, at0, s):
    i = at0
    while i > 0 and ref[i - 1] == s[-1]:
        s = s[-1] + s[:-1]
        i -= 1
    return dict(pos=i, ref=ref[i - 1], alt=ref[i - 1] + s, type="INS")


def apply_variants(ref, variants):
    bases, coords = list(ref), list(range(1, len(ref) + 1))
    for v in sorted(variants, key=lambda x: -x["pos"]):
        p = v["pos"]
        if v["type"] == "SNV":
            assert bases[p - 1] == v["ref"], v
            bases[p - 1] = v["alt"]
        elif v["type"] == "DEL":
            assert "".join(bases[p - 1 : p - 1 + len(v["ref"])]) == v["ref"], v
            del bases[p : p - 1 + len(v["ref"])]
            del coords[p : p - 1 + len(v["ref"])]
        elif v["type"] == "INS":
            assert bases[p - 1] == v["ref"], v
            ins = list(v["alt"][1:])
            bases[p:p] = ins
            coords[p:p] = [None] * len(ins)
    return "".join(bases)


def quals(rng, n, q0, slope, sd=2.0):
    q = q0 - slope * np.arange(n) + rng.normal(0, sd, n)
    return np.clip(np.round(q), 2, 41).astype(int)


def add_errors(seq, q, rng):
    e = 10.0 ** (-q / 10.0)
    hit = rng.random(len(seq)) < e
    s = list(seq)
    for i in np.nonzero(hit)[0]:
        if s[i] != "N":
            s[i] = str(rng.choice([b for b in "ACGT" if b != s[i]]))
    for i in np.nonzero(q <= 2)[0]:
        if rng.random() < 0.5:
            s[i] = "N"
    return "".join(s)


def simulate_pairs(genomes, weights, n_pairs, rng, sample, read_len=100, q0=37.0, slope1=0.05,
                   slope2=0.10, short_frac=0.05, contam_frac=0.03, dup_frac=0.0, barcode="ACGTAC"):
    fr1, fr2 = [], []
    made = []
    w = np.array(weights, dtype=float) / sum(weights)
    for n in range(n_pairs):
        if made and rng.random() < dup_frac:
            frag = made[int(rng.integers(len(made)))]
        else:
            if rng.random() < contam_frac:
                L = int(max(read_len + 10, rng.normal(300, 30)))
                frag = "".join(rng.choice(list("ACGT"), size=L))
            else:
                g = genomes[int(rng.choice(len(genomes), p=w))]
                if rng.random() < short_frac:
                    # keep adapter read-through within the adapter length
                    L = int(rng.integers(read_len - min(len(ADAPTER1), len(ADAPTER2)), read_len))
                else:
                    L = int(max(read_len + 10, rng.normal(300, 30)))
                L = min(L, len(g))
                start = int(rng.integers(0, len(g) - L + 1))
                frag = g[start : start + L]
                if rng.random() < 0.5:
                    frag = revcomp(frag)
            made.append(frag)
        L = len(frag)
        if L < read_len:
            r1 = frag + ADAPTER1[: read_len - L]
            r2 = revcomp(frag) + ADAPTER2[: read_len - L]
        else:
            r1, r2 = frag[:read_len], revcomp(frag)[:read_len]
        q1, q2 = quals(rng, read_len, q0, slope1), quals(rng, read_len, q0, slope2)
        r1, r2 = add_errors(r1, q1, rng), add_errors(r2, q2, rng)
        x, y = int(rng.integers(1000, 30000)), int(rng.integers(1000, 30000))
        tile = 1101 + int(rng.integers(0, 4))
        name = f"VL00123:45:AAAXYZ123:1:{tile}:{x}:{y}"
        qs1 = "".join(chr(33 + int(v)) for v in q1)
        qs2 = "".join(chr(33 + int(v)) for v in q2)
        fr1.append(f"@{name} 1:N:0:{barcode}\n{r1}\n+\n{qs1}\n")
        fr2.append(f"@{name} 2:N:0:{barcode}\n{r2}\n+\n{qs2}\n")
    return "".join(fr1), "".join(fr2)


def make_seq(rng, out: Path):
    d = out / "seq"
    ref, genes = build_reference(rng)
    r1, r2 = genes
    V = {}
    V["V1"] = pick_snp(ref, r1, "synonymous", 50)
    V["V2"] = pick_snp(ref, r1, "missense", 100)
    V["V3"] = pick_snp(ref, r1, "nonsense", 200)
    V["V4"] = intergenic_snp(ref, 2600, rng)
    V["V5"] = pick_snp(ref, r2, "missense", 60)
    V["V6"] = intergenic_snp(ref, 5200, rng)
    D1 = make_deletion(ref, 1000 + 3 * 150, 3)  # remove codon 151 (in frame)
    D1.update(gene="toyR1", consequence="inframe_deletion", effect="p.del(codon 151)", note="3 bp deletion")
    I1 = make_insertion(ref, 1000 + 3 * 250 + 1, "G")  # 1 bp insertion -> frameshift
    I1.update(gene="toyR1", consequence="frameshift_variant", effect="frameshift", note="1 bp insertion")
    M1 = intergenic_snp(ref, 2200, rng)
    M1["note"] = "minor sub-population variant (about 30% of reads)"

    samples = {
        "sampleA": dict(variants=[V["V1"], V["V2"], V["V4"], V["V5"], V["V6"], D1], mixed=None, pairs=1400,
                        kw=dict(q0=37, slope1=0.05, slope2=0.10, short_frac=0.05, contam_frac=0.03, dup_frac=0.04),
                        barcode="ACGTAC"),
        "sampleB": dict(variants=[V["V2"], V["V3"], V["V4"], V["V6"], I1], mixed=M1, pairs=1200,
                        kw=dict(q0=37, slope1=0.06, slope2=0.12, short_frac=0.05, contam_frac=0.03, dup_frac=0.02),
                        barcode="TGACCA"),
        "sampleC": dict(variants=[V["V1"], V["V4"]], mixed=None, pairs=280,
                        kw=dict(q0=33, slope1=0.10, slope2=0.22, short_frac=0.25, contam_frac=0.15, dup_frac=0.10),
                        barcode="GATCAG"),
    }
    truth_rows = []
    for name, s in samples.items():
        major = apply_variants(ref, s["variants"])
        genomes, weights = [major], [1.0]
        vars_here = list(s["variants"])
        if s["mixed"] is not None:
            minor = apply_variants(ref, s["variants"] + [s["mixed"]])
            genomes, weights = [major, minor], [0.7, 0.3]
        a, b = simulate_pairs(genomes, weights, s["pairs"], rng, name, barcode=s["barcode"], **s["kw"])
        write_gz(d / "reads" / f"{name}_R1.fastq.gz", a)
        write_gz(d / "reads" / f"{name}_R2.fastq.gz", b)
        for v in vars_here:
            truth_rows.append([name, "chrToy", v["pos"], v["ref"], v["alt"], v["type"], 1.0, v.get("gene", ""),
                               v.get("consequence", ""), v.get("effect", ""), v.get("note", "")])
        if s["mixed"] is not None:
            v = s["mixed"]
            truth_rows.append([name, "chrToy", v["pos"], v["ref"], v["alt"], v["type"], 0.3, "",
                               v["consequence"], "", v["note"]])

    write_text(d / "ref" / "toy_ref.fa", ">chrToy synthetic 6 kb reference (course toy data)\n" + wrap(ref) + "\n")
    gff = ["##gff-version 3", "##sequence-region chrToy 1 6000"]
    for g in genes:
        gid = g["id"]
        gff += [
            f"chrToy\ttoysim\tgene\t{g['start']}\t{g['end']}\t.\t{g['strand']}\t.\tID=gene:{gid};Name={gid};biotype=protein_coding;description={g['product']}",
            f"chrToy\ttoysim\tmRNA\t{g['start']}\t{g['end']}\t.\t{g['strand']}\t.\tID=transcript:{gid}.1;Parent=gene:{gid};Name={gid}.1;biotype=protein_coding",
            f"chrToy\ttoysim\texon\t{g['start']}\t{g['end']}\t.\t{g['strand']}\t.\tParent=transcript:{gid}.1;Name={gid}.1.exon1",
            f"chrToy\ttoysim\tCDS\t{g['start']}\t{g['end']}\t.\t{g['strand']}\t0\tID=cds:{gid}.1;Parent=transcript:{gid}.1",
        ]
    write_text(d / "ref" / "toy_ref.gff3", "\n".join(gff) + "\n")
    write_text(d / "ref" / "toy_cds_toyR1.fa", ">toyR1 CDS (+ strand, 1001-1900)\n" + wrap(r1["cds"]) + "\n")
    write_text(d / "ref" / "adapters.fa", f">TruSeq_R1_adapter\n{ADAPTER1}\n>TruSeq_R2_adapter\n{ADAPTER2}\n")
    write_tsv(d / "samples.tsv", ["sample", "read1", "read2", "note"], [
        ["sampleA", "reads/sampleA_R1.fastq.gz", "reads/sampleA_R2.fastq.gz", "good quality, about 45x"],
        ["sampleB", "reads/sampleB_R1.fastq.gz", "reads/sampleB_R2.fastq.gz", "good quality, has a minor sub-population"],
        ["sampleC", "reads/sampleC_R1.fastq.gz", "reads/sampleC_R2.fastq.gz", "poor quality, low coverage (a QC teaching case)"],
    ])
    write_tsv(d / "answers" / "truth_variants.tsv",
              ["sample", "chrom", "pos", "ref", "alt", "type", "true_allele_fraction", "gene", "consequence", "protein_effect", "note"],
              truth_rows)
    return ref, genes


# ==========================================================================
# 2. Shared haplotype-block genome simulator (used by gwas and prs)
# ==========================================================================
K_FOUNDERS = 6
BLOCK = 10
AUTO_BLOCKS = 13
X_SNPS = 300  # independent X-chromosome SNPs (one per block) so the sex check is reliable
MU = 0.012  # per-allele flip rate (breaks perfect LD)
POP_MIX = 0.50  # how much POP2 weights resemble POP1 (higher = less divergence)
POP_RISK = 0.35  # extra log-odds of disease in POP2 (creates confounding by ancestry)


def build_panel(rng):
    blocks = [(c, BLOCK) for c in range(1, 23) for _ in range(AUTO_BLOCKS)] + [(23, 1)] * X_SNPS
    founders = []
    for _, n in blocks:
        F = np.zeros((K_FOUNDERS, n + 1), dtype=np.int8)  # last column = hidden causal site
        for j in range(n + 1):
            n1 = int(rng.integers(2, K_FOUNDERS - 1)) if n == 1 else int(rng.integers(1, K_FOUNDERS))  # X SNPs: common alleles
            F[rng.choice(K_FOUNDERS, size=n1, replace=False), j] = 1
        founders.append(F)
    chrom, bp, names, block_of, slices = [], [], [], [], []
    pos_by_chr, count_by_chr = {}, {}
    col = 0
    for b, (c, n) in enumerate(blocks):
        pos = pos_by_chr.get(c, 100_000) + int(rng.integers(200_000, 1_200_000))
        s = col
        for _ in range(n):
            pos += int(rng.integers(1_000, 15_000))
            count_by_chr[c] = count_by_chr.get(c, 0) + 1
            chrom.append(c)
            bp.append(pos)
            names.append(f"ts{c:02d}_{count_by_chr[c]:03d}")
            block_of.append(b)
            col += 1
        pos_by_chr[c] = pos
        slices.append((s, col))
    alleles = []
    for _ in range(len(names)):
        a0, a1 = [("A", "C"), ("A", "G"), ("C", "T"), ("G", "T")][int(rng.integers(4))]
        alleles.append((a0, a1) if rng.random() < 0.5 else (a1, a0))  # (allele coded 0, allele coded 1)
    return dict(blocks=blocks, founders=founders, chrom=np.array(chrom), bp=np.array(bp), names=names,
                block_of=np.array(block_of), slices=slices, alleles=alleles, M=len(names), nb=len(blocks))


def pop_weights(rng, nb, alpha=0.8):
    w1 = rng.dirichlet(np.full(K_FOUNDERS, alpha), size=nb)
    w2 = (1 - POP_MIX) * rng.dirichlet(np.full(K_FOUNDERS, alpha), size=nb) + POP_MIX * w1
    w3 = rng.dirichlet(np.full(K_FOUNDERS, alpha), size=nb)
    return w1, w2, w3


def gen_haps(panel, w, n_hap, rng, mu=MU):
    obs = np.empty((n_hap, panel["M"]), dtype=np.int8)
    hid = np.empty((n_hap, panel["nb"]), dtype=np.int8)
    for b in range(panel["nb"]):
        idx = rng.choice(K_FOUNDERS, size=n_hap, p=w[b])
        block = panel["founders"][b][idx]
        block = block ^ (rng.random(block.shape) < mu).astype(np.int8)
        s, e = panel["slices"][b]
        obs[:, s:e] = block[:, :-1]
        hid[:, b] = block[:, -1]
    return obs, hid


def gen_sib_pairs(panel, w, n_pairs, rng):
    """Return haplotypes (4*n_pairs rows = 2 per child, child order: pair0-sib1, pair0-sib2, ...)."""
    par_obs, _ = gen_haps(panel, w, 4 * n_pairs, rng)
    par = par_obs.reshape(n_pairs, 4, -1)
    out = np.empty((n_pairs * 4, panel["M"]), dtype=np.int8)
    for p in range(n_pairs):
        for sib in range(2):
            h_pat, h_mat = np.empty(panel["M"], np.int8), np.empty(panel["M"], np.int8)
            for b in range(panel["nb"]):
                s, e = panel["slices"][b]
                h_pat[s:e] = par[p, int(rng.integers(2)), s:e]
                h_mat[s:e] = par[p, 2 + int(rng.integers(2)), s:e]
            row = (p * 2 + sib) * 2
            out[row], out[row + 1] = h_pat, h_mat
    return out


def make_hemizygous(obs, sex):
    """obs: (2N, M) haplotypes. Males (sex==1) get the same haplotype twice on X (chrom 23)."""
    return obs  # placeholder; real work is done in to_dosage (needs column mask)


def to_dosage(panel, obs, sex):
    h1, h2 = obs[0::2].astype(np.int8), obs[1::2].astype(np.int8)
    xcols = panel["chrom"] == 23
    male = np.asarray(sex) == 1
    h2 = h2.copy()
    h2[np.ix_(male, xcols)] = h1[np.ix_(male, xcols)]
    return (h1 + h2).astype(np.int8)


def fst_report(panel, w1, w2):
    p1 = np.concatenate([w1[b] @ panel["founders"][b][:, :-1] for b in range(panel["nb"])])
    p2 = np.concatenate([w2[b] @ panel["founders"][b][:, :-1] for b in range(panel["nb"])])
    pb = (p1 + p2) / 2
    ok = (pb > 0.02) & (pb < 0.98)
    return float(np.sum((p1[ok] - p2[ok]) ** 2 / 4) / np.sum(pb[ok] * (1 - pb[ok])))


def write_plink(prefix: Path, geno, panel, inds, flip_ok=True, a1_fixed=None):
    """geno: (N, M) int8 dosage of the allele coded 1; -9 = missing. Writes .bed/.bim/.fam.
    Alleles are re-coded so that A1 is the minor allele (unless that SNP index is in a1_fixed)."""
    N, M = geno.shape
    a1_fixed = set(a1_fixed or [])
    g = geno.copy()
    bim, flipped = [], 0
    for j in range(M):
        col = g[:, j]
        ok = col >= 0
        f1 = col[ok].mean() / 2 if ok.any() else 0.0
        a0, a1 = panel["alleles"][j]
        if f1 > 0.5 and j not in a1_fixed:
            col[ok] = 2 - col[ok]
            a0, a1 = a1, a0
            flipped += 1
        bim.append(f"{panel['chrom'][j]}\t{panel['names'][j]}\t0\t{panel['bp'][j]}\t{a1}\t{a0}")
    code = np.array([0b11, 0b10, 0b00], dtype=np.uint8)
    nbytes = (N + 3) // 4
    prefix.parent.mkdir(parents=True, exist_ok=True)
    with open(str(prefix) + ".bed", "wb") as f:
        f.write(bytes([0x6C, 0x1B, 0x01]))
        for j in range(M):
            col = g[:, j]
            codes = np.where(col < 0, 0b01, code[np.clip(col, 0, 2)]).astype(np.uint8)
            codes = np.concatenate([codes, np.zeros(nbytes * 4 - N, np.uint8)]).reshape(-1, 4)
            f.write((codes[:, 0] | (codes[:, 1] << 2) | (codes[:, 2] << 4) | (codes[:, 3] << 6)).astype(np.uint8).tobytes())
    write_text(Path(str(prefix) + ".bim"), "\n".join(bim) + "\n")
    write_text(Path(str(prefix) + ".fam"), "\n".join("\t".join(str(x) for x in r) for r in inds) + "\n")
    return g


def bisect_intercept(lin, target_prev):
    lo, hi = -15.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        prev = float(np.mean(1 / (1 + np.exp(-(mid + lin)))))
        lo, hi = (mid, hi) if prev < target_prev else (lo, mid)
    return (lo + hi) / 2


# ==========================================================================
# 3. GWAS - case-control cohort with planted QC problems and stratification
# ==========================================================================
def make_gwas(rng, out: Path, panel, weights):
    d = out / "gwas"
    w1, w2, w3 = weights
    n_pool1, n_pool2 = 3600, 2800
    obs1, _ = gen_haps(panel, w1, 2 * n_pool1, rng)
    obs2, _ = gen_haps(panel, w2, 2 * n_pool2, rng)
    obs = np.vstack([obs1, obs2])
    n_pool = n_pool1 + n_pool2
    pop = np.array([1] * n_pool1 + [2] * n_pool2)
    sex = rng.integers(1, 3, size=n_pool)  # 1 male, 2 female
    age = np.clip(np.round(rng.normal(45, 12, n_pool)), 18, 80)
    dos = to_dosage(panel, obs, sex)

    freq = dos.mean(axis=0) / 2
    chrom = panel["chrom"]

    def choose(chr_no, lo, hi, target_idx):
        cand = [j for j in np.nonzero(chrom == chr_no)[0] if lo <= freq[j] <= hi]
        cand.sort(key=lambda j: abs(j - target_idx))
        return int(cand[0])

    first6 = int(np.nonzero(chrom == 6)[0][0])
    first12 = int(np.nonzero(chrom == 12)[0][0])
    causal = choose(6, 0.22, 0.38, first6 + 65)
    suggestive = choose(12, 0.22, 0.38, first12 + 40)

    lin = (np.log(2.0) * dos[:, causal] + np.log(1.6) * dos[:, suggestive] + POP_RISK * (pop == 2)
           + 0.3 * (sex == 2) + 0.015 * (age - 45))
    b0 = bisect_intercept(lin, 0.12)
    p = 1 / (1 + np.exp(-(b0 + lin)))
    y = rng.random(n_pool) < p
    case_idx = rng.choice(np.nonzero(y)[0], size=500, replace=False)
    ctrl_idx = rng.choice(np.nonzero(~y)[0], size=500, replace=False)
    sel = np.concatenate([case_idx, ctrl_idx])
    rng.shuffle(sel)
    N = len(sel)
    status = y[sel].astype(int) + 1  # 1 control, 2 case
    s_sex, s_age, s_pop = sex[sel].copy(), age[sel].copy(), pop[sel].copy()
    hap_rows = np.empty((2 * N, panel["M"]), dtype=np.int8)
    for k, i in enumerate(sel):
        hap_rows[2 * k], hap_rows[2 * k + 1] = obs[2 * i], obs[2 * i + 1]

    # planted: 3 ancestry outliers (POP3)
    out_slots = rng.choice(N, size=3, replace=False)
    o3, _ = gen_haps(panel, w3, 6, rng)
    for k, slot in enumerate(out_slots):
        hap_rows[2 * slot], hap_rows[2 * slot + 1] = o3[2 * k], o3[2 * k + 1]
        s_pop[slot] = 3
    # planted: 3 sibling pairs (POP1)
    free = [i for i in range(N) if i not in set(out_slots)]
    sib_slots = rng.choice(free, size=6, replace=False)
    sibs = gen_sib_pairs(panel, w1, 3, rng)
    for k, slot in enumerate(sib_slots):
        hap_rows[2 * slot], hap_rows[2 * slot + 1] = sibs[2 * k], sibs[2 * k + 1]
        s_pop[slot] = 1
    dos_sel = to_dosage(panel, hap_rows, s_sex)

    # site depends on ancestry
    site_p = {1: [0.6, 0.3, 0.1], 2: [0.1, 0.3, 0.6], 3: [0.1, 0.2, 0.7]}
    site = np.array([int(rng.choice(3, p=site_p[int(pp)])) for pp in s_pop])  # 0=A 1=B 2=C

    # planted: 2 duplicate pairs (a second ID for the same person, 0.3% genotype noise)
    rest = [i for i in range(N) if i not in set(out_slots) | set(sib_slots)]
    dup_src = rng.choice(rest, size=2, replace=False)
    rest2 = [i for i in rest if i not in set(dup_src)]
    dup_dst = rng.choice(rest2, size=2, replace=False)
    for a, b in zip(dup_src, dup_dst):
        row = dos_sel[a].copy()
        noise = rng.random(row.shape) < 0.003
        row[noise] = np.clip(row[noise] + rng.choice([-1, 1], size=noise.sum()), 0, 2)
        dos_sel[b] = row
        s_sex[b], s_pop[b] = s_sex[a], s_pop[a]

    geno = dos_sel.astype(np.int8)
    M = geno.shape[1]
    # planted: low-level random missingness; 12 poor samples; 60 poor SNPs
    geno[rng.random(geno.shape) < 0.003] = -9
    bad_samples = rng.choice(N, size=12, replace=False)
    for i in bad_samples:
        geno[i, rng.random(M) < rng.uniform(0.08, 0.15)] = -9
    autos = np.nonzero(chrom < 23)[0]
    bad_snps = rng.choice(autos, size=60, replace=False)
    for j in bad_snps:
        geno[rng.random(N) < rng.uniform(0.08, 0.25), j] = -9
    # planted: 25 SNPs failing Hardy-Weinberg (excess heterozygotes)
    hwe_cand = [j for j in autos if 0.25 < geno[:, j][geno[:, j] >= 0].mean() / 2 < 0.5 and j not in (causal, suggestive)]
    hwe_snps = rng.choice(hwe_cand, size=25, replace=False)
    for j in hwe_snps:
        hom = np.nonzero((geno[:, j] == 0) | (geno[:, j] == 2))[0]
        flip = hom[rng.random(len(hom)) < 0.40]
        geno[flip, j] = 1

    # IDs and .fam; planted: 6 sex-label mismatches
    ids = [f"P{n:04d}" for n in rng.permutation(np.arange(1, N + 1))]
    fam_sex = s_sex.copy()
    mism = rng.choice(N, size=6, replace=False)
    fam_sex[mism] = 3 - fam_sex[mism]
    inds = [(ids[i], ids[i], 0, 0, int(fam_sex[i]), int(status[i])) for i in range(N)]
    fixed = {causal, suggestive}
    write_plink(d / "cohort", geno, panel, inds, a1_fixed=fixed)

    write_tsv(d / "covariates.tsv", ["FID", "IID", "AGE", "SEX", "SITE_B", "SITE_C"],
              [[ids[i], ids[i], int(s_age[i]), int(fam_sex[i]), int(site[i] == 1), int(site[i] == 2)] for i in range(N)])

    # answer key
    a_pop = {1: "POP1", 2: "POP2", 3: "POP3_outlier"}
    write_tsv(d / "answers" / "true_ancestry.tsv", ["IID", "true_group"], [[ids[i], a_pop[int(s_pop[i])]] for i in range(N)])
    problems = []
    for i in bad_samples:
        problems.append(["sample", ids[i], "high missingness (8-15% of SNPs)"])
    for i in mism:
        problems.append(["sample", ids[i], f".fam sex ({int(fam_sex[i])}) disagrees with X-chromosome genotypes"])
    for a, b in zip(dup_src, dup_dst):
        problems.append(["sample_pair", f"{ids[a]},{ids[b]}", "duplicate (same person, PI_HAT ~ 1)"])
    for k in range(3):
        problems.append(["sample_pair", f"{ids[sib_slots[2 * k]]},{ids[sib_slots[2 * k + 1]]}", "full siblings (PI_HAT ~ 0.5)"])
    for slot in out_slots:
        problems.append(["sample", ids[slot], "ancestry outlier (POP3) - look at PC1/PC2"])
    for j in bad_snps:
        problems.append(["snp", panel["names"][j], "high missingness (8-25%)"])
    for j in hwe_snps:
        problems.append(["snp", panel["names"][j], "excess heterozygosity (HWE failure)"])
    write_tsv(d / "answers" / "planted_problems.tsv", ["level", "id", "problem"], problems)
    write_text(d / "answers" / "truth.md",
               "# GWAS toy cohort - answer key\n\n"
               f"- Cohort: {N} people, 500 cases / 500 controls, {M} SNPs on chromosomes 1-22 and X (coded 23).\n"
               f"- Main causal SNP: **{panel['names'][causal]}** (chromosome {int(chrom[causal])}, bp {int(panel['bp'][causal])}); "
               "allele A1 is the risk allele, simulated odds ratio 2.0 per copy.\n"
               f"- Suggestive SNP: **{panel['names'][suggestive]}** (chromosome {int(chrom[suggestive])}); simulated OR 1.6 per copy - "
               "expect it to be suggestive, not genome-wide significant.\n"
               "- Population stratification: POP2 has higher baseline risk and is over-represented among cases, so naive tests are inflated.\n"
               "- Planted problems: see `planted_problems.tsv`. True ancestry labels: `true_ancestry.tsv`.\n"
               "- Chromosome 23 = X; males are hemizygous (homozygous calls).\n")
    return dict(causal=causal, suggestive=suggestive)


# ==========================================================================
# 4. PRS - base GWAS summary statistics (POP1) + a two-group target cohort
# ==========================================================================
def make_prs(rng, out: Path, panel, weights, gwas_info):
    d = out / "prs"
    w1, w2, w3 = weights
    H2 = 0.4
    nb = panel["nb"]
    autos_blocks = [b for b in range(nb) if panel["blocks"][b][0] < 23]
    n_causal_blocks = int(0.4 * len(autos_blocks))
    cblocks = rng.choice(autos_blocks, size=n_causal_blocks, replace=False)
    beta_h = np.zeros(nb)
    beta_h[cblocks] = rng.normal(0, 1, n_causal_blocks)

    n_base = 10000
    obs_b, hid_b = gen_haps(panel, w1, 2 * n_base, rng)
    sex_b = rng.integers(1, 3, n_base)
    dos_b = to_dosage(panel, obs_b, sex_b)
    hd_b = hid_b[0::2] + hid_b[1::2]
    g_b = hd_b @ beta_h
    scale = math.sqrt(H2 / g_b.var())
    beta_h *= scale
    g_b = g_b * scale
    age_b = np.clip(rng.normal(50, 12, n_base), 18, 85)
    y_b = g_b + 0.25 * (sex_b == 2) + 0.01 * (age_b - 50) + rng.normal(0, math.sqrt(1 - H2), n_base)

    auto_cols = np.nonzero(panel["chrom"] < 23)[0]
    X = dos_b[:, auto_cols].astype(float)
    xm, ym = X.mean(0), y_b.mean()
    xc, yc = X - xm, y_b - ym
    sxx = (xc ** 2).sum(0)
    beta = (xc * yc[:, None]).sum(0) / sxx
    resid_var = ((yc ** 2).sum() - beta ** 2 * sxx) / (n_base - 2)
    se = np.sqrt(resid_var / sxx)
    pval = erfc_p(beta / se)
    f1 = X.mean(0) / 2

    # target cohort: 400 per group
    n_t = 400
    obs_t1, hid_t1 = gen_haps(panel, w1, 2 * n_t, rng)
    obs_t2, hid_t2 = gen_haps(panel, w3, 2 * n_t, rng)  # G2 = a distant ancestry (different LD/frequencies)
    # G2: weaker LD between the array SNPs and the hidden causal sites (extra flips on array SNPs only)
    obs_t2 = obs_t2 ^ (rng.random(obs_t2.shape) < 0.12).astype(np.int8)
    obs_t = np.vstack([obs_t1, obs_t2])
    hid_t = np.vstack([hid_t1, hid_t2])
    group = np.array(["G1"] * n_t + ["G2"] * n_t)
    N = 2 * n_t
    sex_t = rng.integers(1, 3, N)
    age_t = np.clip(np.round(rng.normal(50, 12, N)), 18, 85)
    dos_t = to_dosage(panel, obs_t, sex_t)
    g_t = (hid_t[0::2] + hid_t[1::2]) @ beta_h
    y_t = g_t + 0.25 * (sex_t == 2) + 0.01 * (age_t - 50) + rng.normal(0, math.sqrt(1 - H2), N)

    order = rng.permutation(N)
    ids = [f"T{n:04d}" for n in range(1, N + 1)]
    dos_t, sex_t, age_t, y_t, group = dos_t[order], sex_t[order], age_t[order], y_t[order], group[order]
    geno = dos_t.astype(np.int8)
    geno[rng.random(geno.shape) < 0.002] = -9
    inds = [(ids[i], ids[i], 0, 0, int(sex_t[i]), -9) for i in range(N)]
    written = write_plink(d / "target", geno, panel, inds)
    write_tsv(d / "target_pheno.tsv", ["FID", "IID", "TRAIT", "AGE", "SEX", "GROUP"],
              [[ids[i], ids[i], f"{y_t[i]:.4f}", int(age_t[i]), int(sex_t[i]), group[i]] for i in range(N)])

    # base file in the same allele coding as the target .bim, with planted harmonisation traps
    bim = [ln.split("\t") for ln in (d / "target.bim").read_text().strip().split("\n")]
    bim_by_id = {r[1]: r for r in bim}
    rows = []
    for k, j in enumerate(auto_cols):
        snp = panel["names"][j]
        r = bim_by_id[snp]
        a1, a2 = r[4], r[5]
        # effect of the allele coded 1 in the raw simulation; map to target A1
        raw_a0, raw_a1 = panel["alleles"][j]
        b_raw = beta[k]
        fr = f1[k]
        if a1 == raw_a1:  # target A1 is the coded-1 allele
            eff_allele, oth, b_eff, fa = a1, a2, b_raw, fr
        else:  # target flipped coding
            eff_allele, oth, b_eff, fa = a1, a2, -b_raw, 1 - fr
        rows.append([snp, int(panel["chrom"][j]), int(panel["bp"][j]), eff_allele, oth, fa, b_eff, se[k], pval[k], n_base])
    idx_nonamb = [i for i, r in enumerate(rows) if {r[3], r[4]} not in ({"A", "T"}, {"C", "G"})]
    swap_idx = rng.choice(idx_nonamb, size=4, replace=False)       # valid: alleles swapped AND beta negated
    flip_idx = rng.choice([i for i in idx_nonamb if i not in set(swap_idx)], size=6, replace=False)  # strand-flipped labels
    traps = []
    for i in swap_idx:
        r = rows[i]
        r[3], r[4], r[5], r[6] = r[4], r[3], 1 - r[5], -r[6]
        traps.append([r[0], "alleles swapped (A1/A2 reversed, beta sign flipped) - harmonise by matching alleles"])
    for i in flip_idx:
        r = rows[i]
        r[3], r[4] = COMP_BASE[r[3]], COMP_BASE[r[4]]
        traps.append([r[0], "strand-flipped labels (complement alleles) - resolve by complementing"])
    write_tsv(d / "base_gwas_sumstats.tsv", ["SNP", "CHR", "BP", "A1", "A2", "FREQ_A1", "BETA", "SE", "P", "N"],
              [[r[0], r[1], r[2], r[3], r[4], f"{r[5]:.4f}", f"{r[6]:.5f}", f"{r[7]:.5f}", f"{r[8]:.4g}", r[9]] for r in rows])
    write_tsv(d / "answers" / "harmonisation_traps.tsv", ["SNP", "issue"], traps)
    write_text(d / "answers" / "truth.md",
               "# PRS toy data - answer key\n\n"
               "- Trait is continuous; heritability set to 0.40 in G1.\n"
               f"- Causal variants are **hidden** (not on the array): {n_causal_blocks} blocks carry one. SNPs on the array only *tag* them.\n"
               "- Base GWAS: 10,000 people of G1-like ancestry, autosomes only (no X SNPs in the file).\n"
               "- Target: 400 people from G1 (same ancestry as the base GWAS) and 400 from G2 (a distant ancestry with different allele frequencies and LD). The score is built from G1-ancestry effect sizes, so expect it to predict worse in G2 - portability is the point.\n"
               "- `harmonisation_traps.tsv` lists the SNPs whose labels were deliberately altered in the base file.\n")
    # stash arrays for the check script
    np.savez_compressed(d / "answers" / "_hidden_effects.npz", beta_h=beta_h, cblocks=cblocks)
    return None


# ==========================================================================
# 5. OUTBREAK - 73 isolates, 4 kb alignment, clusters + sporadic + noise
# ==========================================================================
def make_outbreak(rng, out: Path):
    d = out / "outbreak"
    L = 4000
    g0 = np.array(list("".join(rng.choice(list("ACGT"), size=L))))
    r_site = 2730  # 0-based resistance site
    alt_r = str(rng.choice([b for b in "ACGT" if b != g0[r_site]]))

    def mutate(seq, n):
        s = seq.copy()
        for _ in range(int(n)):
            while True:
                i = int(rng.integers(L))
                if i != r_site:
                    break
            s[i] = str(rng.choice([b for b in "ACGT" if b != s[i]]))
        return s

    lineage1 = mutate(g0, 20)
    founders = {
        "C1": mutate(lineage1, 10),
        "C3": mutate(lineage1, 12),
        "C2": mutate(g0, 40),
    }
    founders["C2"][r_site] = alt_r

    def dates(start, n, peak, span):
        offs = np.sort(np.clip(np.round(rng.triangular(0, peak, span, n)), 0, span)).astype(int)
        return [start + timedelta(days=int(o)) for o in offs]

    spec = [
        ("C1", 30, date(2026, 1, 19), 35, 70, 0.6, ["A"] * 7 + ["B"] * 3),
        ("C2", 15, date(2026, 3, 2), 25, 50, 0.5, ["C"] * 17 + ["E"] * 3),
        ("C3", 8, date(2026, 4, 13), 10, 20, 0.3, ["D"]),
    ]
    iso = []  # dicts
    for cl, n, start, peak, span, lam, dist_pool in spec:
        ds = dates(start, n, peak, span)
        seqs = []
        for i in range(n):
            if i == 0:
                parent = founders[cl]
            else:
                parent = seqs[int(rng.integers(max(0, i - 6), i))]
            seqs.append(mutate(parent, rng.poisson(lam)))
        for i in range(n):
            district = dist_pool[int(rng.integers(len(dist_pool)))] if len(dist_pool) > 1 else dist_pool[0]
            fac = "hospital_H" if cl == "C3" else str(rng.choice(["clinic", "clinic", "hospital", "community"]))
            iso.append(dict(cluster=cl, seq=seqs[i], date=ds[i], district=district, facility=fac))
    # sporadic: 12 from lineage1 background, 8 from g0 background (2 of those carry the resistance allele independently)
    for k in range(20):
        base = lineage1 if k < 12 else g0
        s = mutate(base, rng.integers(20, 35) if k < 12 else rng.integers(40, 60))
        if k in (13, 17):
            s[r_site] = alt_r
        dte = date(2026, 1, 5) + timedelta(days=int(rng.integers(0, 173)))
        iso.append(dict(cluster="sporadic", seq=s, date=dte, district=str(rng.choice(list("ABCDEF"))),
                        facility=str(rng.choice(["clinic", "hospital", "community"]))))
    n_iso = len(iso)
    perm = rng.permutation(n_iso)
    iso = [iso[i] for i in perm]
    for i, r in enumerate(iso):
        r["id"] = f"ISO-{i + 1:03d}"
    # phenotype, demographics
    for r in iso:
        carries = r["seq"][r_site] == alt_r
        r["cip"] = "R" if carries else "S"
        r["age"] = int(np.clip(round(rng.normal(32 if r["facility"] != "hospital_H" else 61, 16)), 1, 90))
        r["sex"] = str(rng.choice(["F", "M"]))
        r["outcome"] = "died" if rng.random() < (0.2 if r["cluster"] == "C3" else 0.04) else "recovered"
    disc = [r for r in iso if r["cluster"] == "C2"][3]
    disc["cip"] = "S"  # planted genotype-phenotype discordance

    # planted issues
    typo = [r for r in iso if r["cluster"] == "C1"][5]
    typo_orig = typo["date"]
    typo["date"] = typo["date"].replace(year=2025)
    n_bad = [r for r in iso if r["cluster"] == "sporadic"][:2]
    for r in n_bad:
        s = r["seq"].copy()
        s[rng.random(L) < 0.12] = "N"
        r["seq"] = s

    fasta = "".join(f">{r['id']}\n{wrap(''.join(r['seq']))}\n" for r in sorted(iso, key=lambda r: r["id"]))
    write_text(d / "outbreak_alignment.fasta", fasta)
    write_text(d / "outbreak_reference.fasta", f">ref_ancestor\n{wrap(''.join(g0))}\n")
    rows = [[r["id"], r["date"].isoformat(), r["district"], r["facility"], r["age"], r["sex"], r["outcome"], r["cip"]]
            for r in sorted(iso, key=lambda r: r["id"])]
    dup = rows[10][:]  # planted duplicate row
    rows.insert(11, dup)
    write_tsv(d / "outbreak_metadata.tsv",
              ["isolate_id", "collection_date", "district", "facility", "age", "sex", "outcome", "ciprofloxacin"], rows)
    write_tsv(d / "answers" / "clusters_truth.tsv", ["isolate_id", "true_cluster"],
              [[r["id"], r["cluster"]] for r in sorted(iso, key=lambda r: r["id"])])
    write_text(d / "answers" / "truth.md",
               "# Outbreak toy data - answer key\n\n"
               "- Alignment: 73 isolates x 4,000 positions (all sites kept, including invariant ones).\n"
               "- True groups: C1 (30 isolates, districts A/B), C2 (15, districts C/E, carries the ciprofloxacin-resistance "
               f"mutation at alignment position {r_site + 1}), C3 (8, hospital H in district D), and 20 sporadic isolates.\n"
               "- C1 and C3 share a recent common ancestor (a 'lineage'), so they are close but distinct clusters; C2 is a different lineage.\n"
               "- Two sporadic isolates carry the resistance mutation by independent mutation (convergence): resistance does not imply relatedness.\n"
               "- Planted data problems: (1) one C1 isolate has its collection year mistyped as 2025; "
               "(2) one metadata row is duplicated; (3) two isolates have >10% N bases; "
               "(4) one C2 isolate carries the mutation but is phenotypically susceptible.\n"
               f"- The mistyped isolate is {typo['id']} (true date {typo_orig.isoformat()}); the discordant isolate is {disc['id']}; "
               f"the duplicated row is {dup[0]}; high-N isolates are {', '.join(r['id'] for r in n_bad)}.\n")


# ==========================================================================
# 6. LINELIST - a deliberately messy surveillance linelist
# ==========================================================================
def make_linelist(rng, out: Path):
    d = out / "linelist"
    n = 600
    districts = ["Savanna North", "Savanna South", "Lakeside", "Coastal Hub", "Highland", "Delta East"]
    seq_rate = dict(zip(districts, [0.55, 0.40, 0.25, 0.70, 0.10, 0.15]))
    probs = np.array([0.22, 0.15, 0.14, 0.25, 0.08, 0.16])
    rows, truth = [], []
    start = date(2026, 1, 5)
    for i in range(1, n + 1):
        dist = districts[int(rng.choice(len(districts), p=probs))]
        onset = start + timedelta(days=int(np.clip(rng.gamma(4.0, 14.0), 0, 175)))
        age = int(np.clip(round(rng.gamma(3.0, 11.0)), 0, 95))
        sex = str(rng.choice(["F", "M"]))
        fac = str(rng.choice(["clinic", "hospital", "community"], p=[0.5, 0.3, 0.2]))
        died = rng.random() < (0.12 if age > 60 else 0.03)
        seqd = rng.random() < seq_rate[dist] * (1.2 if fac == "hospital" else 1.0)
        ct = float(np.clip(rng.normal(27, 5), 12, 40))
        truth.append([f"C-{i:04d}", onset.isoformat(), age, sex, dist, fac, "died" if died else "alive", int(seqd)])
        # ---- messy renderings ----
        fmt = rng.choice(["iso", "iso", "dmy", "long", "blank"], p=[0.45, 0.2, 0.2, 0.1, 0.05])
        d_s = {"iso": onset.isoformat(), "dmy": onset.strftime("%d/%m/%Y"), "long": onset.strftime("%d %b %Y").lstrip("0"),
               "blank": ""}[str(fmt)]
        r = rng.random()
        a_s = (str(age) if r < 0.80 else f"{age} yrs" if r < 0.86 else "999" if r < 0.89 else "-1" if r < 0.91
               else "" if r < 0.95 else f"{max(age, 1) * 12} months" if age < 5 else str(age))
        sx = str(rng.choice([sex, sex, sex, "male" if sex == "M" else "Female", sex.lower(), "", "unknown"],
                            p=[0.4, 0.2, 0.1, 0.12, 0.08, 0.05, 0.05]))
        ds = str(rng.choice([dist, dist, dist.upper(), dist.lower(), " " + dist + " ", dist.replace("Savanna", "Savana")],
                            p=[0.5, 0.15, 0.1, 0.1, 0.1, 0.05])) if True else dist
        oc = "died" if died else "alive"
        oc_s = str(rng.choice([oc, oc.capitalize(), oc.upper(), "dead" if died else "recovered", ""],
                              p=[0.6, 0.15, 0.08, 0.12, 0.05]))
        sq = str(rng.choice(["Y", "yes", "1", "TRUE"] if seqd else ["N", "no", "0", "FALSE"]))
        seq_id = f"SEQ-{i:04d}" if seqd and rng.random() < 0.9 else ("SEQ-%04d" % i if (not seqd and rng.random() < 0.02) else "")
        ct_s = f"{ct:.1f}" if rng.random() < 0.85 else str(rng.choice(["ND", "", "NA"]))
        rows.append([f"C-{i:04d}", d_s, a_s, sx, ds, fac, oc_s, sq, seq_id, ct_s])
    rows.insert(300, rows[299][:])  # planted duplicate
    write_tsv(d / "linelist_messy.csv",
              ["case_id", "date_onset", "age", "sex", "district", "facility_type", "outcome", "sequenced", "sequence_id", "ct_value"],
              rows, sep=",")
    write_tsv(d / "answers" / "linelist_truth.csv",
              ["case_id", "date_onset", "age", "sex", "district", "facility_type", "outcome", "sequenced"], truth, sep=",")
    write_text(d / "answers" / "cleaning_notes.md",
               "# Linelist cleaning - what was planted\n\n"
               "- `date_onset`: three formats (ISO `2026-02-03`, `03/02/2026` as day/month/year, `3 Feb 2026`) plus ~5% blanks.\n"
               "- `age`: some like `34 yrs`, some in months (`18 months`), impossible values `999` and `-1`, and blanks.\n"
               "- `sex`: `M`, `F`, `male`, `Female`, lower-case, blank and `unknown`.\n"
               "- `district`: upper/lower case, stray spaces, and a misspelling (`Savana North`).\n"
               "- `outcome`: capitalisation variants, `dead`/`recovered`, blanks.\n"
               "- `sequenced`: `Y/yes/1/TRUE` vs `N/no/0/FALSE`; ~2% of unsequenced cases still have a `sequence_id` (a data conflict).\n"
               "- `ct_value`: `ND`, `NA` or blank in ~15% of rows.\n"
               "- One duplicated row (the row after `C-0300`).\n"
               "- `linelist_truth.csv` is the clean version for checking your work. Sequencing rate differs strongly by district (bias!).\n")


# ==========================================================================
# 7. LINUX practice folder
# ==========================================================================
def make_linux(rng, out: Path, seq_dir: Path):
    d = out / "linux"
    regions = ["North", "South", "East", "West"]
    rows = []
    for i in range(1, 25):
        rows.append([f"S{i:03d}", "RUN_0412", int(rng.integers(1, 5)), "ACGTAC"[: 6], f"2026-03-{int(rng.integers(1, 29)):02d}",
                     str(rng.choice(regions)), int(rng.integers(150_000, 900_000))])
    write_tsv(d / "sample_sheet.csv", ["sample_id", "run", "lane", "barcode", "collection_date", "region", "read_pairs"], rows, sep=",")
    lines = []
    t = date(2026, 3, 30)
    msgs = [("INFO", "cluster density {} K/mm2"), ("INFO", "lane {} Q30 {}%"), ("INFO", "demultiplexing started"),
            ("WARN", "lane {} Q30 below 80% ({}%)"), ("INFO", "tile {} passed filter"), ("ERROR", "tile {} failed focus check")]
    for k in range(300):
        kind = rng.choice(len(msgs), p=[0.15, 0.35, 0.05, 0.08, 0.32, 0.05])
        lvl, m = msgs[int(kind)]
        lane = int(rng.integers(1, 5))
        if "{}" in m:
            if "density" in m:
                m = m.format(int(rng.integers(150, 260)))
            elif "Q30 below" in m:
                m = m.format(lane, int(rng.integers(68, 79)))
            elif "Q30" in m:
                m = m.format(lane, int(rng.integers(82, 96)))
            else:
                m = m.format(1100 + int(rng.integers(1, 120)))
        lines.append(f"2026-03-30 {9 + k // 60:02d}:{k % 60:02d}:{int(rng.integers(0, 60)):02d} {lvl:<5} [lane{lane}] {m}")
    write_text(d / "sequencing_run.log", "\n".join(lines) + "\n")
    # a deliberately messy project directory (spaces, mixed case, odd extensions)
    messy = d / "messy_project"
    names = ["Sample A final FINAL v2.txt", "sample_b notes.TXT", "results (old).csv", "Results_NEW.csv", "fig1 - draft.png.txt",
             "README", "run2/lane1_reads.fq", "run2/lane2_reads.fq", "Run 3/lane1 reads.fq", "tmp/do_not_delete.txt"]
    for nm in names:
        write_text(messy / nm, f"placeholder for {nm}\n")
    # tiny fastq files cut from the real simulated reads
    mini = d / "fastq_mini"
    for s in ("sampleA", "sampleB", "sampleC"):
        with gzip.open(seq_dir / "reads" / f"{s}_R1.fastq.gz", "rt") as f:
            txt = "".join([next(f) for _ in range(4 * 25)])
        write_text(mini / f"{s}_mini_R1.fastq", txt)


# ==========================================================================
# main
# ==========================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=CANONICAL_SEED)
    ap.add_argument("--out", type=Path, default=ROOT / "data")
    ap.add_argument("--only", nargs="*", choices=["seq", "gwas", "prs", "outbreak", "linelist", "linux"])
    args = ap.parse_args()
    out = args.out
    todo = set(args.only or ["seq", "gwas", "prs", "outbreak", "linelist", "linux"])

    # independent, named streams so changing one dataset never changes another
    def stream(name):
        return np.random.default_rng([args.seed, sum(ord(c) * (i + 1) for i, c in enumerate(name))])

    if "seq" in todo:
        make_seq(stream("seq"), out)
        print("seq done")
    panel = weights = gwas_info = None
    if todo & {"gwas", "prs"}:
        prng = stream("panel")
        panel = build_panel(prng)
        weights = pop_weights(prng, panel["nb"])
        print(f"panel: {panel['M']} SNPs in {panel['nb']} blocks; Fst(POP1,POP2) ~ {fst_report(panel, weights[0], weights[1]):.3f}")
    if "gwas" in todo:
        gwas_info = make_gwas(stream("gwas"), out, panel, weights)
        print("gwas done; causal =", panel["names"][gwas_info["causal"]])
    if "prs" in todo:
        make_prs(stream("prs"), out, panel, weights, gwas_info)
        print("prs done")
    if "outbreak" in todo:
        make_outbreak(stream("outbreak"), out)
        print("outbreak done")
    if "linelist" in todo:
        make_linelist(stream("linelist"), out)
        print("linelist done")
    if "linux" in todo:
        if not (out / "seq" / "reads").exists():
            make_seq(stream("seq"), out)
        make_linux(stream("linux"), out, out / "seq")
        print("linux done")


if __name__ == "__main__":
    main()
