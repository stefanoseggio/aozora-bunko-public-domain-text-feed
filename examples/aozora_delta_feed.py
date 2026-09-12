"""
aozora_delta_feed.py
Runs the Aozora Bunko New Public-Domain Text Delta Feed actor and prints the resulting dataset items.
pip install apify-client
"""
import os
import sys

from apify_client import ApifyClient

# Reads your Apify API token from the environment — never hardcode it in source.
client = ApifyClient(os.environ["APIFY_API_TOKEN"])

# Minimal input matching the actor's real input_schema.json:
# onlyNew=False requests a free baseline run (SNAPSHOT_NO_DIFF, uncharged);
# includeFullText=True asks for decoded plain_text / raw_text_with_markup.
run_input = {
    "onlyNew": False,
    "onlyConfirmedPublicDomain": True,
    "includeFullText": True,
    "maxItemsPerRun": 25,
}


def main() -> None:
    # Calls the actor by its Actor ID and waits synchronously for the run to finish.
    run = client.actor("K0XRDbUteacQL3jeF").call(run_input=run_input)

    print(f"Run {run['id']} finished with status: {run['status']}")

    # Fetches the resulting dataset items — one row per delta event.
    dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

    print(f"Fetched {len(dataset_items)} dataset item(s):")
    for item in dataset_items:
        print(f"- [{item['event_type']}] {item['work_id']}: {item['title']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Run failed: {exc}", file=sys.stderr)
        sys.exit(1)
