import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Backup Scripts, Prompts, and/or Documents from a UCCX server"
        ),
    )
    optional = parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "-u",
        "--user",
        type=str,
        required=True,
        help="UCCX user with admin capabilities",
    )
    required.add_argument(
        "-p",
        "--password",
        type=str,
        required=True,
        help="Password for UCCX admin user",
    )
    required.add_argument(
        "-ip",
        "--ip_address",
        metavar="aaa.bbb.ccc.ddd",
        type=str,
        required=True,
        help="ip addressor UCCX server",
    )
    optional.add_argument(
        "-b",
        "--backup",
        default="all",
        choices=["all", "script", "prompt", "document"],
        help="what to backup (scripts, prompts, documents or all) default:all",
    )
    optional.add_argument(
        "-o",
        "--output_dir",
        help=(
            "where to save backups, by default a backups directory will be"
            " created with a date time stamp"
        ),
    )
    parser._action_groups.append(optional)
    return parser.parse_args()
