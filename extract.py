#!/usr/bin/env python3

import os
import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_emails_from_account(olm_dir, folder, email):
    exclude_patterns = [
            "asana.com",
            "reply",
            "noreply",
            "registration",
            "chime",
            "support@",
            "mailchimp",
            ".calendar",
            "=",
            "-_",
            "mailbox",
            "+",
            "account",
            "fatura",
            "hizmetleri",
            "musteri",
            "marketing@",
            "help@",
            "sales"
        ]


    exclude_dir = [
        "Junk Email",
        "Sync Issues",
    ]

    email_list = []
    path = os.path.join(olm_dir, folder)
    path = os.path.join(path, email)
    # output_file = olmdir_folder_email+".csv"
    output_file = f"{olm_dir}_{folder}_{email}.csv"
    print("Extracting emails from: "+path)
    path = os.path.join(path, "com.microsoft.__Messages")
    folders = os.listdir(path)
    for folder in folders:
        # skip files
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        if folder in exclude_dir:
            print("> Skipping exclude_patternsed folder: "+folder)
            continue
        folder_path = os.path.join(path, folder)
        print("> Looking for: "+folder)
        for filename in os.listdir(folder_path):
            if not filename.endswith(".xml"):
                print(folder_path+"/"+filename+" is not xml")
                continue

            try:
                tree = ET.parse(folder_path+"/"+filename)
            except:
                print(folder_path+"/"+filename+" couldn't parsed")
            finally:
                root = tree.getroot()
                for item in root.iter('emailAddress'):
                    if 'OPFContactEmailAddressAddress' in item.attrib:
                        if any(to_check in item.attrib['OPFContactEmailAddressAddress'].lower() for to_check in exclude_patterns):
                            # Exclude email addresses that match the patterns
                            continue
                        elif any(item.attrib['OPFContactEmailAddressAddress'].lower() in s for s in email_list):
                            # Exclude email addresses that are already in the list
                            continue
                        elif "@" in item.attrib['OPFContactEmailAddressName']:
                            to_append = ";"+item.attrib['OPFContactEmailAddressAddress'].lower()
                            email_list.append(to_append)
                        else:
                            to_append = item.attrib['OPFContactEmailAddressName']+";"+item.attrib['OPFContactEmailAddressAddress'].lower()
                            email_list.append(to_append)

    # make every email unique
    email_list = list(set(email_list))

    f = open("output/" + output_file, "wb")
    #write header
    f.write("Name;Email\n".encode('utf8'))
    f.write("\n".join(email_list).encode('utf8'))
    print("Extracted "+str(len(email_list))+" emails to "+output_file)

def extract_accounts(olm_dir):
    """Extract emails from the OLM directory."""
    print("Extracting emails from OLM...")
    accounts = []
    default_folders = [
        "Local",
        "Accounts",
    ]
    for folder in default_folders:
        files = os.listdir(os.path.join(olm_dir, folder))
        for filename in files:
            if '@' in filename:
                accounts.append({
                "email": filename,
                "folder": folder,
                })
    return accounts

def unzip_olm(olm_file):
    """Unzip the OLM file and extract its contents."""
    if not olm_file.endswith('.olm'):
        print(f"File {olm_file} is not an OLM file.")
        return
    if not os.path.exists(olm_file):
        print(f"File {olm_file} does not exist.")
        return
    if not zipfile.is_zipfile(olm_file):
        print(f"File {olm_file} is not a valid zip file.")
        return
    print(f"Extracting {olm_file}...")
    extract_dir = os.path.splitext(olm_file)[0]
    os.makedirs(extract_dir, exist_ok=True)
    # Unzip the OLM file
    with zipfile.ZipFile(olm_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Extracted {olm_file} to {extract_dir}")
    return extract_dir

def process_olm(olm_file):
    """Main function to extract emails from OLM files."""
    print(f"Extracting emails from {olm_file}...")
    extract_dir = unzip_olm(olm_file)
    if not extract_dir:
        print(f"Failed to extract {olm_file}")
        return
    accounts = extract_accounts(extract_dir)
    for account in accounts:
        print(f"Account: {account}")
        extract_emails_from_account(extract_dir, account['folder'], account['email'])
    

if __name__ == "__main__":
    print("Starting OLM extraction...")
    current_dir = os.getcwd()
    olm_files = [f for f in os.listdir(current_dir) if f.endswith('.olm')]
    if not olm_files or len(olm_files) == 0:
        print("No OLM files found.")
        sys.exit(0)

    # MkDir for output files
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    print("OLM files found:")
    for olm_file in olm_files:
        print(f" - {olm_file}")
        process_olm(olm_file)