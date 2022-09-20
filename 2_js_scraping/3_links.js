const Nightmare = require('nightmare');
const nightmare = Nightmare();


const SEARCH = 'https://redditsearch.io/?term=black-lives-matter&dataviz=false&aggs=false&subreddits=&searchtype=posts&search=true&start=1638699710&end=1638786110&size=100';


const SELECTOR = ".submission";

// Used to store and save links.
const NDDB = require('NDDB');

nightmare
    .goto(SEARCH)
    .wait(SELECTOR)
    .evaluate(() => {
        // Return the whole page.
        return document.body.innerHTML;

    })
    .end()
    .then((html) => {

        // Creates cheerio representation of the page.
        const $ = cheerio.load(html);

        // Cheerio follows the jQuery syntax, but it does not
        // do a full render of the page, so no dataset object.
        // We need to access the attributes.

        let links = $(SELECTOR).map((idx, div) => {

            // Makes it a jQuery object.
            let d = $(div);
            let link = d.attr('data-link');

            let title = d.find('.title').text();
            let subreddit = d.find('.subreddit').text();
            let author = d.find('.author').text();

            return {
                url: link,
                title: title,
                subreddit: subreddit,
                author: author,
                // When did we fetch this url?
                urlTimestamp: Date.now()
            };

        }).toArray();

        // console.log(links);

        // Save them for later.
        NDDB.save(links, 'links.json');

    })
    .catch((error) => {
        console.error('Error:', error)
    });





