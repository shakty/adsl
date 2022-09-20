const Nightmare = require('nightmare');
const nightmare = Nightmare();
const cheerio = require('cheerio');
const NDDB = require('NDDB');

// Load database of links.
let db = NDDB.db();
db.loadSync('./links.json');

// Get first link.
let link = db.first();
// console.log(link);

// Main container of first post and replies.
const MAIN_CONTAINER = ".uI_hDmU5GSiudtABRz_37";

// Posts inside main container.
const POST = "._1qeIAgB0cPwnLhDF9XSiJM";

nightmare
    .goto(link.url)
    .wait(MAIN_CONTAINER)
    .evaluate(() => {
        // Need to define it again because this
        // code is executed inside the headless browser
        // and the context in this page is lost.

        // Likewise console.log() or debugger do not work in here.

        return document.body.innerHTML;

    })
    .end()
    .then((html) => {

        // Creates cheerio representation of the page.
        const $ = cheerio.load(html);

        // Cheerio follows the jQuery syntax, but it does not
        // do a full render of the page, so no dataset object.
        // We need to access the attributes.

        // TODO: grab additional information, such as user, data, upvotes, etc.
        let posts = $(POST).map((idx, div) => {
            return $(div).text()
        }).toArray();

        console.log(posts);
    })
    .catch((error) => {
        console.error('Error:', error)
    });




