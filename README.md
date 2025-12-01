 # oqs-provider-KpqC

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
![Status](https://img.shields.io/badge/status-research--only-orange)

**oqs-provider-KpqC** is a fork of the official [oqs-provider](https://github.com/open-quantum-safe/oqs-provider) that integrates Post-Quantum Cryptography (PQC) into OpenSSL 3.x via the provider interface.

This fork preserves all upstream features while adding **four Korean PQC (KpqC) algorithms**, making it possible to evaluate both NIST-standardized algorithms and leading KpqC candidates within a single provider.

---

## 🌟 Key Features

* **KpqC Support**: Adds SMAUG-T, NTRU+, AIMer, and HAETAE via `KpqC-liboqs`.
* **Upstream Compatible**: Fully supports standard `oqs-provider` features.
* **OpenSSL Integration**: Functions as a drop-in provider for research and prototyping.

---

## 🛡️ Supported Algorithms

### 🇰🇷 Korean PQC (KpqC)

* **KEMs**: `SMAUG-T`, `NTRU+`
* **Signatures**: `AIMer`, `HAETAE`

### 🌍 Upstream Algorithms
Retains the full suite including ML-KEM (Kyber), ML-DSA (Dilithium), Falcon, SPHINCS+, etc.

---

## ⚠️ Prerequisites

### 1. Mandatory Dependency
* **You MUST install [KpqC-liboqs](https://github.com/minjoo97/liboqs_KpqC) first.**
* 🚨 **Do NOT use standard `liboqs`** (e.g., via Homebrew). This provider requires the specific KpqC algorithms found only in `KpqC-liboqs`.

### 2. Platform Support
* **Verified on:** **macOS (Apple Silicon)** only.

---

## 🚀 Quickstart (macOS Apple Silicon)

This guide assumes you have already installed **KpqC-liboqs** to `/usr/local`.

1.  **Install Dependencies**
    ```bash
    brew install cmake ninja openssl@3 git
    ```

2.  **Clone Repository**
    ```bash
    git clone [https://github.com/minjoo97/oqs-provider_KpqC.git](https://github.com/minjoo97/oqs-provider_KpqC.git)
    cd oqs-provider_KpqC
    ```

3.  **Configure Build (CMake)**
    This configuration installs the library to `/usr/local` and explicitly targets arm64 architecture.
    ```bash
    cmake -GNinja \
      -DOPENSSL_ROOT_DIR=$(brew --prefix openssl@3) \
      -Dliboqs_DIR=/usr/local/lib/cmake/liboqs \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -S . -B build
    ```

4.  **Build and Install**
    ```bash
    cmake --build build
    sudo cmake --install build
    ```
    *(Note: `sudo` is required to install into `/usr/local/lib/ossl-modules`)*

---
## 🙏 Acknowledgements

This project is a fork of the Open Quantum Safe (OQS) project's **oqs-provider**, built on top of **liboqs**. We thank all OQS contributors for their foundational work on both the provider and the underlying library.

The OQS project is supported by the Post-Quantum Cryptography Alliance (PQCA) under the Linux Foundation.
