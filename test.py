import os

def print_directory_tree(startpath, prefix=""):
    # Hole alle Verzeichnisse und Dateien in dem aktuellen Verzeichnis
    entries = os.listdir(startpath)
    # Sortiere die Einträge
    entries.sort()
    
    for index, entry in enumerate(entries):
        path = os.path.join(startpath, entry)
        # Prüfe, ob es ein Verzeichnis ist
        if os.path.isdir(path):
            # Erstelle eine Verbindung für die Baumstruktur (letztes Element oder nicht)
            connector = "└── " if index == len(entries) - 1 else "├── "
            print(prefix + connector + entry)
            # Berechne den neuen Präfix für die Sub-Ordner
            print_directory_tree(path, prefix + ("    " if connector == "└── " else "│   "))
        else:
            # Bei Dateien die Namen direkt ausgeben
            connector = "└── " if index == len(entries) - 1 else "├── "
            print(prefix + connector + entry)

def main():
    folder_path = r"I:\Git\scilib"  # Ändere dies auf den gewünschten Ordner
    print_directory_tree(folder_path)

if __name__ == "__main__":
    main()

    
   