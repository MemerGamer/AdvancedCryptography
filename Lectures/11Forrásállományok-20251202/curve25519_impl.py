"""
Curve25519 (X25519) Elliptic Curve Diffie-Hellman Key Exchange.

This module provides a secure, Python-native implementation of the X25519 key exchange
protocol as defined in RFC 7748.

Standards:
    - RFC 7748: Security Considerations and X25519 definition.
    - Curve25519: high-speed elliptic-curve cryptography (Bernstein, 2006).

Security Notice:
    This implementation uses algorithmic constant-time primitives (Montgomery Ladder,
    branchless conditional swaps) to mitigate timing attacks. However, as a pure Python
    implementation running on an interpreter, it cannot guarantee complete immunity against
    sophisticated side-channel attacks (cache timing, branch prediction analysis) that
    optimized C/Assembly implementations (like libsodium) provide. 
    
    It is suitable for:
    - Educational understanding of the protocol.
    - Prototyping and testing.
    - Production use where side-channel attacks on the specific Python runtime are not 
      part of the threat model.
"""

import secrets
from typing import Tuple, Optional

# =============================================================================
# Curve25519 Parameters
# =============================================================================

# Prime field modulus: 2^255 - 19
P: int = 2 ** 255 - 19

# Montgomery curve constant (A - 2) / 4, where A = 486662
# used in the differential addition/doubling steps.
A24: int = 121665 


def cswap(swap: int, x_2: int, x_3: int) -> Tuple[int, int]:
    """
    Constant-time conditional swap.
    
    Exchanges x_2 and x_3 if swap is 1.
    Leaves x_2 and x_3 unchanged if swap is 0.
    
    This function uses bitwise operations to avoid data-dependent branching,
    which helps mitigate timing side-channel attacks.
    
    Args:
        swap (int): Control bit (0 or 1).
        x_2 (int): First value.
        x_3 (int): Second value.
        
    Returns:
        Tuple[int, int]: The (potentially swapped) values (x_2, x_3).
    """
    # Calculate mask: if swap is 1, dummy is (x_2 ^ x_3), else 0
    dummy = (x_2 ^ x_3) * swap
    x_2 ^= dummy
    x_3 ^= dummy
    return x_2, x_3


def x25519(k: bytes, u: bytes) -> bytes:
    """
    X25519 scalar multiplication function.
    
    Computes the public key or shared secret by multiplying the scalar k
    by the curve point u-coordinate.
    
    Args:
        k (bytes): 32-byte private key (scalar).
        u (bytes): 32-byte u-coordinate (public key or base point).
        
    Returns:
        bytes: 32-byte u-coordinate of the resulting point (little-endian).
        
    Raises:
        ValueError: If input byte lengths are incorrect.
    """
    if len(k) != 32:
        raise ValueError("Scalar (private key) must be exactly 32 bytes.")
    if len(u) != 32:
        raise ValueError("U-coordinate (public key) must be exactly 32 bytes.")

    # 1. Clamp the scalar (as per RFC 7748)
    # This ensures the scalar is a multiple of 8, clears the 255th bit,
    # and sets the 254th bit. This prevents small-subgroup attacks and
    # ensures fixed execution time logic.
    k_list = bytearray(k)
    k_list[0] &= 248        # Clear lowest 3 bits
    k_list[31] &= 127       # Clear highest bit
    k_list[31] |= 64        # Set second highest bit
    
    scalar = int.from_bytes(k_list, 'little')
    
    # 2. Decode the u-coordinate
    # Mask the most significant bit of the final byte as per RFC 7748
    u_int = int.from_bytes(u, 'little')
    u_int &= (1 << 255) - 1
    
    # 3. Montgomery Ladder
    # This algorithm computes P = scalar * U in constant iterations.
    x_1 = u_int
    x_2 = 1
    z_2 = 0
    x_3 = u_int
    z_3 = 1
    swap = 0
    
    # Iterate from 254 down to 0
    for t in range(254, -1, -1):
        b = (scalar >> t) & 1
        
        # Conditional swap based on bit change
        swap ^= b
        x_2, x_3 = cswap(swap, x_2, x_3)
        z_2, z_3 = cswap(swap, z_2, z_3)
        swap = b
        
        # Differential Addition and Doubling (Montgomery formulas)
        # Using modular arithmetic for field operations
        A = (x_2 + z_2) % P
        AA = pow(A, 2, P)
        B = (x_2 - z_2) % P
        BB = pow(B, 2, P)
        E = (AA - BB) % P
        C = (x_3 + z_3) % P
        D = (x_3 - z_3) % P
        DA = (D * A) % P
        CB = (C * B) % P
        
        # New coordinates
        x_3 = pow(DA + CB, 2, P)
        z_3 = (x_1 * pow(DA - CB, 2, P)) % P
        x_2 = (AA * BB) % P
        z_2 = (E * (AA + A24 * E)) % P
        
    # Final conditional swap to restore correct order
    x_2, x_3 = cswap(swap, x_2, x_3)
    z_2, z_3 = cswap(swap, z_2, z_3)
    
    # 4. Convert Projective (X, Z) to Affine (x)
    # x = X / Z = X * Z^(-1) mod P
    # Calculate modular inverse using Fermat's Little Theorem: Z^(P-2)
    inv_z_2 = pow(z_2, P - 2, P)
    x = (x_2 * inv_z_2) % P
    
    return x.to_bytes(32, 'little')


