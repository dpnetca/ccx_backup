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
        choices=["all", "script", "prompt", "document"],
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
