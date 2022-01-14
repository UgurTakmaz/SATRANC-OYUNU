from copy import deepcopy
from random import choice
from time import sleep, time

renk_MASK = 1 << 3
BEYAZ = 0 << 3
SIYAH = 1 << 3

ENDGAME_PIECE_COUNT = 7

PIECE_MASK = 0b111
EMPTY = 0
PIYON = 1
AT = 2
FIL = 3
KALE = 4
VEZIR = 5
SAH = 6
JOKER = 7

PIECE_TYPES = [PIYON, AT, FIL, KALE, VEZIR, SAH, JOKER]
PIECE_VALUES = {EMPTY: 0, PIYON: 100, AT: 300, FIL: 300, KALE: 500, VEZIR: 900, JOKER: 1300, SAH: 42000}

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

CASTLE_SAHSIDE_BEYAZ = 0b1 << 0
CASTLE_VEZIRSIDE_BEYAZ = 0b1 << 1
CASTLE_SAHSIDE_SIYAH = 0b1 << 2
CASTLE_VEZIRSIDE_SIYAH = 0b1 << 3

FULL_CASTLING_RIGHTS = CASTLE_SAHSIDE_BEYAZ | CASTLE_VEZIRSIDE_BEYAZ | CASTLE_SAHSIDE_SIYAH | CASTLE_VEZIRSIDE_SIYAH

ALL_SQUARES = 0xFFFFFFFFFFFFFFFF
FILE_A = 0x0101010101010101
FILE_B = 0x0202020202020202
FILE_C = 0x0404040404040404
FILE_D = 0x0808080808080808
FILE_E = 0x1010101010101010
FILE_F = 0x2020202020202020
FILE_G = 0x4040404040404040
FILE_H = 0x8080808080808080
RANK_1 = 0x00000000000000FF
RANK_2 = 0x000000000000FF00
RANK_3 = 0x0000000000FF0000
RANK_4 = 0x00000000FF000000
RANK_5 = 0x000000FF00000000
RANK_6 = 0x0000FF0000000000
RANK_7 = 0x00FF000000000000
RANK_8 = 0xFF00000000000000
DIAG_A1H8 = 0x8040201008040201
ANTI_DIAG_H1A8 = 0x0102040810204080
LIGHT_SQUARES = 0x55AA55AA55AA55AA
DARK_SQUARES = 0xAA55AA55AA55AA55

FILE_MASKS = [FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H]
RANK_MASKS = [RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8]

ILK_TAHTA = [BEYAZ | KALE, BEYAZ | AT, BEYAZ | FIL, BEYAZ | VEZIR, BEYAZ | SAH, BEYAZ | FIL, BEYAZ | AT,
                 BEYAZ | KALE,
                 BEYAZ | PIYON, BEYAZ | PIYON, BEYAZ | PIYON, BEYAZ | PIYON, BEYAZ | PIYON, BEYAZ | PIYON,
                 BEYAZ | PIYON, BEYAZ | PIYON,
                 EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                 EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                 EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                 EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                 SIYAH | PIYON, SIYAH | PIYON, SIYAH | PIYON, SIYAH | PIYON, SIYAH | PIYON, SIYAH | PIYON,
                 SIYAH | PIYON, SIYAH | PIYON,
                 SIYAH | KALE, SIYAH | AT, SIYAH | FIL, SIYAH | VEZIR, SIYAH | SAH, SIYAH | FIL, SIYAH | AT,
                 SIYAH | KALE]

BOS_TAHTA = [EMPTY for _ in range(64)]

INITIAL_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
STROKES_YOLO = '1k6/2b1p3/Qp4N1/4r2P/2B2q2/1R6/2Pn2K1/8 w - - 0 1'

TAS_KODLARI = {BEYAZ | SAH: 'K',
               BEYAZ | VEZIR: 'Q',
               BEYAZ | KALE: 'R',
               BEYAZ | FIL: 'B',
               BEYAZ | AT: 'N',
               BEYAZ | PIYON: 'P',
               BEYAZ | JOKER: 'J',
               SIYAH | SAH: 'k',
               SIYAH | VEZIR: 'q',
               SIYAH | KALE: 'r',
               SIYAH | FIL: 'b',
               SIYAH | AT: 'n',
               SIYAH | PIYON: 'p',
               SIYAH | JOKER: 'j',
               EMPTY: '.'}
TAS_KODLARI.update({v: k for k, v in TAS_KODLARI.items()})

DOUBLED_PIYON_PENALTY = 10
ISOLATED_PIYON_PENALTY = 20
BACKWARDS_PIYON_PENALTY = 8
PASSED_PIYON_BONUS = 20
KALE_SEMI_OPEN_FILE_BONUS = 10
KALE_OPEN_FILE_BONUS = 15
KALE_ON_SEVENTH_BONUS = 20

PIYON_BONUS = [0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, -40, -40, 0, 0, 0,
               1, 2, 3, -10, -10, 3, 2, 1,
               2, 4, 6, 8, 8, 6, 4, 2,
               3, 6, 9, 12, 12, 9, 6, 3,
               4, 8, 12, 16, 16, 12, 8, 4,
               5, 10, 15, 20, 20, 15, 10, 5,
               0, 0, 0, 0, 0, 0, 0, 0]

AT_BONUS = [-10, -30, -10, -10, -10, -10, -30, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, -10, -10, -10, -10, -10, -10, -10]

FIL_BONUS = [-10, -10, -20, -10, -10, -20, -10, -10,
             -10, 0, 0, 0, 0, 0, 0, -10,
             -10, 0, 5, 5, 5, 5, 0, -10,
             -10, 0, 5, 10, 10, 5, 0, -10,
             -10, 0, 5, 10, 10, 5, 0, -10,
             -10, 0, 5, 5, 5, 5, 0, -10,
             -10, 0, 0, 0, 0, 0, 0, -10,
             -10, -10, -10, -10, -10, -10, -10, -10]

SAH_BONUS = [0, 20, 40, -20, 0, -20, 40, 20,
             -20, -20, -20, -20, -20, -20, -20, -20,
             -40, -40, -40, -40, -40, -40, -40, -40,
             -40, -40, -40, -40, -40, -40, -40, -40,
             -40, -40, -40, -40, -40, -40, -40, -40,
             -40, -40, -40, -40, -40, -40, -40, -40,
             -40, -40, -40, -40, -40, -40, -40, -40,
             -40, -40, -40, -40, -40, -40, -40, -40]

