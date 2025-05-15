import csv
from typing import Optional
from pathlib import Path
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic import EmailStr, ConfigDict
import pandas as pd

root_dir = Path(__file__).parent
output_dir = root_dir / "output"

@pydantic_dataclass(config=ConfigDict(str_strip_whitespace=True))
class Email:
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    file_name: str
    email_status: str = 'valid'
    duplicate: Optional[bool] = None

frames = []
for file in output_dir.glob("*.csv"):
    data = pd.read_csv(file, sep=';')
    data['file_name'] = Path(file).stem
    frames.append(data)
all_emails = pd.concat(frames).to_dict(orient='records')

emails = []
for email in all_emails:
    _email = email['Email']
    _name = email['Name'] if isinstance(email['Name'], str) else None
    if _name:
        _split = _name.split(' ')
        if len(_split) == 1:
            _first_name = _split[0]
            _last_name = None
        else:
            _first_name = _split[0]
            _last_name = _split[1]
    else:
        _first_name = None
        _last_name = None

    _duplicate = True if _email in [e['email'] for e in emails] else None

    try:
        email = Email(
            first_name=_first_name,
            last_name=_last_name,
            email=_email,
            file_name=Path(file).name,
            duplicate=_duplicate,
        )
    except:
        email = {
            'first_name': _first_name,
            'last_name': _last_name,
            'email': _email,
            'file_name': Path(file).name,
            'email_status': 'invalid',
            'duplicate': _duplicate,
        }
    emails.append(email if isinstance(email, dict) else email.__dict__)

df = pd.DataFrame(emails)
print(df['email_status'].value_counts().to_markdown())
print(df['duplicate'].value_counts().to_markdown())
df.to_csv(output_dir/ "all_emails.csv", index=False)
df.drop_duplicates(subset=['email']).to_csv(output_dir/ "all_emails_unique.csv", index=False)

# print("File counts ", all_emails['file_name'].value_counts().to_markdown())
# print("Total emails ", _all := len(all_emails))
# print("Duplicates ", _dup := len(all_emails.drop_duplicates(subset=['Email'])))
# print("Unique emails ", _uniq := len(all_emails) - _dup)
# print("Duplicates percentage ", _dup / _all)

# print(emails)   