from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

TEMPLATES = [
    ("harassment", "Someone is sending repeated abusive messages and threats on {platform}."),
    ("blackmail", "A person is demanding money and threatening to leak private photos tonight on {platform}."),
    ("hacking", "My account had an unauthorized login and the password recovery phone was changed."),
    ("impersonation", "A fake profile is using my photo and pretending to be me on {platform}."),
    ("doxxing", "My address and phone number were posted publicly and people are threatening me."),
    ("financial_fraud", "I sent money through a wallet transaction and the seller disappeared."),
]
PLATFORMS = ["facebook", "whatsapp", "telegram", "gmail", "instagram", "marketplace"]
LOCATIONS = ["Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna", "Barishal"]
SUSPECTS = ["@shadow_user", "@fakeprofile", "+880-demo-1", "unknown-login", "seller-452", "@serial_abuser"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=50)
    parser.add_argument("--output", default="data/demo/synthetic_cases.csv")
    args = parser.parse_args()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["case_id", "label", "statement", "location", "platform", "suspect_identifier", "evidence_name"])
        for i in range(args.rows):
            label, template = random.choice(TEMPLATES)
            platform = random.choice(PLATFORMS)
            suspect = random.choice(SUSPECTS)
            wr.writerow([
                f"synthetic_{i+1:04d}", label, template.format(platform=platform),
                random.choice(LOCATIONS), platform, suspect, f"evidence_{i+1}.txt",
            ])
    print(f"Wrote {args.rows} synthetic cases to {path}")


if __name__ == "__main__":
    main()