SAH_ENDGAME_BONUS = [0, 10, 20, 30, 30, 20, 10, 0,
                     10, 20, 30, 40, 40, 30, 20, 10,
                     20, 30, 40, 50, 50, 40, 30, 20,
                     30, 40, 50, 60, 60, 50, 40, 30,
                     30, 40, 50, 60, 60, 50, 40, 30,
                     20, 30, 40, 50, 50, 40, 30, 20,
                     10, 20, 30, 40, 40, 30, 20, 10,
                     0, 10, 20, 30, 30, 20, 10, 0]

verbose = False


# ========== SATRANÇ OYUNU ==========

class Game:
    def __init__(self, FEN=''):
        self.board = ILK_TAHTA
        self.to_move = BEYAZ
        self.ep_square = 0
        self.castling_rights = FULL_CASTLING_RIGHTS
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.position_history = []
        if FEN != '':
            self.load_FEN(FEN)
            self.position_history.append(FEN)
        else:
            self.position_history.append(INITIAL_FEN)

        self.move_history = []

    def get_move_list(self):
        return ' '.join(self.move_history)

    def to_FEN(self):
        FEN_str = ''

        for i in range(len(RANKS)):
            first = len(self.board) - 8 * (i + 1)
            empty_sqrs = 0
            for fille in range(len(FILES)):
                piece = self.board[first + fille]
                if piece & PIECE_MASK == EMPTY:
                    empty_sqrs += 1
                else:
                    if empty_sqrs > 0:
                        FEN_str += '{}'.format(empty_sqrs)
                    FEN_str += '{}'.format(piece2str(piece))
                    empty_sqrs = 0
            if empty_sqrs > 0:
                FEN_str += '{}'.format(empty_sqrs)
            FEN_str += '/'
        FEN_str = FEN_str[:-1] + ' '

        if self.to_move == BEYAZ:
            FEN_str += 'w '
        if self.to_move == SIYAH:
            FEN_str += 'b '

        if self.castling_rights & CASTLE_SAHSIDE_BEYAZ:
            FEN_str += 'K'
        if self.castling_rights & CASTLE_VEZIRSIDE_BEYAZ:
            FEN_str += 'Q'
        if self.castling_rights & CASTLE_SAHSIDE_SIYAH:
            FEN_str += 'k'
        if self.castling_rights & CASTLE_VEZIRSIDE_SIYAH:
            FEN_str += 'q'
        if self.castling_rights == 0:
            FEN_str += '-'
        FEN_str += ' '

        if self.ep_square == 0:
            FEN_str += '-'
        else:
            FEN_str += bb2str(self.ep_square)

        FEN_str += ' {}'.format(self.halfmove_clock)
        FEN_str += ' {}'.format(self.fullmove_number)
        return FEN_str

    def load_FEN(self, FEN_str):
        FEN_list = FEN_str.split(' ')

        board_str = FEN_list[0]
        rank_list = board_str.split('/')
        rank_list.reverse()
        self.board = []

        for rank in rank_list:
            rank_pieces = []
            for p in rank:
                if p.isdigit():
                    for _ in range(int(p)):
                        rank_pieces.append(EMPTY)
                else:
                    rank_pieces.append(str2piece(p))
            self.board.extend(rank_pieces)

        to_move_str = FEN_list[1].lower()
        if to_move_str == 'w':
            self.to_move = BEYAZ
        if to_move_str == 'b':
            self.to_move = SIYAH

        castling_rights_str = FEN_list[2]
        self.castling_rights = 0
        if castling_rights_str.find('K') >= 0:
            self.castling_rights |= CASTLE_SAHSIDE_BEYAZ
        if castling_rights_str.find('Q') >= 0:
            self.castling_rights |= CASTLE_VEZIRSIDE_BEYAZ
        if castling_rights_str.find('k') >= 0:
            self.castling_rights |= CASTLE_SAHSIDE_SIYAH
        if castling_rights_str.find('q') >= 0:
            self.castling_rights |= CASTLE_VEZIRSIDE_SIYAH

        ep_str = FEN_list[3]
        if ep_str == '-':
            self.ep_square = 0
        else:
            self.ep_square = str2bb(ep_str)

        self.halfmove_clock = int(FEN_list[4])
        self.fullmove_number = int(FEN_list[5])


# ================================


def get_piece(board, bitboard):
    return board[bb2index(bitboard)]


