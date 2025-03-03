import os

# Obtener la ruta absoluta de este script
base_dir = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta de la fuente
ruta_fuente = os.path.join(base_dir, "assents","Font", "Minecraft.ttf")

# Comprobar si el archivo existe
if os.path.exists(ruta_fuente):
    print("✅ Archivo encontrado:", ruta_fuente)
else:
    print("❌ Archivo NO encontrado. Revisa la ruta.")
