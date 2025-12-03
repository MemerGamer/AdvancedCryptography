from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol import KDF
from Crypto.Protocol.DH import key_agreement
import os

# Define the shared INFO string for HKDF
HKDF_INFO = b"SignalProtocol.DoubleRatchet"


def KDF_RK(rk: bytes, dh_output: bytes) -> tuple[bytes, bytes]:
    """
    KDF_RK: Key Derivation Function for the Root Key Ratchet (uses HKDF-SHA256)
    Input: Root Key (rk), Diffie-Hellman Output (dh_output)
    Output: New Root Key (new_rk), New Chain Key (new_ck)
    """
    # Use dh_output as the salt (standard Signal/Noise Protocol practice)
    # Derive 2 keys of 32 bytes each (RK and CK)
    new_rk, new_ck = KDF.HKDF(
        master=rk,
        key_len=32,
        salt=dh_output,
        hashmod=SHA256,
        num_keys=2,
        context=HKDF_INFO
    )
    return new_rk, new_ck


def KDF_CK(ck: bytes) -> tuple[bytes, bytes]:
    """
    KDF_CK: Key Derivation Function for the Chain Key Ratchet (uses HMAC-SHA256)
    Signal's specification uses HMAC to derive the next Chain Key and Message Key.
    Input: Chain Key (ck)
    Output: New Chain Key (new_ck), Message Key (mk)
    """
    # T_1 is the next Chain Key (new_ck)
    h_ck = HMAC.new(ck, digestmod=SHA256)
    h_ck.update(b'\x01')
    new_ck = h_ck.digest()

    # T_2 is the Message Key (mk)
    h_mk = HMAC.new(ck, digestmod=SHA256)
    h_mk.update(b'\x02')
    mk = h_mk.digest()

    return new_ck, mk


def AES256_GCM_Encrypt(key: bytes, plaintext: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes, bytes]:
    """Encrypts data using AES-256 in GCM mode."""
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(associated_data)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce, ciphertext, tag


def AES256_GCM_Decrypt(key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes, associated_data: bytes = b"") -> bytes:
    """Decrypts data using AES-256 in GCM mode."""
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(associated_data)
    # The digest will raise a ValueError if the tag is invalid (authentication failure)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


# --- ECC Helper Functions using Curve25519 (analogous to X25519) ---

def generate_dh_keys():
    """Generates a new Curve25519 key pair."""
    # We use ECC with the Curve25519 standard
    private_key = ECC.generate(curve='Curve25519')
    # pycryptodome's ECC keys for Curve25519 are typically 32-byte binary representations
    return private_key


def dh_exchange(private_key: ECC.EccKey, public_key_bytes: bytes) -> bytes:
    """Performs the Diffie-Hellman exchange."""
    # For Curve25519, construct public key from raw bytes
    # Curve25519 public keys are 32-byte u-coordinates (little-endian)
    # Convert bytes to integer and construct the public key
    u_coordinate = int.from_bytes(public_key_bytes, 'little')
    public_key = ECC.construct(curve='Curve25519', point_x=u_coordinate)
    
    # Use key_agreement for ECDH (works with Curve25519)
    # kdf=lambda x: x returns the raw shared secret without transformation
    shared_secret = key_agreement(static_priv=private_key, static_pub=public_key, kdf=lambda x: x)
    # Hash the shared secret to get a fixed 32-byte DH output
    h = SHA256.new(shared_secret)
    return h.digest()


class SessionState:
    def __init__(self, name: str, initial_root_key: bytes, initial_send_chain_key: bytes):
        self.name = name
        # --- Root Ratchet State ---
        self.RK = initial_root_key  # Root Key (32 bytes)
        self.DHs = generate_dh_keys()  # Sender's Ephemeral Private Key
        self.DHr_pk_bytes = None  # Receiver's Ephemeral Public Key bytes (last received)

        # --- Symmetric Ratchet State ---
        self.CKs = initial_send_chain_key  # Sending Chain Key (32 bytes)
        self.CKr = None  # Receiving Chain Key (32 bytes)
        self.Ns = 0  # Number of messages sent in current chain
        self.Nr = 0  # Number of messages received in current chain

        # --- Message Key Store for out-of-order messages ---
        # Key: (Public_Key_Bytes, Message_Number), Value: Message_Key
        self.MK_Skipped: dict[tuple[bytes, int], bytes] = {}

    def get_public_key_bytes(self) -> bytes:
        """Returns the public key in a raw byte format (32 bytes for Curve25519)."""
        # For Curve25519, export in raw format (32 bytes)
        return self.DHs.public_key().export_key(format='raw')

    def __str__(self) -> str:
        return (f"--- {self.name} State ---\n"
                f"RK: {self.RK[:4].hex()}...\n"
                f"CKs: {self.CKs[:4].hex()}... (Sent: {self.Ns})\n"
                f"CKr: {self.CKr[:4].hex()}... (Recv: {self.Nr})" if self.CKr else "Not yet initialized")