def bb2index(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            return i


def str2index(position_str):
    fille = FILES.index(position_str[0].lower())
    rank = RANKS.index(position_str[1])
    return 8 * rank + fille


def bb2str(bitboard):
    for i in range(64):
        if bitboard & (0b1 << i):
            fille = i % 8
            rank = int(i / 8)
            return '{}{}'.format(FILES[fille], RANKS[rank])


def str2bb(position_str):
    return 0b1 << str2index(position_str)


def move2str(move):
    return bb2str(move[0]) + bb2str(move[1])


def single_gen(bitboard):
    for i in range(64):
        bit = 0b1 << i
        if bitboard & bit:
            yield bit


def piece_gen(board, piece_code):
    for i in range(64):
        if board[i] & PIECE_MASK == piece_code:
            yield 0b1 << i


def renked_piece_gen(board, piece_code, renk):
    for i in range(64):
        if board[i] == piece_code | renk:
            yield 0b1 << i


def opposing_renk(renk):
    if renk == BEYAZ:
        return SIYAH
    if renk == SIYAH:
        return BEYAZ


def piece2str(piece):
    return TAS_KODLARI[piece]


def str2piece(string):
    return TAS_KODLARI[string]


def print_board(board):
    print('')
    for i in range(len(RANKS)):
        rank_str = str(8 - i) + ' '
        first = len(board) - 8 * (i + 1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(board[first + fille]))
        print(rank_str)
    print('  a b c d e f g h')


def print_rotated_board(board):
    r_board = rotate_board(board)
    print('')
    for i in range(len(RANKS)):
        rank_str = str(i + 1) + ' '
        first = len(r_board) - 8 * (i + 1)
        for fille in range(len(FILES)):
            rank_str += '{} '.format(piece2str(r_board[first + fille]))
        print(rank_str)
    print('  h g f e d c b a')


def print_bitboard(bitboard):
    print('')
    for rank in range(len(RANKS)):
        rank_str = str(8 - rank) + ' '
        for fille in range(len(FILES)):
            if (bitboard >> (fille + (7 - rank) * 8)) & 0b1:
                rank_str += '# '
            else:
                rank_str += '. '
        print(rank_str)
    print('  a b c d e f g h')


def lsb(bitboard):
    for i in range(64):
        bit = (0b1 << i)
        if bit & bitboard:
            return bit


def msb(bitboard):
    for i in range(64):
        bit = (0b1 << (63 - i))
        if bit & bitboard:
            return bit


def get_renked_pieces(board, renk):
    return list2int([(i != EMPTY and i & renk_MASK == renk) for i in board])


def empty_squares(board):
    return list2int([i == EMPTY for i in board])


def occupied_squares(board):
    return nnot(empty_squares(board))


def list2int(lst):
    rev_list = lst[:]
    rev_list.reverse()
    return int('0b' + ''.join(['1' if i else '0' for i in rev_list]), 2)


def nnot(bitboard):
    return ~bitboard & ALL_SQUARES


def rotate_board(board):
    rotated_board = deepcopy(board)
    rotated_board.reverse()
    return rotated_board


def flip_board_v(board):
    flip = [56, 57, 58, 59, 60, 61, 62, 63,
            48, 49, 50, 51, 52, 53, 54, 55,
            40, 41, 42, 43, 44, 45, 46, 47,
            32, 33, 34, 35, 36, 37, 38, 39,
            24, 25, 26, 27, 28, 29, 30, 31,
            16, 17, 18, 19, 20, 21, 22, 23,
            8, 9, 10, 11, 12, 13, 14, 15,
            0, 1, 2, 3, 4, 5, 6, 7]

    return deepcopy([board[flip[i]] for i in range(64)])


def east_one(bitboard):
    return (bitboard << 1) & nnot(FILE_A)


def west_one(bitboard):
    return (bitboard >> 1) & nnot(FILE_H)


def north_one(bitboard):
    return (bitboard << 8) & nnot(RANK_1)


def south_one(bitboard):
    return (bitboard >> 8) & nnot(RANK_8)


def NE_one(bitboard):
    return north_one(east_one(bitboard))


def NW_one(bitboard):
    return north_one(west_one(bitboard))


def SE_one(bitboard):
    return south_one(east_one(bitboard))


def SW_one(bitboard):
    return south_one(west_one(bitboard))


def move_piece(board, move):
    new_board = deepcopy(board)
    new_board[bb2index(move[1])] = new_board[bb2index(move[0])]
    new_board[bb2index(move[0])] = EMPTY
    return new_board


def make_move(game, move):
    new_game = deepcopy(game)
    leaving_position = move[0]
    arriving_position = move[1]

    # timerı güncelle
    new_game.halfmove_clock += 1
    if new_game.to_move == SIYAH:
        new_game.fullmove_number += 1

    # yakalnırsa saati sıfırla
    if get_piece(new_game.board, arriving_position) != EMPTY:
        new_game.halfmove_clock = 0

    #  PIYONLAR: timerı sıfırla, bilinen epi sıfırla yeni ep ata ve piyonu yükselt
    if get_piece(new_game.board, leaving_position) & PIECE_MASK == PIYON:
        new_game.halfmove_clock = 0

        if arriving_position == game.ep_square:
            new_game.board = remove_captured_ep(new_game)

        if is_double_push(leaving_position, arriving_position):
            new_game.ep_square = new_ep_square(leaving_position)

        if arriving_position & (RANK_1 | RANK_8):
            new_game.board[bb2index(leaving_position)] = new_game.to_move | VEZIR

    # güncel değilse ep square sıfırlama
    if new_game.ep_square == game.ep_square:
        new_game.ep_square = 0

    # Kale hamleleri için rok hakkı güncelleme
    if leaving_position == str2bb('a1'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_VEZIRSIDE_BEYAZ)
    if leaving_position == str2bb('h1'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_SAHSIDE_BEYAZ)
    if leaving_position == str2bb('a8'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_VEZIRSIDE_SIYAH)
    if leaving_position == str2bb('h8'):
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_SAHSIDE_SIYAH)

    # rok yapmak
    if get_piece(new_game.board, leaving_position) == BEYAZ | SAH:
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_SAHSIDE_BEYAZ | CASTLE_VEZIRSIDE_BEYAZ)
        if leaving_position == str2bb('e1'):
            if arriving_position == str2bb('g1'):
                new_game.board = move_piece(new_game.board, [str2bb('h1'), str2bb('f1')])
            if arriving_position == str2bb('c1'):
                new_game.board = move_piece(new_game.board, [str2bb('a1'), str2bb('d1')])

    if get_piece(new_game.board, leaving_position) == SIYAH | SAH:
        new_game.castling_rights = remove_castling_rights(new_game, CASTLE_SAHSIDE_SIYAH | CASTLE_VEZIRSIDE_SIYAH)
        if leaving_position == str2bb('e8'):
            if arriving_position == str2bb('g8'):
                new_game.board = move_piece(new_game.board, [str2bb('h8'), str2bb('f8')])
            if arriving_position == str2bb('c8'):
                new_game.board = move_piece(new_game.board, [str2bb('a8'), str2bb('d8')])

    # pozisyonları yenileme ve yeni hamle
    new_game.board = move_piece(new_game.board, (leaving_position, arriving_position))
    new_game.to_move = opposing_renk(new_game.to_move)

    #geçmişi güncelle
    new_game.move_history.append(move2str(move))
    new_game.position_history.append(new_game.to_FEN())
    return new_game


def unmake_move(game):
    if len(game.position_history) < 2:
        return deepcopy(game)

    new_game = Game(game.position_history[-2])
    new_game.move_history = deepcopy(game.move_history)[:-1]
    new_game.position_history = deepcopy(game.position_history)[:-1]
    return new_game


def get_rank(rank_num):
    rank_num = int(rank_num)
    return RANK_MASKS[rank_num]


def get_file(file_str):
    file_str = file_str.lower()
    file_num = FILES.index(file_str)
    return FILE_MASKS[file_num]


