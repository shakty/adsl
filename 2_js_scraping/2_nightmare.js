const Nightmare = require('nightmare');
const nightmare = Nightmare();


const SEARCH = 'https://redditsearch.io/?term=black-lives-matter&dataviz=false&aggs=false&subreddits=&searchtype=posts&search=true&start=1638699710&end=1638786110&size=100';


const SELECTOR = ".submission";

// Option 1. Manipulation inside the headless browser.
//////////////////////////////////////////////////////

nightmare
    .goto(SEARCH)
    .wait(SELECTOR)
    .evaluate(() => {

        // Need to define SELECTOR  again because this
        // code will run inside the headless browser
        // and the context of this page is lost.
        
        // Likewise, console.log() or debugger will not work here.
        
        const SELECTOR = ".submission"; 

        // We use standard browser API.

        let posts = document.querySelectorAll(SELECTOR);
        
        let links = Array.from(posts).map(p => {
            return p.dataset.link;
        });

        return links;
    })
    .end()
    .then((links) => {
        console.log('Links', links)
    })
    .catch((error) => {
        console.error('Error:', error)
    })



// Option 2. Manipulation inside the Node.JS process (better for debugging).
////////////////////////////////////////////////////////////////////////////

   // const cheerio = require('cheerio');

    // nightmare
    // .goto(SEARCH)
    // .wait(SELECTOR)
    // .evaluate(() => {
    
    //     return document.body.innerHTML;
        
    // })
    // .end()
    // .then((html) => {
     
    //     // Creates cheerio representation of the page.
    //     const $ = cheerio.load(html);  

    //     // Cheerio follows the jQuery syntax, but it does not
    //     // do a full render of the page, so no dataset object.
    //     // We need to access the attributes.
        
    //     let links  = $(SELECTOR).map((idx, div) => {
    //         return $(div).attr('data-link');
    //     }).toArray();

    //     // links = Array.from(links).map(d => d.dataset.link);
    //     console.log(links);
        
    // })
    // .catch((error) => {
    //     console.error('Error:', error)
    // });




            