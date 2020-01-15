#Wikipedia-Game

- Program takes two strings, a source page and target page, as command line arguments and prints the list of connected links from start to end.

- Given this input for the python pogram:
    python3 wikipedia_game.py "Battlestar Galactica" "Grace Hopper"
    We should get this output:
    Battlestar Galactica -> Kobol -> COBOL -> Grace Hopper

#To run
- clone the repo
- navigate to the src folder
- %python3 -m venv env
- %source env/bin/activate
- %pip3 install -r requirements.txt