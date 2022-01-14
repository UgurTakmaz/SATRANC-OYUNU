import pygame
import chess
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy

pygame.init()

SQUARE_SIDE = 50
AI_SEARCH_DEPTH = 2

RED_CHECK = (240, 150, 150)
BEYAZ = (255, 255, 255)
BLUE_LIGHT = (140, 184, 219)
BLUE_DARK = (91, 131, 159)
GRAY_LIGHT = (240, 240, 240)
GRAY_DARK = (200, 200, 200)
CHESSWEBSITE_LIGHT = (212, 202, 190)
CHESSWEBSITE_DARK = (100, 92, 89)
LICHESS_LIGHT = (240, 217, 181)
LICHESS_DARK = (181, 136, 99)
LICHESS_GRAY_LIGHT = (164, 164, 164)
LICHESS_GRAY_DARK = (136, 136, 136)

BOARD_renkS = [(GRAY_LIGHT, GRAY_DARK),
                (BLUE_LIGHT, BLUE_DARK),
                (BEYAZ, BLUE_LIGHT),
                (CHESSWEBSITE_LIGHT, CHESSWEBSITE_DARK),
                (LICHESS_LIGHT, LICHESS_DARK),
                (LICHESS_GRAY_LIGHT, LICHESS_GRAY_DARK)]
BOARD_renk = choice(BOARD_renkS)

SIYAH_SAH = pygame.image.load('resimler/SIYAH_SAH.png')
SIYAH_VEZIR = pygame.image.load('resimler/SIYAH_VEZIR.png')
SIYAH_KALE = pygame.image.load('resimler/SIYAH_KALE.png')
SIYAH_FIL = pygame.image.load('resimler/SIYAH_FIL.png')
SIYAH_AT = pygame.image.load('resimler/SIYAH_AT.png')
SIYAH_PIYON = pygame.image.load('resimler/SIYAH_PIYON.png')
SIYAH_JOKER = pygame.image.load('resimler/SIYAH_joker.png')

BEYAZ_SAH = pygame.image.load('resimler/BEYAZ_SAH.png')
BEYAZ_VEZIR = pygame.image.load('resimler/BEYAZ_VEZIR.png')
BEYAZ_KALE = pygame.image.load('resimler/BEYAZ_KALE.png')
BEYAZ_FIL = pygame.image.load('resimler/BEYAZ_FIL.png')
BEYAZ_AT = pygame.image.load('resimler/BEYAZ_AT.png')
BEYAZ_PIYON = pygame.image.load('resimler/BEYAZ_PIYON.png')
BEYAZ_JOKER = pygame.image.load('resimler/BEYAZ_joker.png')

CLOCK = pygame.time.Clock()
CLOCK_TICK = 15

SCREEN = pygame.display.set_mode((8 * SQUARE_SIDE, 8 * SQUARE_SIDE), pygame.RESIZABLE)
SCREEN_TITLE = 'UĞUR-OMER SATRANÇ OYUNU'

pygame.display.set_icon(pygame.image.load('resimler/chess_icon.ico'))
pygame.display.set_caption(SCREEN_TITLE)


