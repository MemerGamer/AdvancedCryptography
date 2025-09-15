# Advanced Cryptography Exercises

This repository contains implementations of various cryptographic operations in multiple programming languages.

## Exercise List

[Exercise Description](./ExcerciseDescription.md)

1. **Password Hashing** (Python) - PBKDF2 with SHA-256
2. **Symmetric Encryption** (Python) - AES encryption/decryption
3. **Digital Signatures** (Python) - RSA signatures with PSS padding
4. **Safe File Access** (Python) - Path traversal protection
5. **SQL Operations** (JavaScript) - Parameterized queries
6. **Integer Formatting** (C) - Thousand separators

All implementations focus on security best practices and include proper input validation.

## Directory Structure

```shell
.
├── python/ # Python implementations
│ ├── main.py # Main demonstration script
│ ├── requirements.txt # Python dependencies
│ └── exercises/ # Individual exercise implementations
│ ├── first.py # Password hashing with PBKDF2
│ ├── second.py # Symmetric encryption with AES
│ ├── third.py # Digital signatures with RSA
│ └── fourth.py # Safe file access with path validation
├── javascript/ # JavaScript implementations
│ └── exercise5.js # SQL operations with parameterized queries
├── c/ # C implementations
│ └── exercise6.c # Integer formatting with thousand separators
├── README.md
└── Exercise Notes.md

```

## Running the Code

### Python Exercises (1-4)

```bash
cd python
pip install -r requirements.txt
python main.py
```

### JavaScript Exercise (5)

```bash
cd javascript
node exercise5.js
```

### C Exercise (6)

```bash
cd c
gcc -o exercise6 exercise6.c
./exercise6
```
