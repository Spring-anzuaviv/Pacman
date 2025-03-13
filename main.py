import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.game import *
os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    game = Game()
    game.run()

main()