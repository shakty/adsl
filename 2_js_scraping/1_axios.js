const axios = require('axios'); 

const SEARCH = 'https://redditsearch.io/?term=black-lives-matter&dataviz=false&aggs=false&subreddits=&searchtype=posts&search=true&start=1638699710&end=1638786110&size=100';

// Adapted from: https://www.zenrows.com/blog/web-scraping-with-javascript-and-nodejs

// First Step: get the whole page.
//////////////////////////////////

axios.get(SEARCH) 
    .then(({ data }) => console.log(data));


// Second Step: get the links.
//////////////////////////////

// Does it work? Why?

// const cheerio = require('cheerio');

// const SELECTOR = ".submission";

// const extractLinks = $ => [ 
//     ...new Set( 
//         $(SELECTOR) // Select pagination links 
//             .map((_, div) => console.log($(div).dataset.link)) // Extract the link 
//             .toArray() // Convert cheerio object to array 
//     ), 
// ]; 

// axios.get(SEARCH).then(({ data }) => { 
// 	const $ = cheerio.load(data);     
// 	const links = extractLinks($); 

// 	console.log(links); 
// 	// ['https://scrapeme.live/shop/page/2/', 'https://scrapeme.live/shop/page/3/', ... ] 
// });