/////////////////////////////////////////////////
// Welcome to the 1st Exercise Sheet: Warm Up! //
/////////////////////////////////////////////////

// Note: this are the solutions based on the Atom's file. For VS Code
// it's basically the same.

// EXERCISE 1 Indentation.
//////////////////////////

// a. Select all the code below and press TAB. Ta da!
// Did something happened? If not, please check again the slides
// to setup Atom.

let a = 1234;
a++;
if (a > 123) {
    a--;
}
else {
    a++;
}
console.log(a);

// b. Why is it still different from the code indented on the slide (Atom only)?
// Automatic indentation simply adjustes the space on the left-hand
// side of your code. It neither adds missing parentheses nor trims
// white space between words. That is up to you to do it.
// Do it, does it read better? Can you grasp what it is doing?

// This code is pretty silly. It is simply checking if the value of variable
// a is greater than 123, if so, it reduces its value by one unit, else it
// increases by one unit. In the end it prints out the value of variable a.
// In this case a is greater than 123, so the value printed is...(you say it!).

// c. Gossip. Another important (futile) debate among programmers is whether
// spaces or tabs should be used for indentation. Check out this video to
// understand how important spaces (tabs) are:
// https://www.youtube.com/watch?v=SsoOG6ZeyUI
// Or read more here:
// https://thenewstack.io/spaces-vs-tabs-a-20-year-debate-and-now-this-what-the-hell-is-wrong-with-go/


// EXERCISE 2 Linting.
//////////////////////
// Linting can spot your code errors on the fly. As you type them.
// It can also gives you suggestions about to better format and organize
// your code. Pretty useful, isn't it?

// But why this weird name? "Linting?" lint was the name originally given
// to a particular program that flagged some suspicious and non-portable
// constructs (likely to be bugs) in C language code.

// Below is some code with some errors and warnings. Next to the line with
// an error there should be a red dot. If you hover over the line, you will
// get additional information about the error. In addition, all the
//  errors are available in a separate panel at the bottom of the page.

// Start fixing the first error, more errors might pop up, because the first
// error was blocking the execution of the code inspection.

// If you don't know how to fix an error, just comment out the line with //.
// However, for some errors you will find a link with additional
// information about how to fix inside the tooltip, and for others you can
// simply click  a "Fix" button.

// Hint: follow the pattern.
a = 1
let b = 2;
let c = 3;

// Hint: This function has no name following the word function.
function sayHello() {
    console.log('Hello!');
}

// Use b and c and the function sayHello.
sayHello();
console.log('The sum of b and c is: ', b+c);


// EXERCISE 3. Autocompletion.
//////////////////////////////
// Atom comes with snippet auto-completion. Cool! But what is a "snippet" ?
// A snippet is simply a portion of code that you can reuse.
// We haven't learn the syntax of JavaScript, but this is just to show off
// some useful features of the editor.

// a. Auto complete for console.log, On the next line, start typing log.
// A popup window will show up with suggestion, pick the first one.

console.log("As I just said, the sum of b and c is: ", b+c);

// b. Auto complete for a personl note to fix this line of code. Start typing
// fix.

// FIXME: Remember to write smart comments for your silly code.
// FIXME: Remeber also to change the statment if (true) into something else
//        below in Exercise 4, otherwise the linter complains about it.

// c. What are all the other suggestions? Atom collects and indexes all the
// words in the projects and suggest them to you as you type. Sometimes
// annoying, sometimes useful.

// EXERCISE 4. Producticity: Shorcuts and More.
///////////////////////////////////////////////
// Proficient programmers use the mouse as little as possible, and try
// to do everything with the keyboard. It is actually possible to code
// without using the mouse at all, but we are still far from that point.
// Here we learn just a couple of useful shortcuts.

// a. Close this project. Ok, here is the catch 22, you have to do it
// with the mouse. On the files tree on the right, right click on the name
// "js-programming-fundamentals" (or whatever you have called this project)
// and select "Remove Project Folder." Don't worry it won't delete it from
// the file system, just from Atom. Then reopen it using the shortcut
// Ctrl-Shift-A.

// b. Comment out useless code with Ctrl-/. Notice if you applied the
// command multiple times, it will uncomment/comment/uncomment... it.
// let uselessCode = 'I am useless';

// c. Cool. What other shorcuts are available? Here is a shortcut to find
// them all. Ctrl-Shift-P. Look around and remember how to get here,
// we will use it later.

// d. It would great if we could have a clone of ourselves, or even better 
// multiple clones. It turns out that you can do it in VS Code! Highlight
// the word "not". Then press Ctrl-D as many times as needed to highlight
// all the next occurrences of the word "not". At every word "not" there is
// a new cursor, so you can write multiple rows at once. Delete the word "not"
// and replace the explanation mark with a sad face.  Press Esc to eliminate
// multiple cursors.

catchMeIfYouCan1 = 'You did catch me :(';
catchMeIfYouCan2 = 'You did catch me :(';
catchMeIfYouCan3 = 'You did catch me :(';


// EXERCISE 5. Bracket Matching.
////////////////////////////////
// JavaScript wraps blocks of codes in curly brackes: { SOME CODE }.
// A common rookie mistake is to forget to open or close a parenthesis,
// causing an error. Unfortunately, these common mistakes are surprisingly
// difficult to catch for the untrained eye and may cause acute distress
// in the joung JavaScript programmer. To prevent or mitigate this outcome,
// get familiar with the Atom built-in "Bracket Matcher" utility.

// a. Position yourself after the closing curly bracket of the following
// if statement (it is the second parenthesis). In the main menu, select
// Packages/Bracket Matcher/Go To Matching Bracket. Where did the cursor go?

if ((b+c) > 1) {
    console.log("Hei!");
}

// b. That was easy, furthermore Atom alreadys highlights the matching
// parentheses In more complicated cases, you might want to use the
// keyboard shortcut. What is it? You can search for it in the menu of all
// Atom commands. It is also written next to the menu option you just clicked.

// EXERCISE 6. Git.
///////////////////
// You made good progress. It is time to look back at when you started
// this exercise. You were a different person, and so this was a different
// file.

// a. Open the Git Tab on the right and visualize the changes in this file

// b. If you are happy with them "stage" them, that is add them to the index.

// c. Add a proper "commit" message to describe your changes. Be concise.

// d. Good! Your changes are saved. Normally, you would be able to push them
// to GitHub, but we won't do it now. In fact, you might not have the
// permissions, but we will come back to this later.

// EXERCISE 7. Hydrogen.
////////////////////////
// This is the final obstacle between you and beginning Part 1.
// You got to have Hydrogen installed and configured. Follow the instructions
// on the slides and then come back here.

// a. Try to execute the following code by pressing Ctrl-Return on each line.

let outcome = 'Yes, I made it!';
console.log(outcome);

// b. Did it work? If so try to execute multiple lines at once, by selecting
// them all, and then pressing Ctrl-Return.

console.log('I want to say it 10 times:');
for (let i = 0; i < 10; i++) {
    console.log(i+1 + ': ' + outcome);
}
console.log('Mike drop.');


// Congrats. You can now advance to the next exercise!
