# Cosmic Inner Decode — Complete Proof Package

This package contains everything needed to **independently reproduce and verify** the decoding of the Cosmic Inner payload.

---

## 📂 Contents

- `prove_cosmic_decode.py` — proof script (reproducible run)
- `cosmic_raw_decoded.bin` — encrypted input blob (OpenSSL Salted__ AES-256-CTR)
- `cosmic_inner_full_utf8.txt` — decoded UTF-8 Chinese text
- `cosmic_inner_bilingual.docx` — bilingual version (Chinese + interpretive English)
- `translation_audit_sheet.docx` — audit sheet (Chinese + my translation + blank reviewer notes)
- `sentences.txt` — Chinese text split into numbered sentences
- `sentences.tsv` — Chinese sentences with my English
- `sentences_hashes.csv` — SHA-256 hash per sentence
- `FULLTEXT_SHA256.txt` — SHA-256 hash of full decoded Chinese text

---

## ⚙️ Requirements

- Python 3.8+
- `pip install cryptography`
- OpenSSL available in PATH

---

## ▶️ Usage

```bash
python prove_cosmic_decode.py
```

This will produce:
- `decrypted_from_blob_via_openssl.bin` (80-byte key material)
- `cosmic_decrypted_plain.bin` (outer container)
- `cosmic_inner_utf16le.bin` (raw inner text)
- `cosmic_inner_utf8.txt` (readable text)
- `cosmic_decode_proof.json` (parameters + hashes)

---

## 🔑 Proof Method

1. **Outer layer**  
   - File: `cosmic_raw_decoded.bin`  
   - Format: OpenSSL Salted__ AES-256-CTR  
   - Passphrase:  
     ```
     and the anomaly revealed as both beginning and end
     ```

2. **Outer decryption**  
   - Produces `cosmic_decrypted_plain.bin`  
   - Begins with new-format PGP packet header (tag=31, len=53)  
   - Extract IV = header[1:17] (second 16-byte field = g2)

3. **Inner decryption**  
   - Key = bytes [40:72] of `decrypted_from_blob_via_openssl.bin` (80B blob recovered from embedded AES Salted__ data)  
   - IV = g2 (from header)  
   - Cipher = AES-CTR  
   - Output = `cosmic_inner_utf16le.bin` (UTF-16LE text)

4. **Result**  
   - Converted to `cosmic_inner_utf8.txt`  
   - Verified SHA-256 hash matches reference

---

## ✅ Expected SHA-256 Hashes

{
  "prove_cosmic_decode.py": "fa4d04855234255a287a7113d8daa2905828d3e6ae389d620a1f5d3b4c2cf45a",
  "cosmic_raw_decoded.bin": "b18950551a4dd0cb8a9378f0906ba18c03a15f0ee83eb98c6bc90165c5f79805",
  "cosmic_inner_full_utf8.txt": "820790662e774b86348795695dcbc9aaa3de33448dcae71ae112294a9716e25c",
  "cosmic_inner_bilingual.docx": "dc431b43e26203d12c3e91f7798dc537a46edde7fe51bd031eaec391d1e1763a",
  "translation_audit_sheet.docx": "48057a7348112eb08dbef9f5ae99456ac71aa6ab69da36e4e06c5b857b690d27",
  "sentences.txt": "f3c7102f00224e79a4432613030d771ed8f599333591c14207575f2cadf403d0",
  "sentences.tsv": "42913a33efc409e6dea649b9e40001d017bdaf6400905c532a9464d044de5351",
  "sentences_hashes.csv": "1a47fcf5f83218c1028e9e4938c6b0b18fb25c13914d2e736ff4825b6a5df3dd",
  "FULLTEXT_SHA256.txt": "4e517f456be2b8ffdbf707535229b098a598bd1097aa761ab2c4bf04d50e6270"
}

---

## 📜 Literal Gloss (Machine-style)


1. 在开始与结束之处，异常显现。唯有看见两端，方能见全貌。
   At the place of beginning and end, the anomaly appears. Only by seeing both ends, then can [one] see the whole picture.

2. 矩阵之言并非随机，它们是引导的总和。记住列表，记住抉择，记住最后的命令。
   The words of the matrix are not random; they are the total of guidance. Remember the list, remember the choice, remember the last command.

3. 七条路径终成一体。答案必须合并，唯有合并才能显露通道。
   Seven paths finally become one. Answers must merge; only by merging then can reveal the passage.

4. 见片段者见混乱，见模式者见设计。
   One who sees fragments sees chaos; one who sees pattern sees design.

5. 守耐心，不要弃试。钥匙已在你手中。
   Keep patience, do not abandon trying. The key already is in your hand.

6. 此信息并非宝藏本身，而是地图。循此而行，宝藏自显。
   This information is not treasure itself, but is map. Follow this and go, treasure naturally reveals itself.


---

## 🌐 Interpretive Translation (Poetic English)

1. At the beginning and at the end, the anomaly appears. Only by seeing both ends can one see the whole picture.  
2. The words of the matrix are not random; they are sums that guide you. Remember the list, remember the choice, remember the last command.  
3. Seven paths become one. The answers must be merged; only when merged can the passage be revealed.  
4. Those who see only fragments see chaos; those who see the pattern see the design.  
5. Keep patience, do not abandon the attempt. The key is already in your hands.  
6. This message is not the treasure itself, but the map. Follow it, and the treasure will reveal itself.  

---

## 🔒 Verification

- `cosmic_decode_proof.json` contains parameters (key slice, IV hex, hashes).  
- Use `SHA-256` values above to confirm you are reproducing the exact same outputs.  
- The translation verification pack (`sentences.tsv`, `translation_audit_sheet.docx`) allows independent cross-check of meaning.