def get_filter(filter_str):
    if filter_str in FILES:
        return get_file(filter_str)
    if filter_str in RANKS:
        return get_rank(filter_str)


# ========== PIYON ==========

def get_all_PIYONs(board):
    return list2int([i & PIECE_MASK == PIYON for i in board])


def get_PIYONs(board, renk):
    return list2int([i == renk | PIYON for i in board])


def PIYON_moves(moving_piece, game, renk):
    return PIYON_pushes(moving_piece, game.board, renk) | PIYON_captures(moving_piece, game, renk)


def PIYON_captures(moving_piece, game, renk):
    return PIYON_simple_captures(moving_piece, game, renk) | PIYON_ep_captures(moving_piece, game, renk)


def PIYON_pushes(moving_piece, board, renk):
    return PIYON_simple_pushes(moving_piece, board, renk) | PIYON_double_pushes(moving_piece, board, renk)


def PIYON_simple_captures(attacSAH_piece, game, renk):
    return PIYON_attacks(attacSAH_piece, game.board, renk) & get_renked_pieces(game.board, opposing_renk(renk))


def PIYON_ep_captures(attacSAH_piece, game, renk):
    if renk == BEYAZ:
        ep_squares = game.ep_square & RANK_6
    if renk == SIYAH:
        ep_squares = game.ep_square & RANK_3
    return PIYON_attacks(attacSAH_piece, game.board, renk) & ep_squares


def PIYON_attacks(attacSAH_piece, board, renk):
    return PIYON_east_attacks(attacSAH_piece, board, renk) | PIYON_west_attacks(attacSAH_piece, board, renk)


def PIYON_simple_pushes(moving_piece, board, renk):
    if renk == BEYAZ:
        return north_one(moving_piece) & empty_squares(board)
    if renk == SIYAH:
        return south_one(moving_piece) & empty_squares(board)


def PIYON_double_pushes(moving_piece, board, renk):
    if renk == BEYAZ:
        return north_one(PIYON_simple_pushes(moving_piece, board, renk)) & (empty_squares(board) & RANK_4)
    if renk == SIYAH:
        return south_one(PIYON_simple_pushes(moving_piece, board, renk)) & (empty_squares(board) & RANK_5)


def PIYON_east_attacks(attacSAH_piece, board, renk):
    if renk == BEYAZ:
        return NE_one(attacSAH_piece & get_renked_pieces(board, renk))
    if renk == SIYAH:
        return SE_one(attacSAH_piece & get_renked_pieces(board, renk))


def PIYON_west_attacks(attacSAH_piece, board, renk):
    if renk == BEYAZ:
        return NW_one(attacSAH_piece & get_renked_pieces(board, renk))
    if renk == SIYAH:
        return SW_one(attacSAH_piece & get_renked_pieces(board, renk))


def PIYON_double_attacks(attacSAH_piece, board, renk):
    return PIYON_east_attacks(attacSAH_piece, board, renk) & PIYON_west_attacks(attacSAH_piece, board, renk)


def is_double_push(leaving_square, target_square):
    return (leaving_square & RANK_2 and target_square & RANK_4) or \
           (leaving_square & RANK_7 and target_square & RANK_5)


def new_ep_square(leaving_square):
    if leaving_square & RANK_2:
        return north_one(leaving_square)
    if leaving_square & RANK_7:
        return south_one(leaving_square)


def remove_captured_ep(game):
    new_board = deepcopy(game.board)
    if game.ep_square & RANK_3:
        new_board[bb2index(north_one(game.ep_square))] = EMPTY
    if game.ep_square & RANK_6:
        new_board[bb2index(south_one(game.ep_square))] = EMPTY
    return new_board


# ========== AT ==========

def get_ATs(board, renk):
    return list2int([i == renk | AT for i in board])


def AT_moves(moving_piece, board, renk):
    return AT_attacks(moving_piece) & nnot(get_renked_pieces(board, renk))


def AT_attacks(moving_piece):
    return AT_NNE(moving_piece) | \
           AT_ENE(moving_piece) | \
           AT_NNW(moving_piece) | \
           AT_WNW(moving_piece) | \
           AT_SSE(moving_piece) | \
           AT_ESE(moving_piece) | \
           AT_SSW(moving_piece) | \
           AT_WSW(moving_piece)


def AT_WNW(moving_piece):
    return moving_piece << 6 & nnot(FILE_G | FILE_H)


def AT_ENE(moving_piece):
    return moving_piece << 10 & nnot(FILE_A | FILE_B)


def AT_NNW(moving_piece):
    return moving_piece << 15 & nnot(FILE_H)


def AT_NNE(moving_piece):
    return moving_piece << 17 & nnot(FILE_A)


def AT_ESE(moving_piece):
    return moving_piece >> 6 & nnot(FILE_A | FILE_B)


def AT_WSW(moving_piece):
    return moving_piece >> 10 & nnot(FILE_G | FILE_H)


def AT_SSE(moving_piece):
    return moving_piece >> 15 & nnot(FILE_A)


def AT_SSW(moving_piece):
    return moving_piece >> 17 & nnot(FILE_H)


def AT_fill(moving_piece, n):
    fill = moving_piece
    for _ in range(n):
        fill |= AT_attacks(fill)
    return fill


def AT_distance(pos1, pos2):
    init_bitboard = str2bb(pos1)
    end_bitboard = str2bb(pos2)
    fill = init_bitboard
    dist = 0
    while fill & end_bitboard == 0:
        dist += 1
        fill = AT_fill(init_bitboard, dist)
    return dist


# ========== SAH ==========

def get_SAH(board, renk):
    return list2int([i == renk | SAH for i in board])


def SAH_moves(moving_piece, board, renk):
    return SAH_attacks(moving_piece) & nnot(get_renked_pieces(board, renk))


def SAH_attacks(moving_piece):
    SAH_atks = moving_piece | east_one(moving_piece) | west_one(moving_piece)
    SAH_atks |= north_one(SAH_atks) | south_one(SAH_atks)
    return SAH_atks & nnot(moving_piece)


