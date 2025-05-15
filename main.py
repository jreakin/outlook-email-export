from pathlib import Path
import pandas as pd

from extract import extract_files
from combine import Email, export_dir, output_dir


# Combine all records from all files
frames = []
for file in output_dir.glob("*.csv"):
    data = pd.read_csv(file, sep=';')
    data['file_name'] = Path(file).stem
    frames.append(data)
all_emails = pd.concat(frames).to_dict(orient='records')


df = Email.validate_combined_files(all_emails)
export_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(export_dir / "all_emails.csv", index=False)
df.drop_duplicates(subset=['email']).to_csv(export_dir / "all_emails_unique.csv", index=False)
