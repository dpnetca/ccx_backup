#!/usr/bin/env python

import json
from datetime import datetime
from pathlib import Path

from cli_parser import parse_args


class CcxServer:
    def __init__(self, user, password, ip) -> None:
        self.user = user
        self.password = password
        self.base_url = f"https://{ip}/adminapi"

    def backup(self, backup_root_dir, resource):
        self.backup_root_dir = backup_root_dir
        file_list = self._get_file_list(resource)
        self._download_files(resource, file_list)

    def _get_file_list(self, resource):
        # url = f"{self.base_url}/{resource}"
        # print("GET ", url)

        with open("sample-list.json", "r") as f:
            json_data = f.read()
        data = self._parse_file_list(resource, json.loads(json_data))

        return data

    def _download_files(self, resource, path_list):
        for path in path_list:
            self._download_file(resource, path)

    def _download_file(self, resource, path):
        bu_path = self.backup_root_dir + path
        Path(bu_path).parents[0].mkdir(parents=True, exist_ok=True)

        url = f"{self.base_url}/{resource}/download/{path}"
        print("GET ", url)

    # Need to remove this and rebuild, using different endpoint results
    @staticmethod
    def _parse_file_list(resource, data):
        if resource == "prompts":
            key = "Prompt"
        elif resource == "scripts":
            key = "Script"
        file_list = [x["Path"] for x in data[key]]
        return file_list


def main():
    args = parse_args()
    ccx = CcxServer(args.user, args.password, args.ip_address)

    now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    backup_root_folder = "backup-" + now
    Path(backup_root_folder).mkdir()

    if args.backup in ["all", "scripts"]:
        ccx.backup(backup_root_folder, " scripts")
    if args.backup in ["all", "prompts"]:
        ccx.backup(backup_root_folder, "prompts")
    if args.backup in ["all", "documents"]:
        ccx.backup(backup_root_folder, "documents")


if __name__ == "__main__":
    main()
