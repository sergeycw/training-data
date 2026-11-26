"""One-time Garmin Connect login: saves tokens for later scripts.

The password is typed by the athlete in the terminal (getpass) and is never
stored. Only the session tokens are saved, to ~/.garminconnect, outside the
repo, so they never reach git. Later scripts call Garmin().login(TOKENSTORE)
without a password. Re-run this script when Garmin rejects the tokens.

Uses the unofficial python-garminconnect library (Garmin has no public API
for workouts). Run with the project venv: .venv-garmin/bin/python.
"""

import getpass
from pathlib import Path

from garminconnect import Garmin

TOKENSTORE = str(Path("~/.garminconnect").expanduser())


def main() -> None:
    email = input("Garmin email: ").strip()
    password = getpass.getpass("Garmin password (not shown): ")
    # MFA: Garmin may send a code by email or app; the library asks for it here.
    api = Garmin(email, password, prompt_mfa=lambda: input("MFA code: ").strip())
    api.login(TOKENSTORE)
    # login() writes tokens but suppresses write errors; dump again so a
    # failed write raises here instead of surfacing later as "needs password".
    api.client.dump(TOKENSTORE)
    print(f"OK: {api.get_full_name()}. Tokens saved to {TOKENSTORE}")


if __name__ == "__main__":
    main()
