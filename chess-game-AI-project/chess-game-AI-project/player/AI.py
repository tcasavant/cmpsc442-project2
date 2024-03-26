from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked':
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def checkmate_on_white(self,gametiles):
        movex=move()
        if self.is_king_in_check(gametiles, 'White'):
        # if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

    def checkmate_on_black(self,gametiles):
        movex=move()
        if self.is_king_in_check(gametiles, 'Black'):
        # if movex.checkb(gametiles)[0]=='checked':
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr

    pst = {
        # 'p': [[ 0,  0,  0,  0,  0,  0,  0,  0],
        #       [ 0, 50, 50, 50, 50, 50, 50, 50],
        #       [ 0, 10, 20, 30, 30, 20, 10, 10],
        #       [ 5,  5, 10, 25, 25, 10,  5,  5],
        #       [ 0,  0,  0, 20, 20,  0,  0,  0],
        #       [ 5, -5,-10,  0,  0,-10, -5,  5],
        #       [ 5, 10, 10,-20,-20, 10, 10,  5],
        #       [ 0,  0,  0,  0,  0,  0,  0,  0]],
        'p': [[20,  25,  30,  35,  35,  30,  25,  20],
              [ 5,  10,  15,  20,  20,  15,  10,   5],
              [ 4,   8,  12,  16,  16,  12,   8,   4],
              [ 3,   6,   9,  12,  12,   9,   6,   3],
              [ 2,   4,   6,   8,   8,   6,   4,   2],
              [ 1,   2,   3, -10, -10,   3,   2,   1],
              [ 0,   0,   0, -40, -40,   0,   0,   0],
              [ 0,   0,   0,   0,   0,   0,   0,   0]],

        # 'n': [[-50,-40,-30,-30,-30,-30,-40,-50],
        #       [-40,-20,  0,  0,  0,  0,-20,-40],
        #       [-30,  0, 10, 15, 15, 10,  0,-30],
        #       [-30,  5, 15, 20, 20, 15,  5,-30],
        #       [-30,  0, 15, 20, 20, 15,  0,-30],
        #       [-30,  5, 10, 15, 15, 10,  5,-30],
        #       [-40,-20,  0,  5,  5,  0,-20,-40],
        #       [-50,-40,-30,-30,-30,-30,-40,-50]],
        'n': [[-10, -10, -10, -10, -10, -10, -10, -10],
              [-10,   0,   0,   0,   0,   0,   0, -10],
              [-10,   0,   5,   5,   5,   5,   0, -10],
              [-10,   0,   5,  10,  10,   5,   0, -10],
              [-10,   0,   5,  10,  10,   5,   0, -10],
              [-10,   0,   5,   5,   5,   5,   0, -10],
              [-10,   0,   0,   0,   0,   0,   0, -10],
              [-10, -30, -10, -10, -10, -10, -30, -10]],

        # 'b': [[-20,-10,-10,-10,-10,-10,-10,-20],
        #       [-10,  0,  0,  0,  0,  0,  0,-10],
        #       [-10,  0,  5, 10, 10,  5,  0,-10],
        #       [-10,  5,  5, 10, 10,  5,  5,-10],
        #       [-10,  0, 10, 10, 10, 10,  0,-10],
        #       [-10, 10, 10, 10, 10, 10, 10,-10],
        #       [-10,  5,  0,  0,  0,  0,  5,-10],
        #       [-20,-10,-10,-10,-10,-10,-10,-20]],
        'b': [[-10, -10, -10, -10, -10, -10, -10, -10],
              [-10,   0,   0,   0,   0,   0,   0, -10],
              [-10,   0,   5,   5,   5,   5,   0, -10],
              [-10,   0,   5,  10,  10,   5,   0, -10],
              [-10,   0,   5,  10,  10,   5,   0, -10],
              [-10,   0,   5,   5,   5,   5,   0, -10],
              [-10,   0,   0,   0,   0,   0,   0, -10],
              [-10, -10, -20, -10, -10, -20, -10, -10]],

        'r': [[  0,  0,  0,  0,  0,  0,  0,  0],
              [  5, 10, 10, 10, 10, 10, 10,  5],
              [ -5,  0,  0,  0,  0,  0,  0, -5],
              [ -5,  0,  0,  0,  0,  0,  0, -5],
              [ -5,  0,  0,  0,  0,  0,  0, -5],
              [ -5,  0,  0,  0,  0,  0,  0, -5],
              [ -5,  0,  0,  0,  0,  0,  0, -5],
              [  0,  0,  0,  5,  5,  0,  0,  0]],

        'q': [[-20,-10,-10, -5, -5,-10,-10,-20],
              [-10,  0,  0,  0,  0,  0,  0,-10],
              [-10,  0,  5,  5,  5,  5,  0,-10],
              [ -5,  0,  5,  5,  5,  5,  0, -5],
              [  0,  0,  5,  5,  5,  5,  0, -5],
              [-10,  5,  5,  5,  5,  5,  0,-10],
              [-10,  0,  5,  0,  0,  0,  0,-10],
              [-20,-10,-10, -5, -5,-10,-10,-20]],

        # 'k': [[-30,-40,-40,-50,-50,-40,-40,-30],
        #       [-30,-40,-40,-50,-50,-40,-40,-30],
        #       [-30,-40,-40,-50,-50,-40,-40,-30],
        #       [-30,-40,-40,-50,-50,-40,-40,-30],
        #       [-20,-30,-30,-40,-40,-30,-30,-20],
        #       [-10,-20,-20,-20,-20,-20,-20,-10],
        #       [ 20, 20,  0,  0,  0,  0, 20, 20],
        #       [ 20, 30, 10,  0,  0, 10, 30, 20]],
        'k': [[-40, -40, -40, -40, -40, -40, -40, -40],
              [-40, -40, -40, -40, -40, -40, -40, -40],
              [-40, -40, -40, -40, -40, -40, -40, -40],
              [-40, -40, -40, -40, -40, -40, -40, -40],
              [-40, -40, -40, -40, -40, -40, -40, -40],
              [-40, -40, -40, -40, -40, -40, -40, -40],
              [-20, -20, -20, -20, -20, -20, -20, -20],
              [  0,  20,  40, -20,   0, -20,  40,  20]],

        'k_end': [[  0,  10,  20,  30,  30,  20,  10,   0],
                  [ 10,  20,  30,  40,  40,  30,  20,  10],
                  [ 20,  30,  40,  50,  50,  40,  30,  20],
                  [ 30,  40,  50,  60,  60,  50,  40,  30],
                  [ 30,  40,  50,  60,  60,  50,  40,  30],
                  [ 20,  30,  40,  50,  50,  40,  30,  20],
                  [ 10,  20,  30,  40,  40,  30,  20,  10],
                  [  0,  10,  20,  30,  30,  20,  10,   0]]
    }

    # cur_val defaults to over 1200, only used when checking the king piece to see if it is in endgame
    def piece_square_value(self, piece, x, y, cur_val=10000):
        # Get the value from the piece-square table based on the piece type and position
        if piece.alliance == 'White':
            if piece.tostring().lower() == 'k' and cur_val < 1200:
                return self.pst['k_end'][y][x]
            return self.pst[piece.tostring().lower()][y][x]
        else:
            if piece.tostring().lower() == 'k' and cur_val < 1200:
                return self.pst['k_end'][7-y][x]
            return self.pst[piece.tostring().lower()][7-y][x]

    def is_king_in_check(self, gametiles, color):
        # Find the king's position
        king_position = None
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece.tostring().lower() == 'k' and piece.alliance == color:
                    king_position = (x, y)
                    break
            if king_position:
                break

        if king_position is None:
            # King not found (likely due to incorrect board state)
            return False

        # Check for attacks on the king
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece.alliance is not None and piece.alliance != color:
                    legal_moves = piece.legalmoveb(gametiles)
                    if legal_moves is not None and king_position in legal_moves:
                        # King is in check
                        return True

        # King is not in check
        return False


    def calculateb(self,gametiles):
        value=0

        for x in range(8):
            for y in range(8):

                ## Pawn ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='p':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 100 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # # Doubled pawns: Two pawns in same column
                    # for yp in range(8):
                    #     if yp != y and gametiles[yp][x].pieceonTile.tostring() == gametiles[y][x].pieceonTile.tostring():
                    #         piece_value = piece_value - 10


                    # # Isolated pawns: No pawns of same color in neighboring column
                    # isolated = True
                    # if x != 0:
                    #     xp = x - 1
                    #     for yp in range(8):
                    #         if gametiles[yp][xp].pieceonTile.tostring() == gametiles[y][x].pieceonTile.tostring():
                    #             isolated = False
                    # if x != 7:
                    #     xp = x + 1
                    #     for yp in range(8):
                    #         if gametiles[yp][xp].pieceonTile.tostring() == gametiles[y][x].pieceonTile.tostring():
                    #             isolated = False
                    # if isolated:
                    #     piece_value = piece_value - 10


                    # # Blocked pawns: Another piece directly in front of pawn and can't take to the diagonal
                    # if gametiles[y][x].pieceonTile.alliance == 'White' and (y == 8 or gametiles[y+1][x].pieceonTile.alliance != None):
                    #     piece_value = piece_value - 10
                    # elif gametiles[y][x].pieceonTile.alliance == 'Black' and (y == 0 or gametiles[y-1][x].pieceonTile.alliance != None):
                    #     piece_value = piece_value - 10


                    # # Add checks for pawn shelter
                    # if gametiles[y][x].pieceonTile.alliance == 'White':
                    #     # Check for pawn shelter
                    #     if (y > 1 and gametiles[y-1][x].pieceonTile.tostring() == 'p' and
                    #         gametiles[y-2][x].pieceonTile.tostring().lower() == 'p'):
                    #         piece_value += 20

                    # elif gametiles[y][x].pieceonTile.alliance == 'Black':
                    #     # Check for pawn shelter
                    #     if (y < 6 and gametiles[y+1][x].pieceonTile.tostring() == 'P' and
                    #         gametiles[y+2][x].pieceonTile.tostring() == 'P'):
                    #         piece_value += 20


                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='P'):
                        piece_value = piece_value * -1
                    value = value + piece_value

                ## Knight ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='n':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 320 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='N'):
                        piece_value = piece_value * -1
                    value = value + piece_value

                ## Bishop ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='b':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 330 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='B'):
                        piece_value = piece_value * -1
                    value = value + piece_value

                ## Rook ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='r':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 500 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='R'):
                        piece_value = piece_value * -1
                    value = value + piece_value

                ## Queen ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='q':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 900 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='Q'):
                        piece_value = piece_value * -1
                    value = value + piece_value

                ## King ##
                if gametiles[y][x].pieceonTile.tostring().lower()=='k':
                    piece_value = 0

                    # Base piece value
                    piece_value=piece_value + 20000 + self.piece_square_value(gametiles[y][x].pieceonTile, x, y, value)

                    # Mobility score
                    # legal_moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    # if legal_moves != None:
                    #     piece_value = piece_value + 50*len(legal_moves)


                    # # Check is bad
                    # if self.is_king_in_check(gametiles, 'White') or self.is_king_in_check(gametiles, 'Black'):
                    #     piece_value = piece_value - 50

                    # Checkmate is bad
                    if self.checkmate_on_black(gametiles):
                        piece_value = 100000
                    elif self.checkmate_on_white(gametiles):
                        piece_value = -100000

                    # Make the value negative if it is the opponents piece
                    if (gametiles[y][x].pieceonTile.tostring()=='K'):
                        piece_value = piece_value * -1
                    value = value + piece_value


        return value


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
