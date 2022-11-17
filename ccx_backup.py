#!/usr/bin/env python
import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Backup Scripts, Prompts, and/or Documents from a UCCX server"
        ),
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        required=True,
        help="UCCX user with admin capabilities",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        required=True,
        help="Password for UCCX admin user",
    )
    parser.add_argument(
        "-ip",
        "--ip_address",
        metavar="aaa.bbb.ccc.ddd",
        type=str,
        required=True,
        help="ip addressor UCCX server",
    )
    parser.add_argument(
        "-b",
        "--backup",
        default="all",
        choices=["all", "scripts", "prompts", "documents"],
        help="what to backup (scripts, prompts, documents or all) default:all",
    )
    # parser.add_argument(
    #     "-o",
    #     "--output_dir",
    #     help=(
    #         "where to save backups, by default a backups directory will be"
    #         " created with a date time stamp"
    #     ),
    # )
    return parser.parse_args()


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
