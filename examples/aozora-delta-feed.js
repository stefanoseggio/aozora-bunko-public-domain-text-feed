// aozora-delta-feed.js
// Runs the Aozora Bunko New Public-Domain Text Delta Feed actor and logs the resulting dataset items.
// npm install apify-client
const { ApifyClient } = require('apify-client');

// Reads your Apify API token from the environment — never hardcode it in source.
const client = new ApifyClient({
    token: process.env.APIFY_API_TOKEN,
});

// Minimal input matching the actor's real input_schema.json:
// onlyNew:false requests a free baseline run (SNAPSHOT_NO_DIFF, uncharged);
// includeFullText:true asks for decoded plain_text / raw_text_with_markup.
const input = {
    onlyNew: false,
    onlyConfirmedPublicDomain: true,
    includeFullText: true,
    maxItemsPerRun: 25,
};

async function main() {
    // Calls the actor by its Actor ID and waits synchronously for the run to finish.
    const run = await client.actor('K0XRDbUteacQL3jeF').call(input);

    console.log(`Run ${run.id} finished with status: ${run.status}`);

    // Fetches the resulting dataset items — one row per delta event.
    const { items } = await client.dataset(run.defaultDatasetId).listItems();

    console.log(`Fetched ${items.length} dataset item(s):`);
    for (const item of items) {
        console.log(`- [${item.event_type}] ${item.work_id}: ${item.title}`);
    }
}

main().catch((err) => {
    console.error('Run failed:', err);
    process.exitCode = 1;
});
