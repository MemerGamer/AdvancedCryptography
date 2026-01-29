# sss_secure_backup.py
from Crypto.Util.number import *
import hashlib
from Crypto.Random import get_random_bytes
from shamir_secret_share import *
from datetime import datetime
import random

class DistributedKeyBackup:
    def __init__(self, threshold, locations):
        self.threshold = threshold
        self.locations = locations

    def backup_keys(self, keys_dict, prime):
        # minden kulcsot len(self.locations) darab reszre osztunk
        # amelyet self.threshold resz-bol lehet majd visszaallitani
        backups = {}

        for key_name, key_value in keys_dict.items():
            # a reszek meghatarozasahoz a kulcsokat atalakitjuk int-e
            if isinstance(key_value, bytes):
                key_int = int.from_bytes(key_value[:32])
            elif isinstance(key_value, str):
                key_int = int.from_bytes(
                    hashlib.sha256(key_value.encode()).digest()[:32])
            else:
                key_int = key_value

            # a reszek meghatarozasa
            shares = generate_shares(key_int, self.threshold, len(self.locations), prime)

            # 1. VALÓS TIMESTAMP GENERÁLÁSA
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # a kulcs, a reszek es a helysegek osszekapcsolasa
            location_shares = {}
            for i, location in enumerate(self.locations):
                location_shares[location] = {
                    'share': shares[i],
                    'key_name': key_name,
                    'timestamp': current_timestamp,  # valós timestamp
                    'backup_id': f"BK{str(abs(hash(key_name + str(i))))[:8]}"
                }

            backups[key_name] = {
                'shares': shares,
                'locations': location_shares,
                'metadata': {
                    'created': current_timestamp,  # valós timestamp
                    'type': 'Password' if isinstance(key_value, str) else 'Binary Key',
                    'protected': True
                }
            }
        return backups

    def recover_key(self, key_name, shares_from_locations, prime):
        if len(shares_from_locations) < self.threshold:
            print(f"❌ A visszaállításhoz {self.threshold} helység szükséges, de csak {len(shares_from_locations)} áll rendelkezésre!")
            return None

        # a megadott helysegek reszeinek a kivalasztasa
        shares = []
        for location_data in shares_from_locations.values():
            if 'share' in location_data:
                shares.append(location_data['share'])

        # a megadott kulcs visszaallitasa a reszekbol
        key_int = reconstruct_secret(shares, self.threshold, prime)
        key_bytes = key_int.to_bytes(32)

        print(f"✅ A kulcs neve: {key_name}")
        print(f"   A felhasznált helységek száma: {len(shares_from_locations)}")
        print(f"   A visszaállított érték: {key_bytes.hex()}")

        return key_bytes

# 2. RANDOM HELYSÉG KIVÁLASZTÁS FÜGGVÉNY
def select_random_locations(all_locations, count):
    """Véletlenszerűen kiválaszt 'count' számú helységet a listából"""
    if count > len(all_locations):
        print(f"⚠️ Figyelem: {count} helységet kértél, de csak {len(all_locations)} áll rendelkezésre!")
        count = len(all_locations)
    
    selected = random.sample(all_locations, count)
    print(f"🎲 Véletlenszerűen kiválasztott helységek ({len(selected)} db):")
    for loc in selected:
        print(f"   - {loc}")
    return selected

