
#!/usr/bin/env python3
# prove_cosmic_decode.py  (reproducible proof)

import argparse, subprocess, sys, json, hashlib, base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

ANOMALY_PW = "and the anomaly revealed as both beginning and end"
AES_BLOB_B64 = "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"

def sha256(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def ensure_openssl():
    try:
        subprocess.run(["openssl","version"], check=True, capture_output=True, text=True)
    except Exception:
        print("ERROR: OpenSSL not found in PATH", file=sys.stderr)
        sys.exit(2)

def openssl_dec_ctr(in_path: Path, out_path: Path, pw: str):
    cmd = ["openssl","enc","-d","-aes-256-ctr","-in", str(in_path), "-out", str(out_path), "-pass", f"pass:{pw}"]
    r = subprocess.run(cmd, text=True, capture_output=True)
    if r.returncode != 0:
        print("OpenSSL error:", r.stderr, file=sys.stderr)
        sys.exit(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cosmic", type=Path, default=Path("cosmic_raw_decoded.bin"))
    ap.add_argument("--blob-out", type=Path, default=Path("decrypted_from_blob_via_openssl.bin"))
    ap.add_argument("--plain-out", type=Path, default=Path("cosmic_decrypted_plain.bin"))
    ap.add_argument("--inner-bin", type=Path, default=Path("cosmic_inner_utf16le.bin"))
    ap.add_argument("--inner-txt", type=Path, default=Path("cosmic_inner_utf8.txt"))
    ap.add_argument("--proof-json", type=Path, default=Path("cosmic_decode_proof.json"))
    args = ap.parse_args()

    ensure_openssl()

    # 1) recover 80-byte key material
    blob_enc = Path("aes_blob.enc")
    blob_enc.write_bytes(base64.b64decode(AES_BLOB_B64))
    openssl_dec_ctr(blob_enc, args.blob_out, ANOMALY_PW)
    kb = args.blob_out.read_bytes()
    if len(kb) != 80:
        print(f"ERROR: expected 80 bytes from blob, got {{len(kb)}}", file=sys.stderr)
        sys.exit(2)

    # 2) outer decrypt
    if not args.cosmic.exists():
        print(f"ERROR: {{args.cosmic}} not found", file=sys.stderr); sys.exit(2)
    openssl_dec_ctr(args.cosmic, args.plain_out, ANOMALY_PW)
    data = args.plain_out.read_bytes()

    # 3) parse header (tag=31, len=53)
    if not (data[0] & 0x80 and (data[0] & 0x40) and (data[0] & 0x3F)==31 and data[1]==53):
        print("ERROR: not tag=31,len=53", file=sys.stderr); sys.exit(2)
    hdr = data[2:2+53]; payload = data[2+53:]
    g2 = hdr[1:17]

    # 4) inner AES-CTR
    key = kb[40:72]; iv = g2
    pt = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend()).decryptor().update(payload)

    args.inner_bin.write_bytes(pt)
    try: txt = pt.decode("utf-16le")
    except Exception: txt = pt.decode("utf-16le", errors="ignore")
    args.inner_txt.write_text(txt, encoding="utf-8")

    proof = {
        "outer": {
            "passphrase": ANOMALY_PW,
            "mode": "aes-256-ctr",
            "sha256_output": sha256(args.plain_out),
            "g2_iv_hex": g2.hex()
        },
        "inner": {
            "cipher": "AES-CTR",
            "key_source": "blob[40:72]",
            "key_hex": key.hex(),
            "iv_hex": iv.hex(),
            "sha256_inner_txt": sha256(args.inner_txt)
        },
        "blob": {
            "sha256_blob_out": sha256(args.blob_out)
        }
    }
    args.proof_json.write_text(json.dumps(proof, indent=2), encoding="utf-8")
    print("[OK] Proof:", args.proof_json)

if __name__ == "__main__":
    main()