def can_castle_SAHside(game, renk):
    if renk == BEYAZ:
        return (game.castling_rights & CASTLE_SAHSIDE_BEYAZ) and \
               game.board[str2index('f1')] == EMPTY and \
               game.board[str2index('g1')] == EMPTY and \
               (not is_attacked(str2bb('e1'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('f1'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('g1'), game.board, opposing_renk(renk)))
    if renk == SIYAH:
        return (game.castling_rights & CASTLE_SAHSIDE_SIYAH) and \
               game.board[str2index('f8')] == EMPTY and \
               game.board[str2index('g8')] == EMPTY and \
               (not is_attacked(str2bb('e8'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('f8'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('g8'), game.board, opposing_renk(renk)))


def can_castle_VEZIRside(game, renk):
    if renk == BEYAZ:
        return (game.castling_rights & CASTLE_VEZIRSIDE_BEYAZ) and \
               game.board[str2index('b1')] == EMPTY and \
               game.board[str2index('c1')] == EMPTY and \
               game.board[str2index('d1')] == EMPTY and \
               (not is_attacked(str2bb('c1'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('d1'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('e1'), game.board, opposing_renk(renk)))
    if renk == SIYAH:
        return (game.castling_rights & CASTLE_VEZIRSIDE_SIYAH) and \
               game.board[str2index('b8')] == EMPTY and \
               game.board[str2index('c8')] == EMPTY and \
               game.board[str2index('d8')] == EMPTY and \
               (not is_attacked(str2bb('c8'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('d8'), game.board, opposing_renk(renk))) and \
               (not is_attacked(str2bb('e8'), game.board, opposing_renk(renk)))


def castle_SAHside_move(game):
    if game.to_move == BEYAZ:
        return (str2bb('e1'), str2bb('g1'))
    if game.to_move == SIYAH:
        return (str2bb('e8'), str2bb('g8'))


def castle_VEZIRside_move(game):
    if game.to_move == BEYAZ:
        return (str2bb('e1'), str2bb('c1'))
    if game.to_move == SIYAH:
        return (str2bb('e8'), str2bb('c8'))


def remove_castling_rights(game, removed_rights):
    return game.castling_rights & ~removed_rights


# ========== FIL ==========

def get_FILs(board, renk):
    return list2int([i == renk | FIL for i in board])


def FIL_rays(moving_piece):
    return diagonal_rays(moving_piece) | anti_diagonal_rays(moving_piece)


def diagonal_rays(moving_piece):
    return NE_ray(moving_piece) | SW_ray(moving_piece)


def anti_diagonal_rays(moving_piece):
    return NW_ray(moving_piece) | SE_ray(moving_piece)


def NE_ray(moving_piece):
    ray_atks = NE_one(moving_piece)
    for _ in range(6):
        ray_atks |= NE_one(ray_atks)
    return ray_atks & ALL_SQUARES


def SE_ray(moving_piece):
    ray_atks = SE_one(moving_piece)
    for _ in range(6):
        ray_atks |= SE_one(ray_atks)
    return ray_atks & ALL_SQUARES


def NW_ray(moving_piece):
    ray_atks = NW_one(moving_piece)
    for _ in range(6):
        ray_atks |= NW_one(ray_atks)
    return ray_atks & ALL_SQUARES


def SW_ray(moving_piece):
    ray_atks = SW_one(moving_piece)
    for _ in range(6):
        ray_atks |= SW_one(ray_atks)
    return ray_atks & ALL_SQUARES


def NE_attacks(single_piece, board, renk):
    blocker = lsb(NE_ray(single_piece) & occupied_squares(board))
    if blocker:
        return NE_ray(single_piece) ^ NE_ray(blocker)
    else:
        return NE_ray(single_piece)


def NW_attacks(single_piece, board, renk):
    blocker = lsb(NW_ray(single_piece) & occupied_squares(board))
    if blocker:
        return NW_ray(single_piece) ^ NW_ray(blocker)
    else:
        return NW_ray(single_piece)


def SE_attacks(single_piece, board, renk):
    blocker = msb(SE_ray(single_piece) & occupied_squares(board))
    if blocker:
        return SE_ray(single_piece) ^ SE_ray(blocker)
    else:
        return SE_ray(single_piece)


def SW_attacks(single_piece, board, renk):
    blocker = msb(SW_ray(single_piece) & occupied_squares(board))
    if blocker:
        return SW_ray(single_piece) ^ SW_ray(blocker)
    else:
        return SW_ray(single_piece)


def diagonal_attacks(single_piece, board, renk):
    return NE_attacks(single_piece, board, renk) | SW_attacks(single_piece, board, renk)


def anti_diagonal_attacks(single_piece, board, renk):
    return NW_attacks(single_piece, board, renk) | SE_attacks(single_piece, board, renk)


def FIL_attacks(moving_piece, board, renk):
    atks = 0
    for piece in single_gen(moving_piece):
        atks |= diagonal_attacks(piece, board, renk) | anti_diagonal_attacks(piece, board, renk)
    return atks


def FIL_moves(moving_piece, board, renk):
    return FIL_attacks(moving_piece, board, renk) & nnot(get_renked_pieces(board, renk))


# ========== KALE ==========

def get_KALEs(board, renk):
    return list2int([i == renk | KALE for i in board])


def KALE_rays(moving_piece):
    return rank_rays(moving_piece) | file_rays(moving_piece)


def rank_rays(moving_piece):
    return east_ray(moving_piece) | west_ray(moving_piece)


def file_rays(moving_piece):
    return north_ray(moving_piece) | south_ray(moving_piece)


def east_ray(moving_piece):
    ray_atks = east_one(moving_piece)
    for _ in range(6):
        ray_atks |= east_one(ray_atks)
    return ray_atks & ALL_SQUARES


def west_ray(moving_piece):
    ray_atks = west_one(moving_piece)
    for _ in range(6):
        ray_atks |= west_one(ray_atks)
    return ray_atks & ALL_SQUARES


def north_ray(moving_piece):
    ray_atks = north_one(moving_piece)
    for _ in range(6):
        ray_atks |= north_one(ray_atks)
    return ray_atks & ALL_SQUARES


def south_ray(moving_piece):
    ray_atks = south_one(moving_piece)
    for _ in range(6):
        ray_atks |= south_one(ray_atks)
    return ray_atks & ALL_SQUARES


def east_attacks(single_piece, board, renk):
    blocker = lsb(east_ray(single_piece) & occupied_squares(board))
    if blocker:
        return east_ray(single_piece) ^ east_ray(blocker)
    else:
        return east_ray(single_piece)


def west_attacks(single_piece, board, renk):
    blocker = msb(west_ray(single_piece) & occupied_squares(board))
    if blocker:
        return west_ray(single_piece) ^ west_ray(blocker)
    else:
        return west_ray(single_piece)


def rank_attacks(single_piece, board, renk):
    return east_attacks(single_piece, board, renk) | west_attacks(single_piece, board, renk)


def north_attacks(single_piece, board, renk):
    blocker = lsb(north_ray(single_piece) & occupied_squares(board))
    if blocker:
        return north_ray(single_piece) ^ north_ray(blocker)
    else:
        return north_ray(single_piece)


def south_attacks(single_piece, board, renk):
    blocker = msb(south_ray(single_piece) & occupied_squares(board))
    if blocker:
        return south_ray(single_piece) ^ south_ray(blocker)
    else:
        return south_ray(single_piece)


def file_attacks(single_piece, board, renk):
    return north_attacks(single_piece, board, renk) | south_attacks(single_piece, board, renk)


def KALE_attacks(moving_piece, board, renk):
    atks = 0
    for single_piece in single_gen(moving_piece):
        atks |= rank_attacks(single_piece, board, renk) | file_attacks(single_piece, board, renk)
    return atks


def KALE_moves(moving_piece, board, renk):
    return KALE_attacks(moving_piece, board, renk) & nnot(get_renked_pieces(board, renk))


# ========== VEZIR ==========

def get_VEZIR(board, renk):
    return list2int([i == renk | VEZIR for i in board])


def VEZIR_rays(moving_piece):
    return KALE_rays(moving_piece) | FIL_rays(moving_piece)


def VEZIR_attacks(moving_piece, board, renk):
    return FIL_attacks(moving_piece, board, renk) | KALE_attacks(moving_piece, board, renk)


def VEZIR_moves(moving_piece, board, renk):
    return FIL_moves(moving_piece, board, renk) | KALE_moves(moving_piece, board, renk)


# ========== JOKER ==========

def joker_rays(moving_piece):
    return VEZIR_rays(moving_piece)


def joker_attacks(moving_piece, board, renk):
    return VEZIR_attacks(moving_piece, board, renk) | AT_attacks(moving_piece)


def joker_moves(moving_piece, board, renk):
    return VEZIR_moves(moving_piece, board, renk) | AT_moves(moving_piece, board, renk)


# ===========================

def is_attacked(target, board, attacSAH_renk):
    return count_attacks(target, board, attacSAH_renk) > 0


def is_check(board, renk):
    return is_attacked(get_SAH(board, renk), board, opposing_renk(renk))


def get_attacks(moving_piece, board, renk):
    piece = board[bb2index(moving_piece)]

    if piece & PIECE_MASK == PIYON:
        return PIYON_attacks(moving_piece, board, renk)
    elif piece & PIECE_MASK == AT:
        return AT_attacks(moving_piece)
    elif piece & PIECE_MASK == FIL:
        return FIL_attacks(moving_piece, board, renk)
    elif piece & PIECE_MASK == KALE:
        return KALE_attacks(moving_piece, board, renk)
    elif piece & PIECE_MASK == VEZIR:
        return VEZIR_attacks(moving_piece, board, renk)
    elif piece & PIECE_MASK == SAH:
        return SAH_attacks(moving_piece)
    elif piece & PIECE_MASK == JOKER:
        return joker_attacks(moving_piece, board, renk)


def get_moves(moving_piece, game, renk):
    piece = game.board[bb2index(moving_piece)]

    if piece & PIECE_MASK == PIYON:
        return PIYON_moves(moving_piece, game, renk)
    elif piece & PIECE_MASK == AT:
        return AT_moves(moving_piece, game.board, renk)
    elif piece & PIECE_MASK == FIL:
        return FIL_moves(moving_piece, game.board, renk)
    elif piece & PIECE_MASK == KALE:
        return KALE_moves(moving_piece, game.board, renk)
    elif piece & PIECE_MASK == VEZIR:
        return VEZIR_moves(moving_piece, game.board, renk)
    elif piece & PIECE_MASK == SAH:
        return SAH_moves(moving_piece, game.board, renk)
    elif piece & PIECE_MASK == JOKER:
        return joker_moves(moving_piece, game.board, renk)


def count_attacks(target, board, attacSAH_renk):
    attack_count = 0

    for index in range(64):
        piece = board[index]
        if piece != EMPTY and piece & renk_MASK == attacSAH_renk:
            pos = 0b1 << index

            if get_attacks(pos, board, attacSAH_renk) & target:
                attack_count += 1

    return attack_count


def material_sum(board, renk):
    material = 0
    for piece in board:
        if piece & renk_MASK == renk:
            material += PIECE_VALUES[piece & PIECE_MASK]
    return material


def material_balance(board):
    return material_sum(board, BEYAZ) - material_sum(board, SIYAH)


def mobility_balance(game):
    return count_legal_moves(game, BEYAZ) - count_legal_moves(game, SIYAH)


def evaluate_game(game):
    if game_ended(game):
        return evaluate_end_node(game)
    else:
        return material_balance(game.board) + positional_balance(game)  # + 10*mobility_balance(game)


def evaluate_end_node(game):
    if is_checkmate(game, game.to_move):
        return win_score(game.to_move)
    elif is_stalemate(game) or \
            has_insufficient_material(game) or \
            is_under_75_move_rule(game):
        return 0


def positional_balance(game):
    return positional_bonus(game, BEYAZ) - positional_bonus(game, SIYAH)


def positional_bonus(game, renk):
    bonus = 0

    if renk == BEYAZ:
        board = game.board
    elif renk == SIYAH:
        board = flip_board_v(game.board)

    for index in range(64):
        piece = board[index]

        if piece != EMPTY and piece & renk_MASK == renk:
            piece_type = piece & PIECE_MASK

            if piece_type == PIYON:
                bonus += PIYON_BONUS[index]
            elif piece_type == AT:
                bonus += AT_BONUS[index]
            elif piece_type == FIL:
                bonus += FIL_BONUS[index]

            elif piece_type == KALE:
                position = 0b1 << index

                if is_open_file(position, board):
                    bonus += KALE_OPEN_FILE_BONUS
                elif is_semi_open_file(position, board):
                    bonus += KALE_SEMI_OPEN_FILE_BONUS

                if position & RANK_7:
                    bonus += KALE_ON_SEVENTH_BONUS

            elif piece_type == SAH:
                if is_endgame(board):
                    bonus += SAH_ENDGAME_BONUS[index]
                else:
                    bonus += SAH_BONUS[index]

    return bonus


def is_endgame(board):
    return count_pieces(occupied_squares(board)) <= ENDGAME_PIECE_COUNT


def is_open_file(bitboard, board):
    for f in FILES:
        rank_filter = get_file(f)
        if bitboard & rank_filter:
            return count_pieces(get_all_PIYONs(board) & rank_filter) == 0


def is_semi_open_file(bitboard, board):
    for f in FILES:
        rank_filter = get_file(f)
        if bitboard & rank_filter:
            return count_pieces(get_all_PIYONs(board) & rank_filter) == 1


def count_pieces(bitboard):
    return bin(bitboard).count("1")


def win_score(renk):
    if renk == BEYAZ:
        return -10 * PIECE_VALUES[SAH]
    if renk == SIYAH:
        return 10 * PIECE_VALUES[SAH]


def pseudo_legal_moves(game, renk):
    for index in range(64):
        piece = game.board[index]

        if piece != EMPTY and piece & renk_MASK == renk:
            piece_pos = 0b1 << index

            for target in single_gen(get_moves(piece_pos, game, renk)):
                yield (piece_pos, target)

    if can_castle_SAHside(game, renk):
        yield (get_SAH(game.board, renk), east_one(east_one(get_SAH(game.board, renk))))
    if can_castle_VEZIRside(game, renk):
        yield (get_SAH(game.board, renk), west_one(west_one(get_SAH(game.board, renk))))


def legal_moves(game, renk):
    for move in pseudo_legal_moves(game, renk):
        if is_legal_move(game, move):
            yield move


def is_legal_move(game, move):
    new_game = make_move(game, move)
    return not is_check(new_game.board, game.to_move)


def count_legal_moves(game, renk):
    move_count = 0
    for _ in legal_moves(game, renk):
        move_count += 1
    return move_count


def is_stalemate(game):
    for _ in legal_moves(game, game.to_move):
        return False
    return not is_check(game.board, game.to_move)


def is_checkmate(game, renk):
    for _ in legal_moves(game, game.to_move):
        return False
    return is_check(game.board, renk)


def is_same_position(FEN_a, FEN_b):
    FEN_a_list = FEN_a.split(' ')
    FEN_b_list = FEN_b.split(' ')
    return FEN_a_list[0] == FEN_b_list[0] and \
           FEN_a_list[1] == FEN_b_list[1] and \
           FEN_a_list[2] == FEN_b_list[2] and \
           FEN_a_list[3] == FEN_b_list[3]


def has_threefold_repetition(game):
    current_pos = game.position_history[-1]
    position_count = 0
    for position in game.position_history:
        if is_same_position(current_pos, position):
            position_count += 1
    return position_count >= 3


def is_under_50_move_rule(game):
    return game.halfmove_clock >= 100


def is_under_75_move_rule(game):
    return game.halfmove_clock >= 150


def has_insufficient_material(game):  # TODO: other insufficient positions
    if material_sum(game.board, BEYAZ) + material_sum(game.board, SIYAH) == 2 * PIECE_VALUES[SAH]:
        return True
    if material_sum(game.board, BEYAZ) == PIECE_VALUES[SAH]:
        if material_sum(game.board, SIYAH) == PIECE_VALUES[SAH] + PIECE_VALUES[AT] and \
                (get_ATs(game.board, SIYAH) != 0 or get_FILs(game.board, SIYAH) != 0):
            return True
    if material_sum(game.board, SIYAH) == PIECE_VALUES[SAH]:
        if material_sum(game.board, BEYAZ) == PIECE_VALUES[SAH] + PIECE_VALUES[AT] and \
                (get_ATs(game.board, BEYAZ) != 0 or get_FILs(game.board, BEYAZ) != 0):
            return True
    return False


def game_ended(game):
    return is_checkmate(game, BEYAZ) or \
           is_checkmate(game, SIYAH) or \
           is_stalemate(game) or \
           has_insufficient_material(game) or \
           is_under_75_move_rule(game)


def random_move(game, renk):
    return choice(legal_moves(game, renk))


def evaluated_move(game, renk):
    best_score = win_score(renk)
    best_moves = []

    for move in legal_moves(game, renk):
        evaluation = evaluate_game(make_move(game, move))

        if is_checkmate(make_move(game, move), opposing_renk(game.to_move)):
            return [move, evaluation]

        if (renk == BEYAZ and evaluation > best_score) or \
                (renk == SIYAH and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)

    return [choice(best_moves), best_score]


def minimax(game, renk, depth=1):
    if game_ended(game):
        return [None, evaluate_game(game)]

    [simple_move, simple_evaluation] = evaluated_move(game, renk)

    if depth == 1 or \
            simple_evaluation == win_score(opposing_renk(renk)):
        return [simple_move, simple_evaluation]

    best_score = win_score(renk)
    best_moves = []

    for move in legal_moves(game, renk):
        his_game = make_move(game, move)

        if is_checkmate(his_game, his_game.to_move):
            return [move, win_score(his_game.to_move)]

        [_, evaluation] = minimax(his_game, opposing_renk(renk), depth - 1)

        if evaluation == win_score(opposing_renk(renk)):
            return [move, evaluation]

        if (renk == BEYAZ and evaluation > best_score) or \
                (renk == SIYAH and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)

    return [choice(best_moves), best_score]


def alpha_beta(game, renk, depth, alpha=-float('inf'), beta=float('inf')):
    if game_ended(game):
        return [None, evaluate_game(game)]

    [simple_move, simple_evaluation] = evaluated_move(game, renk)

    if depth == 1 or \
            simple_evaluation == win_score(opposing_renk(renk)):
        return [simple_move, simple_evaluation]

    best_moves = []

    if renk == BEYAZ:
        for move in legal_moves(game, renk):
            if verbose:
                print('\t' * depth + str(depth) + '. evaluating ' + TAS_KODLARI[
                    get_piece(game.board, move[0])] + move2str(move))

            new_game = make_move(game, move)
            [_, score] = alpha_beta(new_game, opposing_renk(renk), depth - 1, alpha, beta)

            if verbose:
                print('\t' * depth + str(depth) + '. ' + str(score) + ' [{},{}]'.format(alpha, beta))

            if score == win_score(opposing_renk(renk)):
                return [move, score]

            if score == alpha:
                best_moves.append(move)
            if score > alpha:  # BEYAZ max puan
                alpha = score
                best_moves = [move]
                if alpha > beta:  # alpha-beta sınırı
                    if verbose:
                        print('\t' * depth + 'cutoff')
                    break
        if best_moves:
            return [choice(best_moves), alpha]
        else:
            return [None, alpha]

    if renk == SIYAH:
        for move in legal_moves(game, renk):
            if verbose:
                print('\t' * depth + str(depth) + '. evaluating ' + TAS_KODLARI[
                    get_piece(game.board, move[0])] + move2str(move))

            new_game = make_move(game, move)
            [_, score] = alpha_beta(new_game, opposing_renk(renk), depth - 1, alpha, beta)

            if verbose:
                print('\t' * depth + str(depth) + '. ' + str(score) + ' [{},{}]'.format(alpha, beta))

            if score == win_score(opposing_renk(renk)):
                return [move, score]

            if score == beta:
                best_moves.append(move)
            if score < beta:  # SIYAH min puan
                beta = score
                best_moves = [move]
                if alpha > beta:  # alpha-beta sınırı
                    if verbose:
                        print('\t' * depth + 'cutoff')
                    break
        if best_moves:
            return [choice(best_moves), beta]
        else:
            return [None, beta]


def parse_move_code(game, move_code):
    move_code = move_code.replace(" ", "")
    move_code = move_code.replace("x", "")

    if move_code.upper() == 'O-O' or move_code == '0-0':
        if can_castle_SAHside(game, game.to_move):
            return castle_SAHside_move(game)

    if move_code.upper() == 'O-O-O' or move_code == '0-0-0':
        if can_castle_VEZIRside(game, game.to_move):
            return castle_VEZIRside_move(game)

    if len(move_code) < 2 or len(move_code) > 4:
        return False

    if len(move_code) == 4:
        filter_squares = get_filter(move_code[1])
    else:
        filter_squares = ALL_SQUARES

    destination_str = move_code[-2:]
    if destination_str[0] in FILES and destination_str[1] in RANKS:
        target_square = str2bb(destination_str)
    else:
        return False

    if len(move_code) == 2:
        piece = PIYON
    else:
        piece_code = move_code[0]
        if piece_code in FILES:
            piece = PIYON
            filter_squares = get_filter(piece_code)
        elif piece_code in TAS_KODLARI:
            piece = TAS_KODLARI[piece_code] & PIECE_MASK
        else:
            return False

    valid_moves = []
    for move in legal_moves(game, game.to_move):
        if move[1] & target_square and \
                move[0] & filter_squares and \
                get_piece(game.board, move[0]) & PIECE_MASK == piece:
            valid_moves.append(move)

    if len(valid_moves) == 1:
        return valid_moves[0]
    else:
        return False


def get_player_move(game):
    move = None
    while not move:
        move = parse_move_code(game, input())
        if not move:
            print('Invalid move!')
    return move


def get_AI_move(game, depth=2):
    if verbose:
        print('Searching best move for BEYAZ...' if game.to_move == BEYAZ else 'Searching best move for SIYAH...')
    start_time = time()

    if find_in_book(game):
        move = get_book_move(game)
    else:
        #         move = minimax(game, game.to_move, depth)[0]
        move = alpha_beta(game, game.to_move, depth)[0]

    end_time = time()
    if verbose:
        print('Found move ' + TAS_KODLARI[get_piece(game.board, move[0])] + ' from ' + str(
            bb2str(move[0])) + ' to ' + str(bb2str(move[1])) + ' in {:.3f} seconds'.format(
            end_time - start_time) + ' ({},{})'.format(evaluate_game(game), evaluate_game(make_move(game, move))))
    return move


def print_outcome(game):
    print(get_outcome(game))


def get_outcome(game):
    if is_stalemate(game):
        return 'Draw by stalemate'
    if is_checkmate(game, BEYAZ):
        return 'SIYAH wins!'
    if is_checkmate(game, SIYAH):
        return 'BEYAZ wins!'
    if has_insufficient_material(game):
        return 'Draw by insufficient material!'
    if is_under_75_move_rule(game):
        return 'Draw by 75-move rule!'


def play_as_BEYAZ(game=Game()):
    print('Playing as BEYAZ!')
    while True:
        print_board(game.board)
        if game_ended(game):
            break

        game = make_move(game, get_player_move(game))

        print_board(game.board)
        if game_ended(game):
            break

        game = make_move(game, get_AI_move(game))
    print_outcome(game)


def play_as_SIYAH(game=Game()):
    print('Playing as SIYAH!')
    while True:
        print_rotated_board(game.board)
        if game_ended(game):
            break

        game = make_move(game, get_AI_move(game))

        print_rotated_board(game.board)
        if game_ended(game):
            break

        game = make_move(game, get_player_move(game))
    print_outcome(game)


def watch_AI_game(game=Game(), sleep_seconds=0):
    print('Watching AI-vs-AI game!')
    while True:
        print_board(game.board)
        if game_ended(game):
            break

        game = make_move(game, get_AI_move(game))
        sleep(sleep_seconds)
    print_outcome(game)


def play_as(renk):
    if renk == BEYAZ:
        play_as_BEYAZ()
    if renk == SIYAH:
        play_as_SIYAH()


def play_random_renk():
    renk = choice([BEYAZ, SIYAH])
    play_as(renk)


def find_in_book(game):
    if game.position_history[0] != INITIAL_FEN:
        return False

    openings = []
    book_file = open("hamleler.txt")
    for line in book_file:
        if line.startswith(game.get_move_list()) and line.rstrip() > game.get_move_list():
            openings.append(line.rstrip())
    book_file.close()
    return openings


def get_book_move(game):
    openings = find_in_book(game)
    chosen_opening = choice(openings)
    next_moves = chosen_opening.replace(game.get_move_list(), '').lstrip()
    move_str = next_moves.split(' ')[0]
    move = [str2bb(move_str[:2]), str2bb(move_str[-2:])]
    return move