# 3. & 4. KÜLÖNBÖZŐ KONFIGURÁCIÓK TESZTELÉSE
def test_configuration(threshold, total_locations, recovery_locations, prime):
    """
    Tesztelés különböző konfigurációkkal
    
    Args:
        threshold: minimum helységek száma a visszaállításhoz
        total_locations: összes helység száma
        recovery_locations: helységek száma a visszaállítás során
        prime: prímszám a számításokhoz
    """
    print("\n" + "="*70)
    print(f"🧪 TESZT KONFIGURÁCIÓ:")
    print(f"   Threshold (minimum): {threshold}")
    print(f"   Összes helység: {total_locations}")
    print(f"   Visszaállításhoz használt helységek: {recovery_locations}")
    print("="*70 + "\n")
    
    all_locations = [
        "eu-east-1 (Budapest)",
        "eu-west-1 (Dublin)",
        "ap-northeast-1 (Tokyo)",
        "eu-east-2 (Kolozsvár)",
        "ap-southeast-2 (Sydney)",
        "us-east-1 (Virginia)",
        "us-west-2 (Oregon)",
        "sa-east-1 (São Paulo)"
    ]
    
    # Csak a szükséges számú helységet választjuk ki
    selected_locations = all_locations[:total_locations]
    
    backup_system = DistributedKeyBackup(
        threshold=threshold,
        locations=selected_locations
    )

    # a backup-okhoz szukseges kulcsok
    encryption_keys = {
        'database_master_key': get_random_bytes(32),
        'file_encryption_key': get_random_bytes(32),
        'backup_encryption_key': get_random_bytes(32),
        'admin_password_hash': "hashed_admin_password_2024"
    }
    
    print('🔑 Eredeti kulcsok:')
    print('database_master_key: ', encryption_keys['database_master_key'].hex())
    print('file_encryption_key: ', encryption_keys['file_encryption_key'].hex())
    print('backup_encryption_key: ', encryption_keys['backup_encryption_key'].hex())
    print('admin_password_hash: ', hashlib.sha256(encryption_keys['admin_password_hash'].encode()).digest()[:32].hex())
    print()

    print("📦 A kulcsok szétosztása:")
    print(f"Helységek száma: {len(backup_system.locations)}")
    print(f"A visszaállításhoz szükséges helységek száma (threshold): {backup_system.threshold}")
    print()

    # a backup-ok letrehozasa
    backups = backup_system.backup_keys(encryption_keys, prime)

    print("✅ A kulcsokat sikeresen szétosztottuk:")
    for key_name, backup_data in backups.items():
        locations = list(backup_data['locations'].keys())
        print(f"  📁 {key_name}:")
        print(f"     Helységek: {', '.join(locations)}")
        print(f"     Létrehozva: {backup_data['metadata']['created']}")
    print()

    # 2. VÉLETLENSZERŰ HELYSÉGEK KIVÁLASZTÁSA
    available_locations = select_random_locations(
        backup_system.locations, 
        recovery_locations
    )
    print()
    
    # A kulcsok visszaállítása
    print("🔄 A megadott kulcs visszaállítása...")
    selected_key = 'admin_password_hash'
    shares_to_recover = {}
    
    for location in available_locations:
        if location in backup_system.locations:
            shares_to_recover[location] = {
                'share': backups[selected_key]['shares'][
                    backup_system.locations.index(location)
                ],
                'timestamp': backups[selected_key]['locations'][location]['timestamp']
            }

    # a kulcs meghatarozasa a reszekbol
    recovered_key = backup_system.recover_key(
        selected_key, shares_to_recover, prime
    )
    
    # Ellenőrzés
    if recovered_key:
        original_hash = hashlib.sha256(encryption_keys[selected_key].encode()).digest()[:32]
        if recovered_key == original_hash:
            print("✅ SIKERES visszaállítás! A kulcs megegyezik az eredetivel.\n")
        else:
            print("❌ HIBA! A visszaállított kulcs NEM egyezik az eredetivel!\n")
    
    return backup_system, backups

def main():
    prime = getPrime(512)
    
    # TESZT 1: Normál működés (threshold = 3, locations = 5, recovery = 3)
    print("\n" + "#"*70)
    print("# TESZT 1: NORMÁL MŰKÖDÉS")
    print("#"*70)
    test_configuration(
        threshold=3, 
        total_locations=5, 
        recovery_locations=3, 
        prime=prime
    )
    
    # TESZT 2: Több helység a visszaállításhoz (threshold = 3, locations = 5, recovery = 4)
    print("\n" + "#"*70)
    print("# TESZT 2: TÖBB HELYSÉG A VISSZAÁLLÍTÁSHOZ")
    print("#"*70)
    test_configuration(
        threshold=3, 
        total_locations=5, 
        recovery_locations=4, 
        prime=prime
    )
    
    # TESZT 3: Magasabb threshold (threshold = 5, locations = 7, recovery = 5)
    print("\n" + "#"*70)
    print("# TESZT 3: MAGASABB THRESHOLD")
    print("#"*70)
    test_configuration(
        threshold=5, 
        total_locations=7, 
        recovery_locations=5, 
        prime=prime
    )
    
    # TESZT 4: HIBAKEZELÉS - Kevesebb helység, mint a threshold
    print("\n" + "#"*70)
    print("# TESZT 4: HIBAKEZELÉS - KEVESEBB HELYSÉG, MINT A THRESHOLD")
    print("#"*70)
    test_configuration(
        threshold=4, 
        total_locations=6, 
        recovery_locations=2,  # Kevesebb mint a threshold!
        prime=prime
    )
    
    # TESZT 5: KRITIKUS ESET - Pont a threshold számú helység
    print("\n" + "#"*70)
    print("# TESZT 5: PONT A THRESHOLD SZÁMÚ HELYSÉG")
    print("#"*70)
    test_configuration(
        threshold=3, 
        total_locations=5, 
        recovery_locations=3,  # Pontosan a threshold
        prime=prime
    )

if __name__ == "__main__":
    main()