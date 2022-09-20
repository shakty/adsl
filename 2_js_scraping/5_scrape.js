const Nightmare = require('nightmare');
const nightmare = Nightmare();
const cheerio = require('cheerio');
const NDDB = require('NDDB');

// Get database of links.
let db = NDDB.db();
db.loadSync('./links.json');


// Check this checklist!
// https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/

// See also:
// https://www.voidkat.com/nightmarejs-scrapping/

// This article has some advice on concurrent scraping, using proxies, and 
// changing the userAgent to avoid being blocked:
// https://www.zenrows.com/blog/web-scraping-with-javascript-and-nodejs 


// Extract posts from the reddit page.
const getPosts = item => {

    const MAIN_CONTAINER = ".uI_hDmU5GSiudtABRz_37";
    const POST = "._1qeIAgB0cPwnLhDF9XSiJM";

    nightmare
        .goto(item.url)
        .wait(MAIN_CONTAINER)
        .evaluate(() => {
            // Need to define it again because this
            // code is executed inside the headless browser
            // and the context in this page is lost.

            // Likewise console.log() or debugger do not work in here.

            return document.body.innerHTML;

        })
        .then((html) => {

            debugger

            // Creates cheerio representation of the page.
            const $ = cheerio.load(html);

            // Cheerio follows the jQuery syntax, but it does not
            // do a full render of the page, so no dataset object.
            // We need to access the attributes.

            // TODO: grab additional info: user, data, upvotes, etc.
            let posts = $(POST).map((idx, div) => {
                return $(div).text()
            }).toArray();

            // Save posts inside item.
            // We make them a long string now for simplicity, as we 
            // do not collect additional info and evaluate them all
            // together.
            item.posts = posts.join(' ');

            // Tell that fetching succeded.
            scrapeNext(true);
        })
        .catch((error) => {
            console.error('Error:', error)

            // Tell that fetching failed.
            scrapeNext(false);
        });

};

// Close nightmaer and save dataset.
// TODO: sometimes nightmare does not close correctly.
const stopScraping = () => {

    if (verbose) console.log('Scraping ended, saving database.')

    // Close nightmare.
    nightmare.end();

    // Save all posts.
    db.save('reddit.csv', {
        header: 'all'
    });
};

// Start the process of scraping the next item from the database.
// If enough items are scraped, it stops the scraping process.
// Otherwise it recursively call itself to fetch more items.
const scrapeNext = (res) => {

    // TODO: We could enable a re-try mechanism if res is false.

    // Update counter.
    counter++;

    // Get next item.
    let item = db.get(counter);

    // If there are no more items or if we reached the limit,
    // end the scraping.
    if (!item || counter >= LIMIT) {
        stopScraping();
        return;
    }

    if (verbose) console.log('Scraping item ' + counter + ': ' + item.title);

    // Otherwise call getPosts for the current item after a delay.
    // We pass scrapeNext as a callback that will be invoked when scraping
    // of first item is done. We could do scraping concurrently (i.e., 
    // multiple requests at the same time), however this increases the likehood
    // of getting banned by the web site.
    setTimeout(() => getPosts(item, scrapeNext), DELAY);
};


// Max number of items for which posts will be fetched.
const LIMIT = 20;

// Counts number of items fetched.
let counter = -1;

// Number of milliseconds to wait between requests.
const DELAY = 5000;

// Output info to console.
let verbose = true;


// First call 
scrapeNext(true);