def generate_keypair() -> Tuple[bytes, bytes]:
    """
    Generates a secure X25519 keypair.
    
    Returns:
        Tuple[bytes, bytes]: A tuple containing:
            - private_key (32 bytes): The secret scalar.
            - public_key (32 bytes): The calculated public point.
    """
    private_key = secrets.token_bytes(32)
    # The generator point for Curve25519 is u = 9
    base_point = (9).to_bytes(32, 'little')
    public_key = x25519(private_key, base_point)
    return private_key, public_key


def compute_shared_secret(private_key: bytes, peer_public_key: bytes) -> bytes:
    """
    Computes the Diffie-Hellman shared secret.
    
    Args:
        private_key (bytes): Your 32-byte private key.
        peer_public_key (bytes): The other party's 32-byte public key.
        
    Returns:
        bytes: The 32-byte shared secret.
    """
    return x25519(private_key, peer_public_key)


# =============================================================================
# Testing and Verification
# =============================================================================

def run_tests():
    """
    Runs self-tests including RFC 7748 test vectors and a simulated exchange.
    """
    print("Running Curve25519 (X25519) Integrity Checks...")
    
    # ---------------------------------------------------------
    # Test Vector 1 from RFC 7748, Section 6.1
    # ---------------------------------------------------------
    alice_priv_hex = '77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a'
    expected_pub_hex = '8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a'
    
    alice_priv = bytes.fromhex(alice_priv_hex)
    base_point = (9).to_bytes(32, 'little')
    
    result_pub = x25519(alice_priv, base_point)
    
    if result_pub.hex() == expected_pub_hex:
        print("[PASS] RFC 7748 Test Vector 1")
    else:
        print(f"[FAIL] RFC 7748 Test Vector 1")
        print(f"  Expected: {expected_pub_hex}")
        print(f"  Got:      {result_pub.hex()}")
        return

    # ---------------------------------------------------------
    # Test Vector 2 (Shared Secret) from RFC 7748
    # ---------------------------------------------------------
    bob_priv_hex = '5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb'
    bob_priv = bytes.fromhex(bob_priv_hex)
    
    # Alice calculates shared secret using Bob's public key (derived from Bob's priv)
    bob_pub = x25519(bob_priv, base_point)
    shared_secret = x25519(alice_priv, bob_pub)
    
    expected_shared_hex = '4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742'
    
    if shared_secret.hex() == expected_shared_hex:
        print("[PASS] RFC 7748 Test Vector 2 (Shared Secret)")
    else:
        print(f"[FAIL] RFC 7748 Test Vector 2")
        print(f"  Expected: {expected_shared_hex}")
        print(f"  Got:      {shared_secret.hex()}")
        return

    # ---------------------------------------------------------
    # Simulated Key Exchange
    # ---------------------------------------------------------
    print("\nSimulating Ephemeral Key Exchange...")
    
    alice_priv, alice_pub = generate_keypair()
    bob_priv, bob_pub = generate_keypair()
    
    alice_shared = compute_shared_secret(alice_priv, bob_pub)
    bob_shared = compute_shared_secret(bob_priv, alice_pub)
    
    if alice_shared == bob_shared:
        print(f"[PASS] Key Exchange Simulation")
        print(f"  Alice Pub: {alice_pub.hex()[:16]}...")
        print(f"  Bob Pub:   {bob_pub.hex()[:16]}...")
        print(f"  Shared:    {alice_shared.hex()[:16]}...")
    else:
        print("[FAIL] Key Exchange Simulation: Secrets mismatch!")

if __name__ == "__main__":
    run_tests()
