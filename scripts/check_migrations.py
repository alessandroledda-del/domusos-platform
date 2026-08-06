from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
model_apps = []
missing = []
for model_file in sorted((root / 'backend/apps').glob('*/models.py')):
    text = model_file.read_text(encoding='utf-8')
    if 'models.Model' not in text and 'AbstractUser' not in text:
        continue
    app = model_file.parent.name
    model_apps.append(app)
    migration = model_file.parent / 'migrations' / '0001_initial.py'
    if not migration.exists():
        missing.append(app)

if missing:
    print('Migrazioni iniziali mancanti: ' + ', '.join(missing))
    sys.exit(1)
print(f'Migrazioni presenti per {len(model_apps)} app: ' + ', '.join(model_apps))
