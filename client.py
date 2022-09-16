#!/usr/bin/env python3
import socket
import json
import ssl
import argparse

# Put all the words in a list to iterate after.
with open('words.txt') as f:
    words = []
    for line in f:
        words.append(line[:5])


def send(so, msg):
    """Function that sends the message through the socket"""
    msg = bytes(msg, 'utf-8')
    total_sent = 0
    while total_sent < len(msg):
        sent = so.send(msg)
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent = total_sent + sent
    # print(total_sent)


def receive(so):
    """Function that receives the message from the server through the socket.
    *Disclaimer: both functions were inspired by the ones showed by the professor in class"""
    end = False
    mes = ''
    while not end:
        mes = so.recv(1024).decode()
        if mes.endswith('\n'):
            end = True
    # print(mes)
    return mes


def getID(msg):
    """Retrieve the ID of the game"""
    msg = json.loads(msg)
    ID = msg['id']
    return ID


def firstWord(ID, sock):
    """Always start with the same word -according to Google one of the best to start with-"""
    msg = json.dumps({"type": "guess", "id": str(ID), "word": "least"}) + '\n'
    send(sock, msg)
    return 'least'


def compare_words(my_word, words_from_list):
    """This function is used to later discard the words that do not match with the 'marks' obtained from the server"""
    new_marks = []
    posi_not_found = []
    lett_not_in_word = []
    for (i, letter1), letter2 in zip(enumerate(my_word), words_from_list):
        if letter1 == letter2:
            new_marks.append('2')
        else:
            new_marks.append('0')
            posi_not_found.append(i)
            lett_not_in_word.append(letter2)
    for i in posi_not_found:
        if my_word[i] in lett_not_in_word:
            new_marks[i] = "1"
            lett_not_in_word.remove(my_word[i])
    return "".join(new_marks)


def filter_words(word_list, word, marks):
    """Creates a new filtered list, containing only possible words"""
    new_possible_words = []
    for w in word_list:
        if compare_words(word, w) == marks:
            new_possible_words.append(w)
    # print("New words: ", new_possible_words)
    return new_possible_words


def processAnswer(msg, last_word, prev_words):
    """Gets the new word to be used and the list of new words"""
    msg = json.loads(msg)
    guesses = msg['guesses']
    # print(guesses)
    last_try = guesses[-1]
    # print(last_try)
    marks = ''.join(str(e) for e in last_try['marks'])  # Get the marks as a string
    next_words = filter_words(prev_words, last_word, marks)
    return next_words, next_words[0]


def check_end(msg):
    """To end the game in case the type is 'bye'"""
    msg = json.loads(msg)
    mode = msg['type']
    if mode == 'bye':
        return False
    else:
        return True


# Start the game
def main():
    # Get the arguments
    parser = argparse.ArgumentParser(
        usage='./client <-p port> <-s> [hostname] [Northeaster-Username]')
    parser.add_argument('-p', type=int, required=False, dest='port')
    parser.add_argument('-s', action='store_true', required=False,
                        help='if the socket is encrypted with TLS/SSL', dest='ssl')
    parser.add_argument('hostname', type=str)
    parser.add_argument('nuid', type=str, metavar='Northeaster-Username')
    args = parser.parse_args()

    # Initialize the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # If the socket has to be encrypted
    if args.ssl:
        sock = ssl.wrap_socket(sock)

    # Use the port given or default 27993. 27994 for SSL encrypting.
    port = args.port if args.port is not None else (
        27994 if args.ssl else 27993)

    # Connect
    sock.connect((args.hostname, port))

    # Process initial message
    init_msg = json.dumps({"type": "hello", "northeastern_username": str(args.nuid)}) + '\n'
    send(sock, init_msg)

    # Get the first message
    mes = receive(sock)

    # Get the ID and store it
    ID = getID(mes)
    # print(ID)

    # Send the first word and process the answer
    last_word = firstWord(ID, sock)
    answer = receive(sock)
    # print(last_word)

    # Get the second set of words
    next_words, new_word = processAnswer(answer, last_word, words)
    new_msg = json.dumps({"type": "guess", "id": str(ID), "word": str(new_word)}) + '\n'
    last_word = new_word
    send(sock, new_msg)

    # Iterate to choose the following words
    while True:
        answer = receive(sock)
        # print("Answer from server:", answer)
        # Check if it's done
        if not check_end(answer):
            answer = json.loads(answer)
            print(answer['flag'])
            break

        next_words, new_word = processAnswer(answer, last_word, next_words)
        new_msg = json.dumps({"type": "guess", "id": str(ID), "word": str(new_word)}) + '\n'
        send(sock, new_msg)
        last_word = new_word
        # print("Last word used:", last_word)


if __name__ == '__main__':
    main()
