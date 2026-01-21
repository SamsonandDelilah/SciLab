import numpy as np
import re
from decimal import Decimal
from gmpy2 import mpfr, const_pi

def GradToRadians(x):
    """
    Konvertiert Winkelangaben in Radianten.

    Unterstützte Eingabeformate:
    - Dezimalgrad (float, int, Decimal, BigFloat)
    - DMS-Format als String (z.B. "180°34'12''")
    - Wissenschaftliche Notation als String oder Zahl (z.B. "2.3456e1", 2.3456e1)

    :param x: Der Winkel, der konvertiert werden soll. Entweder ein numerischer Wert oder ein String.
    :return: Der Winkel in Radianten oder None bei Fehler.
    """
    error_message = None  # Variable für die Fehlermeldung
    try:
        # Überprüfen, ob die Eingabe ein unterstützter numerischer Typ ist
        if isinstance(x, (int, float, Decimal, mpfr)):
            # Umwandlung in float für die Radianten-Konvertierung
            if isinstance(x, mpfr):
                decimal_value = x  # BigFloat in float konvertieren
            elif isinstance(x, Decimal):
                decimal_value = mpfr(str(x))   # Decimal in float konvertieren
            else:
                decimal_value = mpfr(x)           # Direkte float oder int-Nutzung
                
            # Rückgabe in Radianten (mpfr mit hoher Präzision)
            radians = decimal_value * const_pi() / mpfr('180')
            return radians

        # Überprüfen auf ein DMS-Format oder wissenschaftliche Notation im String-Format
        elif isinstance(x, str):
            dms_pattern = r"^(-?\d+)°(\d+)'(\d+)''$"  # Regex für DMS-Format
            scientific_pattern = r"^(-?\d+(?:\.\d+)?e[+-]?\d+)$"  # Regex für wissenschaftliche Notation
            
            # Überprüfen, ob das Eingabemuster DMS entspricht
            match_dms = re.match(dms_pattern, x)
            # Überprüfen, ob das Eingabemuster der wissenschaftlichen Notation entspricht
            match_scientific = re.match(scientific_pattern, x)

            if match_dms:
                # DMS Extraktion
                grad = int(match_dms.group(1))                  # Grad extrahieren
                minuten = int(match_dms.group(2))                # Minuten extrahieren
                sekunden = int(match_dms.group(3))               # Sekunden extrahieren
                decimal_grad = grad + (minuten / 60) + (sekunden / 3600)
                # Umrechnung in Dezimalgrad, # Rückgabe des Wertes in Radianten
                return mpfr(decimal_grad) * const_pi() / mpfr('180')  # mpfr statt np.radians!

                
            elif match_scientific:
                # Konvertierung von wissenschaftlicher Notation in float
                return mpfr(x) * const_pi() / mpfr('180')  # mpfr statt float
                
            else:
                error_message = f"Ungültiges Format: '{x}'.\nBitte verwende 'Grad°Minuten'Sekunden'' oder wissenschaftliche Notation.\n"
        
        else:
            error_message = "Eingabe muss entweder ein numerisch oder eine Zeichenkette sein.\n"
    
    except Exception as e:  # Fängt alle Arten von Fehlern ab
        error_message = str(e)  # Speichere die Fehlermeldung
    
    if error_message:
        print(error_message)  # Gebe die Fehlermeldung aus
        return None  # Rückgabe von None bei Fehler

def RadiansToGrad(x):
    """
    Konvertiert Winkelangaben von Radianten in Grad.
    
    Unterstützte Eingabeformate:
    - Dezimalradianten (float, int, Decimal, mpfr)
    - DMS-Format als String (wird zu Radianten konvertiert)
    - Wissenschaftliche Notation als String oder Zahl
    
    :param x: Der Winkel in Radianten. Numerischer Wert oder String.
    :return: Der Winkel in Grad (mpfr) oder None bei Fehler.
    """
    error_message = None
    try:
        # Numerische Typen
        if isinstance(x, (int, float, Decimal, mpfr)):
            if isinstance(x, mpfr):
                radian_value = x
            elif isinstance(x, Decimal):
                radian_value = mpfr(str(x))
            else:
                radian_value = mpfr(x)
            
            # Umrechnung: grad = radian * 180 / π
            grad = radian_value * mpfr('180') / const_pi()
            return grad

        # String Verarbeitung (DMS → Radiant → Grad)
        elif isinstance(x, str):
            dms_pattern = r"^(-?\d+)°(\d+)'(\d+)''$"
            scientific_pattern = r"^(-?\d+(?:\.\d+)?[eE][+-]?\d+)$"
            
            match_dms = re.match(dms_pattern, x)
            match_scientific = re.match(scientific_pattern, x)

            if match_dms:
                # Bereits in Grad → direkt zurückgeben
                grad = int(match_dms.group(1))
                minuten = int(match_dms.group(2))
                sekunden = int(match_dms.group(3))
                dezimal_grad = grad + (minuten / 60) + (sekunden / 3600)
                return mpfr(dezimal_grad)
                
            elif match_scientific:
                # Wissenschaftliche Notation → Radiant → Grad
                return mpfr(x) * mpfr('180') / const_pi()
                
            else:
                error_message = f"Ungültiges Format: '{x}'.\nVerwende Radianten oder DMS.\n"
        
        else:
            error_message = "Eingabe muss numerisch oder String sein."
    
    except Exception as e:
        error_message = str(e)
    
    if error_message:
        print(error_message)
        return None


# Beispiele zur Verwendung der Funktion
result = GradToRadians("180")
if result is not None:
    s = result * 34
else:
    print("Berechnung kann nicht durchgeführt werden.")

# Weitere Beispiele
print(GradToRadians(180.57))               # Beispiel mit Dezimalgrad
print(GradToRadians("180°20'13''"))        # Beispiel mit DMS
print(GradToRadians("2.3456e1"))            # Beispiel mit wissenschaftlicher Notation
print(GradToRadians(mpfr("180.57")) )              # Beispiel mit Dezimalgrad

print("Radians\n")

print(RadiansToGrad(np.pi))              # π → 180° (mpfr)
print(RadiansToGrad(mpfr('3.1415926535', 128)))  # Hohe Präzision
print(RadiansToGrad("1.234e1"))          # Wissenschaftlich → Grad
print(RadiansToGrad("180°20'13''"))      # DMS → Grad (direkt)
