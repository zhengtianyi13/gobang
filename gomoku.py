
from copy import deepcopy  # you may use this for copying a board
import re


def newGame(player1, player2):
    '''
    创建一个新的游戏
    创建游戏状态字典
    '''
    return {
        'player1': player1,
        'player2': player2,
        'who': 1,
        'board': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
    }



def printBoard(board):
    """
    打印棋盘的函数
    
    """
    print("   | a | b | c | d | e | f | g | h |")
    print("   +---+---+---+---+---+---+---+---+")
    num = 1
    for i in board:
        print(" %d |" % num, end="")
        for j in i:
            if j == 0:
                print("   |", end="")
            elif j == 1:
                print(" X |", end="")
            else:
                print(" O |", end="")
        print("", end="\n")
        num = num + 1
    print("   +---+---+---+---+---+---+---+---+")

    return


def posToIndex(s):
    """
    棋盘位置转数组序号
    """
    try:
        s = s.lstrip()  #Remove space
        regex1 = '[1-8]([a-h]|[A-H])'  #Regular expression matches the corresponding chessboard position
        regex2 = '([a-h]|[A-H])[1-8]'

        if len(s) != 2:
            raise ValueError

        if re.match(regex1, s):

            if ord(s[1]) > 96:
                return (int(s[0]) - 1, int(chr(ord(s[1]) - 49)))
            else:
                return (int(s[0]) - 1, int(chr(ord(s[1]) - 17)))

        elif re.match(regex2, s):

            if ord(s[0]) > 96:
                return (int(s[1]) - 1, int(chr(ord(s[0]) - 49)))

            else:
                return (int(s[1]) - 1, int(chr(ord(s[0]) - 17)))

        else:
            raise ValueError

    except ValueError as e:

        print('The value entered does not conform to the specification', e)


def indexToPos(t):
    """
    序号转棋盘位置
    """
    s2 = str(t[0] + 1)
    s1 = chr(t[1] + 97)
    return s1 + s2


def loadGame(filename):
    """
    加载txt文件的游戏
    """
    game = {}

    try:
        with open(filename, encoding='utf-8') as f:

            line1 = f.readline()[:-1]
            line2 = f.readline()[:-1]
            line3 = f.readline()[:-1]

            if line1 == "":  #Player name is not empty
                raise ValueError
            if line2 == "":

                raise ValueError
            if line3 not in ['1', '2']:

                raise ValueError

            game['player1'] = line1
            game['player2'] = line2
            game['who'] = line3

            board = []

            for i in range(8):
                line = f.readline().replace('\n', '').split(',')

                num = 0
                for j in line:
                    if j not in ['0', '1', '2']:
                        raise ValueError
                    else:
                        line[num] = int(j)
                        num = num + 1
                if len(line) != 8:
                    raise ValueError
                board.append(line)
            game['board'] = board
            return game

    except ValueError as ve:

        print('The format of the read in file is incorrect', ve)

    except FileNotFoundError:

        print(f"Sorry, the file {filename} does not exist.")


def getValidMoves(board):
    """
    获得可行的移动位置
    """

    vaildmoves = []
    for iindex, i in enumerate(board):
        for jindex, j in enumerate(i):
            if j == 0:
                vaildmoves.append((iindex, jindex))

    return vaildmoves


def makeMove(board, move, who):
    """
    下棋函数
    """

    i = move[0]
    j = move[1]
    board[i][j] = who
    return board


def hasWon(board, who):
    """
    判断是否获胜
    """

    # Horizontal scanning
    for r in board:
        continu1 = 0
        for n in r:
            if n == who:
                continu1 = continu1 + 1
                if continu1 == 5:
                    return True
            else:
                continu1 = 0

    # Vertical scanning
    for c in range(8):
        continu2 = 0
        for r in range(8):
            if board[r][c] == who:
                continu2 = continu2 + 1
                if continu2 == 5:
                    return True
            else:
                continu2 = 0

    #Top left to bottom right

    for n in range(4):
        continu3 = 0
        for m in range(8 - n):
            if board[n + m][m] == who:
                continu3 = continu3 + 1
                if continu3 == 5:
                    return True
            else:
                continu3 = 0

    #Top right to bottom left

    for n in range(4, 8):
        continu4 = 0
        for m in range(n + 1):
            if board[n - m][m] == who:
                continu4 = continu4 + 1
                if continu4 == 5:
                    return True
            else:
                continu4 = 0

    return False


def suggestMove1(board, who):
    """
    简单的五子棋AI
    """

    #Condition 1, the way to win immediately
    Validmoveslist = getValidMoves(board)

    for i in Validmoveslist:
        board2 = deepcopy(board)
        board2 = makeMove(board2, i, who)
        if hasWon(board2, who):
            return i

    #Condition 2, prevent the opponent from winning
    enemy = 2 if who == 1 else 1

    for i in Validmoveslist:
        board2 = deepcopy(board)
        board2 = makeMove(board2, i, enemy)
        if hasWon(board2, enemy):
            return i

    #If the above conditions are not met, return to the first position in the list
    return Validmoveslist[0]

