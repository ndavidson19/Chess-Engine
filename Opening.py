import chess as ch
import chess.polyglot as polyglot

with polyglot.open_reader("Human.bin") as reader:
    for entry in reader.find_all(ch.Board()):
        print(entry.move)