# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from KeyManager import KeyManager
from Node import Node
import random
import string
import pyaes


if __name__ == '__main__':
    key_manager = KeyManager()
    A = Node()
    B = Node()
    A.input_op_mode(key_manager, B)
    B.show_decryption()



