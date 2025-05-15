from typing import Optional, List
from pathlib import Path
from pydantic.dataclasses import dataclass as pydantic_dataclass
from pydantic import EmailStr, ConfigDict, ValidationError
import pandas as pd
from icecream import ic

# Paths
root_dir = Path(__file__).parent
output_dir = root_dir / "output"
export_dir = root_dir / "export"

# Ken Wise-specific email class
@pydantic_dataclass(config=ConfigDict(str_strip_whitespace=True))
class Email:
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    file_name: str
    email_status: str = 'valid'
    duplicate: Optional[bool] = None

    @classmethod
    def validate_combined_files(cls, file: list[dict]) -> pd.DataFrame:
        ic.configureOutput(prefix='combine.py|', includeContext=False)
    
        if not isinstance(file, list):
            raise ValueError("File must be a list of dictionaries")

        # Convert to Email class
        emails = []
        for row in file:
            _email = row['Email']
            _name = row['Name'] if isinstance(row['Name'], str) else None
            _file_name = row['file_name']
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
                    file_name=_file_name,
                    duplicate=_duplicate,
                )
            except ValidationError:
                email = {
                    'first_name': _first_name,
                    'last_name': _last_name,
                    'email': _email,
                    'file_name': _file_name,
                    'email_status': 'invalid',
                    'duplicate': _duplicate,
                }
            emails.append(email if isinstance(email, dict) else email.__dict__)
        email_df = pd.DataFrame(emails)
        print(f"""VALIDATION REPORT \n{'-'*50} \nEmail status counts: \n{'='*25} \n{email_df['email_status'].value_counts().to_markdown()}
               \nDuplicate counts: \n{'='*25} \n{email_df['duplicate'].value_counts().to_markdown()} \n{'-'*50}""")

        return email_df

