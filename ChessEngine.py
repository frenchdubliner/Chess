class GameState():
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog =[]
    '''
    Takes a Move as a parameter and executes it
    '''
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0: # Make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): # number of columns in a given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls the appropriate move function based on the piece type
        return moves
    '''
    Get all the pawn moves for the pawn located at a row, col and add these moves to the list
    '''
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance on row 6
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance on row 6
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c),(r+1,c+1),self.board))


    '''
    Get all the Rook moves for the Rook located at a row, col and add these moves to the list
    '''
    def getRookMoves(self,r,c,moves):
        pass
    def getKingMoves(self,r,c,moves):
        pass
    def getQueenMoves(self,r,c,moves):
        pass
    def getKnightMoves(self,r,c,moves):
        pass
    def getBishopMoves(self,r,c,moves):
        pass



class Move():

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow*10 + self.endCol
        print(self.moveID)

    '''
    overridding the equals method
    '''

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
    
    def getChessNotation(self):
        return self.getRankFiles(self.startRow,self.startCol)+self.getRankFiles(self.endRow,self.endCol)

    def getRankFiles(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]