#---------------TASK 11-------------------------------------


def has4(board, who):
    """
   判断是否4子连珠
    """

    # Horizontal judgement
    for r in board:
        continu1 = 0
        for n in r:
            if n == who:
                continu1 = continu1 + 1
                if continu1 == 4:
                    return True
            else:
                continu1 = 0

    # Vertical judgement
    for c in range(8):
        continu2 = 0
        for r in range(8):
            if board[r][c] == who:
                continu2 = continu2 + 1
                if continu2 == 4:
                    return True
            else:
                continu2 = 0

    #Top left to bottom right
    for n in range(4):
        continu3 = 0
        for m in range(8 - n):
            if board[n + m][m] == who:
                continu3 = continu3 + 1
                if continu3 == 4:
                    return True
            else:
                continu3 = 0

    #Top right to bottom left
    for n in range(4, 8):
        continu4 = 0
        for m in range(n + 1):
            if board[n - m][m] == who:
                continu4 = continu4 + 1
                if continu4 == 4:
                    return True
            else:
                continu4 = 0

    return False


def hasself(board, pos, who):
    """
    判断一个棋子周边是否有相同的棋子
    """
    i = pos[0]
    j = pos[1]

    #If the current position is at the edge of the chessboard, return (- 1, - 1)
    if i in [0, 7]:
        return (-1, -1)
    if j in [0, 7]:
        return (-1, -1)

    #Are there any adjacent pieces in the horizontal direction
    if i <= 6 and board[i + 1][j] == who:
        return (i, j)

    if i >= 1 and board[i - 1][j] == who:
        return (i, j)

    #Are there any adjacent pieces in the vertical row
    if j <= 6 and board[i][j + 1] == who:
        return (i, j)

    if j >= 1 and board[i][j - 1] == who:
        return (i, j)

    #Oblique
    if i <= 6 and j <= 6 and board[i + 1][j + 1] == who:
        return (i, j)

    if i >= 1 and j >= 1 and board[i - 1][j - 1] == who:
        return (i, j)

    return (-1, -1)


def suggestMove2(board, who):
    """
    加强AI
    """

    #Condition 1, the way to win immediately
    Validmoveslist = getValidMoves(board)

    for i in Validmoveslist:
        board2 = deepcopy(board)
        board2 = makeMove(board2, i, who)
        if hasWon(board2, who):
            return i

    #Condition 2, prevent the opponent from winning
    enemy = 2 if who == 1 else 1

    for i in Validmoveslist:
        board2 = deepcopy(board)
        board2 = makeMove(board2, i, enemy)
        if hasWon(board2, enemy):
            return i

    #Add new conditions to prevent rivals from forming four in a row
    for i in Validmoveslist:
        board2 = deepcopy(board)
        board2 = makeMove(board2, i, enemy)
        if has4(board2, enemy):
            return i

    #Try to get down near your own chess pieces
    pos1 = Validmoveslist[len(Validmoveslist) //
                          2]  #Try to play chess in the middle
    for i in Validmoveslist:
        board2 = deepcopy(board)
        pos = hasself(board2, i, who)
        if pos != (-1, -1):
            return pos

    return (pos1[0], pos1[1] + 3)


# ------------------- Main function --------------------
def play():
    """ 
    主函数
    """
    print("*" * 55)
    print("***" + " " * 8 + "WELCOME TO GOMOKU!" + " " * 8 + "***")
    print("*" * 55, "\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")

    player1 = ""
    player2 = ""
    flag = 0

    while not player1:
        player1 = input("Please enter a non empty player1 name: ")
        player1 = player1.strip()

    if player1 == 'L':
        flag = 1
        while 1:
            filename = input(
                "Please enter the game file you want to load: ").lstrip()
            if filename == "":
                filename = 'game.txt'
            game = loadGame(filename)
            if game is not None:
                print("Game loaded successfully")
                break
    else:
        while not player2:
            player2 = input("Please enter a non empty player2 name: ")
            player2 = player2.strip()

    print("Now let's start the game. Below is the chessboard\n")

    if flag == 0:
        game = newGame(player1, player2)
    printBoard(game['board'])
    game['who'] = int(game['who'])

    while 1:
        nowplayer = game['who']
        player = game['player1'] if nowplayer == 1 else game['player2']
        board = game["board"]
        print(f"Now is player{nowplayer}:{player}'s turn\n")
        if player == 'C':
            board = makeMove(board, suggestMove2(board, nowplayer), nowplayer)
        else:
            while 1:
                pos = input(
                    "Please select the location where you want to put your chess : "
                )
                index = posToIndex(pos)
                if index not in getValidMoves(board):
                    print("The position you entered is incorrect")
                else:
                    break
            board = makeMove(board, index, nowplayer)

        printBoard(board)

        if hasWon(board, nowplayer):
            print(f"player{nowplayer}:{player} win !!!!")
            break

        if len(getValidMoves(board)) == 0:
            print("game draw !!!")
            break

        game["who"] = 2 if nowplayer == 1 else 1
        game['board'] = board


if __name__ == '__main__' or __name__ == 'builtins':
    play()