def ratchet_encrypt(session: SessionState, plaintext: bytes) -> dict:
    """Performs the Symmetric Ratchet and then Encrypts a message."""

    # 1. Symmetric Ratchet: Derive new Chain Key and Message Key
    session.CKs, mk = KDF_CK(session.CKs)

    # 2. Encrypt
    header_public_key = session.get_public_key_bytes()

    # Associated Data for integrity: Public Key + Message Number
    associated_data = header_public_key + session.Ns.to_bytes(4, 'big')

    nonce, ciphertext, tag = AES256_GCM_Encrypt(mk, plaintext, associated_data)

    # 3. Update State
    message_number = session.Ns
    session.Ns += 1

    # Return the "wire message" components
    return {
        'PK': header_public_key,
        'N': message_number,
        'Nonce': nonce,
        'Ciphertext': ciphertext,
        'Tag': tag,
    }


def ratchet_decrypt(session: SessionState, received_message: dict) -> str:
    """Processes a received message and performs the DH or Symmetric Ratchet."""
    R_PK = received_message['PK']
    R_N = received_message['N']

    # 1. Check Skipped Message Keys
    # Handle out-of-order messages within the current chain
    if (R_PK, R_N) in session.MK_Skipped:
        mk = session.MK_Skipped.pop((R_PK, R_N))

        # Decrypt using the stored Message Key
        associated_data = R_PK + R_N.to_bytes(4, 'big')
        plaintext = AES256_GCM_Decrypt(mk, received_message['Nonce'], received_message['Ciphertext'],
                                       received_message['Tag'], associated_data)
        return plaintext.decode('utf-8')

    # 2. Check for New Diffie-Hellman Ratchet (DH Ratchet)
    # The ratchet advances if the received public key (R_PK) is different from the last used key (DHr_pk_bytes).
    # Special case: if this is the first message (DHr_pk_bytes is None) but we already have CKr from X3DH,
    # we should use the existing CKr and not do a DH ratchet yet. The DH ratchet happens on the NEXT message.
    is_first_message = (session.DHr_pk_bytes is None and session.CKr is not None)
    
    if not is_first_message and (session.DHr_pk_bytes is None or R_PK != session.DHr_pk_bytes):
        print(f"\n*** {session.name} performing DH Ratchet! (Key Change Detected) ***")

        # A. Store/Skip old message keys (Perfect Forward Secrecy)
        if session.CKr is not None:
            # Generate and store all remaining possible message keys from the old chain
            print(f"Skipping {R_N - session.Nr} keys from old receiving chain (CKr, N={session.Nr}).")
            while session.Nr < R_N:
                session.CKr, skip_mk = KDF_CK(session.CKr)
                session.MK_Skipped[(session.DHr_pk_bytes, session.Nr)] = skip_mk
                session.Nr += 1

        # B. Perform the ECDH exchange (The DH Ratchet Step)

        # New Receiver DH Key: The public key from the received message
        session.DHr_pk_bytes = R_PK

        # Shared Secret: Current Private Key (DHs) + Received Public Key (R_PK)
        dh_output = dh_exchange(session.DHs, R_PK)

        # C. Advance the Root Key (RK) and establish new Receiving Chain Key (CKr)
        session.RK, session.CKr = KDF_RK(session.RK, dh_output)
        session.Nr = 0
    elif is_first_message:
        # First message: just record the sender's public key, use existing CKr from X3DH
        session.DHr_pk_bytes = R_PK

        # D. Advance the Sender's Chain (The Sender's DH Ratchet Step)
        # Generate a NEW key pair for *future* messages (Post-Compromise Security)
        session.DHs = generate_dh_keys()

        # Use the *new* private key (DHs) and the *received* public key (R_PK)
        dh_output_new = dh_exchange(session.DHs, R_PK)

        # E. Advance RK and establish new Sending Chain Key (CKs)
        session.RK, session.CKs = KDF_RK(session.RK, dh_output_new)
        session.Ns = 0

    # 3. Symmetric Ratchet: Derive Message Key and Decrypt

    # Advance the CKr until we reach the message number R_N
    # We need to derive keys for messages Nr, Nr+1, ..., R_N
    # So we loop while Nr < R_N, then derive one more for R_N
    while session.Nr < R_N:
        session.CKr, _ = KDF_CK(session.CKr)  # Skip intermediate message keys
        session.Nr += 1
    
    # Now derive the message key for R_N
    session.CKr, mk = KDF_CK(session.CKr)
    session.Nr += 1

    # Decrypt
    associated_data = R_PK + R_N.to_bytes(4, 'big')
    plaintext = AES256_GCM_Decrypt(
        mk,
        received_message['Nonce'],
        received_message['Ciphertext'],
        received_message['Tag'],
        associated_data
    )

    return plaintext.decode('utf-8')

