## Project 1: Socket Basics

### Description
Implement a client program that plays a variant of the recently-popular game Wordle. The program will make guesses for the secret word, and the server will give you information about how close your guess is. Once the client correctly guesses the word, the server will return a secret flag.

### Approach
For the server connection, I created two basic functions. The _send_ function just sends the message through the socket and stores the sent bytes. On the contrary, the _receive_ function gets the message from the server and stores it in a variable. Both functions are used to communicate with the server and be able to implement the game algorithm.
Next, for the Wordle part I store the ID from the server that will be used for the current game. In my approach I decided to always use the same word for the first try, in this case ‘least’ as according to Google it was a desirable choice.
The game algorithm works with two main functions that are repeated until the correct word is found. The function _compare_words_ gets the given word and compares it to all the words from the word list being used for that try. Iterates through all the letters just checking if they are the same, if they are, it adds a 2 to the new marks (later used to compare to the given ones by the server), however, if they are not the same they get added to a list of letters not in the word to later filter all the words, finally, if the word has one of those letters, the mark gets changed to a 1 and removed from the missing letters list. Then the function _filter_words_ checks all the words in the current list and compares them to the marks received from the server. If they follow the pattern, that word gets added to the next word list.
Finally, the algorithm will iterate until it gets the final word, printing the obtained flag. 

### Challenges and difficulties
The most challenging thing for this project was learning how to work with the Khoury Machine. Coming as an exchange student and taking a high-level class like this is difficult since everyone in the class is supposed to know all these basic things from previous years. After finding out how to work with that, learning about sockets was not as difficult as I thought. At first, I was a bit lost but with some YouTube tutorials and a lot of research I figured. For the algorithm to solve the problem I exchanged ideas with a few of my classmates and together we managed to get a result. 

### Testing and debugging
I tested the code using trial and error until I got the flag each time I ran it. I have not focused on the performance much since I am not used to working with the terminal and sometimes it was hard to handle all the stuff there. Nevertheless, I got the result in about 3-8 tries every time being surprisingly consistent. 