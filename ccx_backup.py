#!/usr/bin/env python

from datetime import datetime
from pathlib import Path
import requests
from cli_parser import parse_args
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class CcxServer:
    def __init__(self, user, password, ip) -> None:
        self.user = user
        self.password = password
        self.base_url = f"https://{ip}/adminapi"
        self.verify_cert = False

    def backup(self, backup_root_dir, resource):
        self.backup_root_dir = backup_root_dir
        file_list = self._get_file_list(resource)
        self._download_files(resource, file_list)

    def _get_file_list(self, resource, path="/"):
        url = f"{self.base_url}/{resource}{path}"
        headers = {"Accept": "application/json"}
        res = requests.get(
            url,
            headers=headers,
            auth=(self.user, self.password),
            verify=self.verify_cert,
        )
        data = res.json()
        file_list = []
        key = resource.title()
        if data[key].get("Folder"):
            for folder in data[key]["Folder"]:
                file_list.extend(
                    self._get_file_list(
                        resource, folder["path"] + folder["FolderName"] + "/"
                    )
                )
        if data[key].get("File"):
            for file in data[key]["File"]:
                file_list.append(file["path"] + file["FileName"])
        return file_list

    def _download_files(self, resource, path_list):
        for path in path_list:
            self._download_file(resource, path)

    def _download_file(self, resource, path):
        bu_path = f"{self.backup_root_dir}/{resource}{path}"
        Path(bu_path).parents[0].mkdir(parents=True, exist_ok=True)

        url = f"{self.base_url}/{resource}/download{path}"
        headers = {"Accept": "application/json"}
        res = requests.get(
            url,
            headers=headers,
            auth=(self.user, self.password),
            verify=self.verify_cert,
        )
        with open(bu_path, "wb") as f:
            f.write(res.content)


def main():
    args = parse_args()
    ccx = CcxServer(args.user, args.password, args.ip_address)

    if args.output_dir:
        backup_root_folder = args.output_dir
    else:
        now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        backup_root_folder = "backup-" + now
    Path(backup_root_folder).mkdir()

    if args.backup in ["all", "script"]:
        ccx.backup(backup_root_folder, "script")
    if args.backup in ["all", "prompt"]:
        ccx.backup(backup_root_folder, "prompt")
    if args.backup in ["all", "document"]:
        ccx.backup(backup_root_folder, "document")


if __name__ == "__main__":
    main()