def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode((8 * square_side_len, 8 * square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len


def print_empty_board():
    SCREEN.fill(BOARD_renk[0])
    paint_dark_squares(BOARD_renk[1])


def paint_square(square, square_renk):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_renk, (SQUARE_SIDE * col, SQUARE_SIDE * row, SQUARE_SIDE, SQUARE_SIDE), 0)


def paint_dark_squares(square_renk):
    for position in chess.single_gen(chess.DARK_SQUARES):
        paint_square(chess.bb2str(position), square_renk)


def get_square_rect(square):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    return pygame.Rect((col * SQUARE_SIDE, row * SQUARE_SIDE), (SQUARE_SIDE, SQUARE_SIDE))


def coord2str(position, renk=chess.BEYAZ):
    if renk == chess.BEYAZ:
        file_index = int(position[0] / SQUARE_SIDE)
        rank_index = 7 - int(position[1] / SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if renk == chess.SIYAH:
        file_index = 7 - int(position[0] / SQUARE_SIDE)
        rank_index = int(position[1] / SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]


def print_board(board, renk=chess.BEYAZ):
    if renk == chess.BEYAZ:
        printed_board = board
    if renk == chess.SIYAH:
        printed_board = chess.rotate_board(board)

    print_empty_board()

    if chess.is_check(board, chess.BEYAZ):
        paint_square(chess.bb2str(chess.get_SAH(printed_board, chess.BEYAZ)), RED_CHECK)
    if chess.is_check(board, chess.SIYAH):
        paint_square(chess.bb2str(chess.get_SAH(printed_board, chess.SIYAH)), RED_CHECK)

    for position in chess.renked_piece_gen(printed_board, chess.SAH, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_SAH, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.VEZIR, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_VEZIR, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.KALE, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_KALE, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.FIL, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_FIL, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.AT, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_AT, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.PIYON, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_PIYON, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.JOKER, chess.SIYAH):
        SCREEN.blit(pygame.transform.scale(SIYAH_JOKER, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))

    for position in chess.renked_piece_gen(printed_board, chess.SAH, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_SAH, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.VEZIR, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_VEZIR, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.KALE, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_KALE, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.FIL, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_FIL, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.AT, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_AT, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.PIYON, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_PIYON, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.renked_piece_gen(printed_board, chess.JOKER, chess.BEYAZ):
        SCREEN.blit(pygame.transform.scale(BEYAZ_JOKER, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))

    pygame.display.flip()


def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()


def make_AI_move(game, renk):
    set_title(SCREEN_TITLE + ' - HAMLE HESAPLANIYOR...')
    new_game = chess.make_move(game, chess.get_AI_move(game, AI_SEARCH_DEPTH))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, renk)
    return new_game


def try_move(game, attempted_move):
    for move in chess.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chess.make_move(game, move)
    return game


def play_as(game, renk):
    run = True
    ongoing = True
    joker = 0

    try:
        while run:
            CLOCK.tick(CLOCK_TICK)
            print_board(game.board, renk)

            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False

            if ongoing and game.to_move == chess.opposing_renk(renk):
                game = make_AI_move(game, renk)

            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    leaving_square = coord2str(event.pos, renk)

                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, renk)

                    if ongoing and game.to_move == renk:
                        move = (chess.str2bb(leaving_square), chess.str2bb(arriving_square))
                        game = try_move(game, move)
                        print_board(game.board, renk)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing:  # H tuşu
                        game = make_AI_move(game, renk)
                    if event.key == 117:  # U TUŞU
                        game = chess.unmake_move(game)
                        game = chess.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        print_board(game.board, renk)
                        ongoing = True
                    if event.key == 99:  # C tuşu
                        global BOARD_renk
                        new_renks = deepcopy(BOARD_renkS)
                        new_renks.remove(BOARD_renk)
                        BOARD_renk = choice(new_renks)
                        print_board(game.board, renk)
                    if event.key == 112 or event.key == 100:  # P veya D tuşu
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101:  # E tuşu
                        print('eval = ' + str(chess.evaluate_game(game) / 100))
                    if event.key == 106:  # J tuşu
                        joker += 1
                        if joker == 13 and chess.get_VEZIR(game.board, renk):
                            VEZIR_index = chess.bb2index(chess.get_VEZIR(game.board, renk))
                            game.board[VEZIR_index] = renk | chess.JOKER
                            print_board(game.board, renk)

                if event.type == pygame.VIDEORESIZE:
                    if SCREEN.get_height() != event.h:
                        resize_screen(int(event.h / 8.0))
                    elif SCREEN.get_width() != event.w:
                        resize_screen(int(event.w / 8.0))
                    print_board(game.board, renk)
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as BEYAZ:\n\t' if renk == chess.BEYAZ else '\nPlaying as SIYAH:\n\t')
        bug_file.write(game.get_move_list() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()


def play_as_BEYAZ(game=chess.Game()):
    return play_as(game, chess.BEYAZ)


def play_as_SIYAH(game=chess.Game()):
    return play_as(game, chess.SIYAH)


def play_random_renk(game=chess.Game()):
    renk = choice([chess.BEYAZ, chess.SIYAH])
    play_as(game, renk)


# chess.verbose = True
play_random_renk()