# --- Initial Setup (Mimicking X3DH Output) ---
# In a real Signal implementation, these would come from X3DH key exchange
# For this demo, we simulate X3DH by having both parties share initial keys
INITIAL_RK = os.urandom(32)

# In Signal, X3DH establishes a shared secret from which both parties derive:
# - Root Key (RK) - same for both
# - Initial chain keys - Alice's sending chain = Bob's receiving chain (and vice versa)
# For this demo, we derive a shared initial chain key that both can use
SHARED_INITIAL_CK, _ = KDF.HKDF(master=INITIAL_RK, key_len=32, salt=b"", hashmod=SHA256, num_keys=2, context=b"InitialChainKey")

# Party A (Alice) - starts with sending chain key (matches Bob's receiving chain)
alice = SessionState(name="Alice", initial_root_key=INITIAL_RK, initial_send_chain_key=SHARED_INITIAL_CK)
# Party B (Bob) - initialize receiving chain key to match Alice's sending chain
bob = SessionState(name="Bob", initial_root_key=INITIAL_RK, initial_send_chain_key=os.urandom(32))
bob.CKr = SHARED_INITIAL_CK  # Set Bob's receiving chain to match Alice's sending chain

# --- 1. Alice sends first message (Triggers DH Ratchet on Bob) ---
print("--- 1. Alice sends first message (Initial DH step on Bob's side) ---")
msg1 = ratchet_encrypt(alice, b"Hello Bob, starting the pycryptodome ratchet.")
print(f"Alice's Public Key: {msg1['PK'].hex()[:8]}...")
print(alice)

decrypted1 = ratchet_decrypt(bob, msg1)
print(f"\nBob decrypted: '{decrypted1}'")
print(bob)

# --- 2. Bob replies (Triggers DH Ratchet on Alice) ---
print("\n--- 2. Bob replies (Initial DH step on Alice's side) ---")
msg2 = ratchet_encrypt(bob, b"Ratcheting established. Over.")
print(f"Bob's Public Key: {msg2['PK'].hex()[:8]}...")
print(bob)

decrypted2 = ratchet_decrypt(alice, msg2)
print(f"\nAlice decrypted: '{decrypted2}'")
print(alice)

# --- 3. Alice sends second message (Symmetric Ratchet) ---
print("\n--- 3. Alice sends second message (Symmetric Ratchet) ---")
msg3 = ratchet_encrypt(alice, b"Symmetric key advance initiated.")
print(alice)

decrypted3 = ratchet_decrypt(bob, msg3)
print(f"\nBob decrypted: '{decrypted3}'")
print(bob)

# --- 4. Bob replies again (Symmetric Ratchet) ---
print("\n--- 4. Bob sends second message (Symmetric Ratchet) ---")
msg4 = ratchet_encrypt(bob, b"Another key used and discarded.")
print(bob)

decrypted4 = ratchet_decrypt(alice, msg4)
print(f"\nAlice decrypted: '{decrypted4}'")
print(alice)