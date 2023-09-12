
# All the text that follows a pound sign, that is #, is a comment.
# Whatever follows the double slash on the same line is ignored by
# the computer, it is just for you to read.

# Empty lines are also ignore, obviously.

# Comments are perhaps the most important
# What do programmers write in these comments?
# Imagine yourself opening this file in 2 years. What would you
# like to know in the most concise way possible?

# In this file, comments contain the instructions for the exercises
# as well as useful hints.

# Enough said. Let's begin with understanding how to move around
# in the Visual Studio Code editor.

# I hope you don't get bored. If so, just continue with the exercises
# in the next file at your own pace. You will find the solutions in the
# folder called solutions. Who would expect this?

# EXERCISE 1 Indentation.
#########################

# a. Select all the code below and press the combination of keys to 
# correctly indent your code. What combination? It depends on your 
# operating system! 
# On Windows : Shift + Alt + F
# On Mac : Shift + Option + F
# On Linux : Ctrl + Shift + I

a=1234
a=a+1
if a > 123: 
    a=a-1
else: a=a+1
print(a)


# b. Can you grasp what the code is doing? If not, don't worry you
# will learn it in this course.

# c. Gossip. Another important (futile) debate among programmers is whether
# spaces or tabs should be used for indentation. Check out this video to
# understand how important spaces (tabs) are:
# https:#www.youtube.com/watch?v=SsoOG6ZeyUI
# Or read more here:
# https:#thenewstack.io/spaces-vs-tabs-a-20-year-debate-and-now-this-what-the-hell-is-wrong-with-go/


# EXERCISE 2 Linting.
#
# Linting can spot your code errors on the fly. As you type them.
# It can also gives you suggestions about to better format and organize
# your code. Pretty useful, isn't it?

# But why this weird name? "Linting?" lint was the name originally given
# to a particular program that flagged some suspicious and non-portable
# constructs (likely to be bugs) in C language code.

# Below is some code with some errors and warnings. Below the error
# there should be a red line. If you hover over the line, you will
# get additional information about the error. In addition, all the
# errors are available in a separate panel at the bottom of the page 
# (bottom left, look for an x inside a circle).

# Start fixing the first error, more errors might pop up, because the first
# error was blocking the execution of the code inspection 
# (and of the auto-formatting).

# If you don't know how to fix an error, just comment out the line with #.
# However, for some errors you will find a link with additional
# information about how to fix inside the tooltip, and for others you can
# simply click a "Fix" button.

# Hint: follow the pattern.
a = 1
b = 2
c = 3

# Hint: Check the tooltip.
def not_used():
    print('Hello!')


# EXERCISE 3. Producticity: Shorcuts and More.
#/
# Proficient programmers use the mouse as little as possible, and try
# to do everything with the keyboard. It is actually possible to code
# without using the mouse at all, but we are still far from that point.
# Here we just learn a couple of useful tricks.

# a. Comment out useless code with Ctrl-/. Notice if you applied the
# command multiple times, it will uncomment/comment/uncomment... it.
# uselessCode = 'I am useless'

# c. Cool. What other shorcuts are available? Here is a shortcut to find
# them all. Ctrl-Shift-P. Look around and remember how to get here,
# we will use it later.

# d. It would great if we could have a clone of ourselves, or even better 
# multiple clones. It turns out that you can do it in VS Code! Highlight
# the word "not". Then press Ctrl-D as many times as needed to highlight
# all the next occurrences of the word "not". At every word "not" there is
# a new cursor, so you can write multiple rows at once. Delete the word "not"
# and replace the explanation mark with a sad face. Press Esc to eliminate
# multiple cursors.

catchMeIfYouCan1 = 'You caught me :('
catchMeIfYouCan2 = 'You caught me :('
catchMeIfYouCan3 = 'You caught me :('


# EXERCISE 4. Bracket Matching.
#
# JavaScript wraps blocks of codes in curly brackets: { SOME CODE }.
#
# A common rookie mistake is to forget to open or close a parenthesis,
# causing an error. Unfortunately, these common mistakes are surprisingly
# difficult to catch for the untrained eye and may cause acute distress
# in the joung JavaScript programmer. To prevent or mitigate this outcome,
# get familiar with the VS Code built-in "Bracket Matcher" utility.

# a. Position yourself after the closing curly bracket of the following
# if statement (it is the second parenthesis). Does the opening curly 
# bracket get highlighted?

a = 1
b = 2
c = 3
if (a*2 + (c/(b+1))) > 1:
    print("Hei!")


# b. That was easy. In more complicated cases, you might want to use a
# keyboard shortcut. Yes, but which one? You can search for "Go to bracket"
# in the menu of all VS Code commands. How do you open that menu? If you don't 
# remember, go back to exercise 3.d.

