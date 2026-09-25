import re

with open(r'C:\Users\DESKTOP\.gemini\antigravity-ide\brain\0c647258-75ad-4bc1-ad44-97da5a8d80f8\scratch\pdf_full_text.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

tables = []
current_table = []
in_table = False

for line in lines:
    line = line.strip()
    if line.startswith('Tabla ') and line[6:].isdigit():
        if in_table:
            tables.append(current_table)
        in_table = True
        current_table = [line]
    elif in_table:
        if line.startswith('Nota:'):
            current_table.append(line)
            tables.append(current_table)
            in_table = False
        elif not line.startswith('PAGE') and not line.startswith('======') and not line.startswith('ESCUELA DE EDUC') and not line.startswith('DIRECCIÓN ACAD') and not line.startswith('Informe Ejecutivo') and not line.startswith('pág.'):
            current_table.append(line)

print(f"Found {len(tables)} tables.")
