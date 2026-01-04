import os
import hashlib

def find_and_remove_duplicates(parent_folder):
    hashes = {}
    duplicates_count = 0
    saved_size = 0
    
    print(f"\n--- INICIANDO ESCANEO EN: {parent_folder} ---")

    for dirpath, _, filenames in os.walk(parent_folder):
        for f in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, f))
            
            # Evitar procesar archivos temporales de sistema
            if f.startswith('~$') or f.lower() == 'desktop.ini':
                continue

            try:
                with open(file_path, 'rb') as afile:
                    file_hash = hashlib.md5(afile.read()).hexdigest()
                
                print(f"Analizando: {f} | Hash: {file_hash[:8]}...")

                if file_hash in hashes:
                    size = os.path.getsize(file_path)
                    print(f"¡DUPLICADO ENCONTRADO! Borrando: {f}")
                    os.remove(file_path)
                    duplicates_count += 1
                    saved_size += size
                else:
                    hashes[file_hash] = file_path
            except Exception as e:
                print(f"ERROR con {f}: {e}")

    print(f"--- FIN: {duplicates_count} borrados ---\n")
    return duplicates_count, saved_size