#!/usr/bin/env python

import argparse


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
    parser.add_argument(
        "-o",
        "--output_dir",
        help=(
            "where to save backups, by default a backups directory will be"
            " created with a date time stamp"
        ),
    )
    return parser.parse_args()


class CcxServer:
    def __init__(self, user, password, ip) -> None:
        self.user = user
        self.password = password
        self.base_url = f"https://{ip}/adminapi"

    def backup_scripts(self):
        print("backup scripts")
        self._backup("scripts")

    def backup_prompts(self):
        print("backup prompts")

    def backup_documents(self):
        print("backup documents")

    def _backup(self, resource):
        file_list = self._get_file_list(resource)
        self._download_files(resource, file_list)

    def _get_file_list(self, resource):
        url = f"{self.base_url}/{resource}"
        print("GET ", url)
        return ["aaa", "bbb"]

    def _download_files(self, resource, path_list):
        for path in path_list:
            self._download_file(resource, path)

    def _download_file(self, resource, path):
        url = f"{self.base_url}/{resource}/download/{path}"
        print("GET ", url)


def main():
    args = parse_args()
    ccx = CcxServer(args.user, args.password, args.ip_address)

    # Implement backup folder name selector....

    if args.backup in ["all", "scripts"]:
        ccx.backup_scripts()
    if args.backup in ["all", "prompts"]:
        ccx.backup_prompts()
    if args.backup in ["all", "documents"]:
        ccx.backup_documents()


if __name__ == "__main__":
    main()
