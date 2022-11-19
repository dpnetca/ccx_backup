#!/usr/bin/env python

from datetime import datetime
from pathlib import Path
from typing import List

import requests

# surpresssing certificate warnings, bad idea, but probably required for this
from urllib3.exceptions import InsecureRequestWarning

from cli_parser import parse_args

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class CcxServer:
    """CcxServer class to group backup tasks together, probably not
    really needed but it's here.

    """

    def __init__(self, user: str, password: str, ip: str) -> None:
        self.user = user
        self.password = password
        self.base_url = f"https://{ip}/adminapi"
        self.verify_cert = False  # bad idea but required for this

    def backup(self, backup_root_dir: str, resource: str) -> None:
        """backup method is the only method that should be directly called
        it will trigger a few subsequent flows to backup all sepcified files

        Args:
            backup_root_dir (string): directory to store backups
            resource (string): resource being backed up (prompt, script,
                 or document)
        """
        self.backup_root_dir = backup_root_dir
        file_list = self._get_file_list(resource)
        self._download_files(resource, file_list)

    def _get_file_list(self, resource: str, path="/") -> List[str]:
        """call the api endpoint to get list of files recurively search
        through folders and parse the responses to generate and return
        a list of files with their folder path

        Args:
            resource (string): resource type being queried
            path (str, optional): path to query, used for recursive lookups.
                Defaults to "/".

        Returns:
            list: list of file paths
        """
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

    def _download_files(self, resource: str, path_list: List[str]) -> None:
        """loop over file list and call function to download each file

        Args:
            resource (str): resource being downloaded
            path_list (list): list of files with path
        """
        for path in path_list:
            self._download_file(resource, path)

    def _download_file(self, resource: str, path: str) -> None:
        """download and save each file

        Args:
            resource (str): resource being downloaded
                 (prompt string or document)
            path (stt): file path to file
        """
        bu_path = f"{self.backup_root_dir}/{resource}{path}"
        Path(bu_path).parent.mkdir(parents=True, exist_ok=True)

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

    # initialize the ccxserver class object with CLI passed arguments
    ccx = CcxServer(args.user, args.password, args.ip_address)

    # create backup root directory bsaed on passed argument or date-time stamp
    if args.output_dir:
        backup_root_folder = args.output_dir
    else:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_root_folder = "backup-" + now
    Path(backup_root_folder).mkdir()

    # if backing up all then call each otherwise call specific resource,
    # probaably a cleaner way to do this
    if args.backup in ["all", "script"]:
        ccx.backup(backup_root_folder, "script")
    if args.backup in ["all", "prompt"]:
        ccx.backup(backup_root_folder, "prompt")
    if args.backup in ["all", "document"]:
        ccx.backup(backup_root_folder, "document")


if __name__ == "__main__":
    main()
