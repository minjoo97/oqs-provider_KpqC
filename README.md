# KpqC-provider for OpenSSL (3.x)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
![Status](https://img.shields.io/badge/status-research--only-orange)

## Overview

**KpqC-provider** is a fork of the official [oqs-provider](https://github.com/open-quantum-safe/oqs-provider) that integrates Post-Quantum Cryptography (PQC) into OpenSSL 3.x via the provider interface.

This fork preserves all upstream features while adding **four Korean PQC (KpqC) algorithms**, making it possible to evaluate both NIST-standardized algorithms and leading KpqC candidates within a single provider.

---

## 🌟 Key Features

* **Upstream Compatible**: Fully supports `oqs-provider` features (TLS 1.3 KEMs & signatures, CMS, CMP, EVP, X.509/PKCS#12, etc.).
* **KpqC Support**: Adds SMAUG-T, NTRU+, AIMer, and HAETAE.
* **Hybrid & Composite**: Supports classical + PQC combinations, as in the upstream `oqs-provider`.
* **OpenSSL Integration**: Functions as a drop-in provider for research and prototyping.

---

## 🛡️ Supported Algorithms

### 🇰🇷 Korean PQC (KpqC) algorithms

* **KEMs**
    * **SMAUG-T**: `smaug_t1`, `smaug_t3`, `smaug_t5`
    * **NTRU+**: `ntru_plus_kem576`, `ntru_plus_kem768`, `ntru_plus_kem864`, `ntru_plus_kem1152`
* **Signatures**
    * **AIMer**: `AIMer128f/s`, `AIMer192f/s`, `AIMer256f/s`
    * **HAETAE**: `HAETAE2`, `HAETAE3`, `HAETAE5`

### 🌍 Upstream oqs-provider algorithms

This fork retains the entire `oqs-provider` suite, including BIKE, FrodoKEM, HQC, ML-KEM (Kyber), NTRU-Prime, ML-DSA (Dilithium), Falcon, SPHINCS+, and more. For the full list, please see the [upstream documentation](https://github.com/open-quantum-safe/oqs-provider).

> **👉 Check enabled algorithms at runtime:**
> ```bash
> openssl list -kem-algorithms -provider oqsprovider
> openssl list -signature-algorithms -provider oqsprovider
> ```

---

## ⚠️ Notes on OpenSSL 3.5+

* OpenSSL 3.5+ includes native `ML-KEM` and `ML-DSA`.
* With `oqs-provider ≥ 0.9.0`, overlapping liboqs IDs are **auto-disabled** when OpenSSL’s native ones are present.
* **In practice**:
    * Use OpenSSL’s built-ins for `ML-KEM`/`ML-DSA` on version 3.5+.
    * Use this provider for **all other PQC algorithms**, including KpqC.
    * On OpenSSL < 3.5, the provider's versions remain active.

---

## 🔒 Limitations & Security

* This project is for **research and prototyping only** — it is not production-ready.
* **Do not use** to protect sensitive data.
* Follow the upstream [liboqs security guidelines](https://github.com/open-quantum-safe/liboqs#limitations-and-security).
* Prefer **hybrid cryptography** (PQC + classical) during migration testing.

> **Note on AVX2**
>
> Experimental AVX2-optimized KpqC implementations are included but **not fully validated**. Use them only for performance evaluation, never for security-critical deployments.

---

## 🚀 Quickstart

### Build (Linux/macOS)

```bash
git clone -b main <your-repo-url>
cd KpqC-provider
mkdir build && cd build
cmake -GNinja ..
ninja

### Test

From the `build` directory:
```bash
ctest

(You may also adapt upstream’s scripts/fullbuild.sh and scripts/runtests.sh.)


##Activate the Provider
# Example: Set OPENSSL_MODULES to where the built provider is installed
export OPENSSL_MODULES=/usr/local/lib/ossl-modules

# Verify algorithms are available
openssl list -kem-algorithms -provider oqsprovider
openssl list -signature-algorithms -provider oqsprovider

Windows (Visual Studio 2019+)
Clone the repository.

Open the folder in Visual Studio (CMake auto-configures).

Build the ALL_BUILD target.

📜 License
This project is licensed under the MIT License. See LICENSE.txt for details. Upstream oqs-provider and liboqs are also MIT-licensed.

🙏 Acknowledgements
This project is a fork of oqs-provider, built on liboqs. We thank the OQS contributors and the PQCA under the Linux Foundation.
