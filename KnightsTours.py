from manim import *
import random
config.frame_height=16
config.frame_width=9
config.pixel_height=1920
config.pixel_width=1080
    
class MoveAroundChessboard(Scene):
    
    moves = []
    
    startSquare = 0
    
    myImage = 'images\knight_black.png'
    
    moveDiagonally = False
    showPath = True
    visitedSquareColour = ''
    
    def set_startSquare(self, i):
        self.startSquare = i
               
    def set_moves(self, listOfMoves):
        self.moves = listOfMoves
        
    def set_image(self, image):
        self.myImage = image
        
    def set_moveDiagonally(self, moveDiagonally):
        self.moveDiagonally = moveDiagonally
        
    def set_showPath(self, showPath):
        self.showPath = showPath
        
    def set_visitedSquareColour(self, visitedSquareColour):
        self.visitedSquareColour = visitedSquareColour
            
    def construct(self):
    
        unvisited_colours=['#50F6E3', '#F650B6', '#E350F6', '#9050F6', '#5063F6', '#50B6F6']
        
    
        unvisited_black = '#070B2C'
        unvisited_white = '#E6ECF2'
        visited_black = ''
        visited_white = ''
        col = random.randint(0, len(unvisited_colours)-1)
        #could have a different colour for the visited black and white squares, but keeping them the same for now.
        #I like how you can easily see how many squares haven't been visited if all the visited ones are the same colour
        if self.visitedSquareColour == '':
            visited_black = unvisited_colours[col]
            visited_white = unvisited_colours[col]
        else:
            visited_black = self.visitedSquareColour
            visited_white = self.visitedSquareColour
            
        #purples
        #visited_black = '#480E4F'
        #visited_white = '#B4A1D1'
                       
        def is_black_square(i):
            #it's a black square if:
            #i is even and i mod 16 is between 0 and 7
            #i is odd and i mod 16 is between 8 and 15
            if ((i%2==0 and (i%16)<=7) or (i%2==1 and (i%16)>7)):
                return True
            else:
                return False
                
        def set_square_colour(square, visited, i):
            if is_black_square(i):
                if visited:
                    square.set_fill(visited_black, opacity=1)
                    square.set_sheen(0.3,DR)
                else:
                    square.set_fill(unvisited_black, opacity=1)
                    square.set_sheen(-0.1,DOWN)
            else:
                if visited:
                    square.set_fill(visited_white, opacity=1)
                    square.set_sheen(0.3,DR)
                else:
                    square.set_fill(unvisited_white, opacity=1)
                    square.set_sheen(0.1,UP)
                
        def get_square_index(x, y):
            return int((x+3.5)*8+(y+3.5))
                       
        path = VMobject()
        path.set_stroke(LIGHTER_GRAY,opacity=1, width=5)
        path2 = VMobject()
        path2.set_stroke(DARK_GRAY,opacity=1, width=3)
        
        diagonal = VMobject()
        diagonal.set_stroke(WHITE,opacity=1,width=9)
        diagonal2 = VMobject()
        diagonal2.set_stroke(BLACK,opacity=1,width=5)
        
        #dot is the image of a knight that's seen onscreen
        #dot2 is an invisible circle that's used to create the diagonal lines
        dot = ImageMobject(self.myImage)
        #his scale works for horizontal aspect ratio but not vertical?
        dot.scale(0.35)
        dot2 = Circle(radius=0)
        startDot = Circle(radius=0)       
                
        #generate the chessboard       
        squares = VGroup()
        for x in range(64):
            square = Square(side_length=1)  # create a square
            set_square_colour(square, False, x)
            square.set_stroke(width=0)
            squares.add(square)
                
        squares.arrange_in_grid(row_heights=[1,1,1,1,1,1,1,1], col_widths=[1,1,1,1,1,1,1,1], row_alignments="cccccccc", col_alignments="cccccccc", buff=0, flow_order='ru')
                
        self.add(squares)
            
        dots = VGroup()
        for i in range(0,64):
            dots.add(Dot(color="#50F6E3"))
            
        dots.arrange_in_grid(row_heights=[1,1,1,1,1,1,1,1], col_widths=[1,1,1,1,1,1,1,1], row_alignments="cccccccc", col_alignments="cccccccc", buff=0, flow_order='ru')
        
        dot.move_to(dots[self.startSquare])
        dot2.move_to(dot)
        startDot.move_to(dot)
                
        #set the start square to be visited
        start_square = squares[self.startSquare]
        set_square_colour(start_square, True, self.startSquare)
               
        #path is the line that follows the moves of the knight; 2 squares one way and 1 square another. It follows dot around the board. there are two of them so that I could do a light border around the path
        path2.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path2(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path2.add_updater(update_path2)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path(path):
            #I don't know if I actually need two of these updaters, or if I can just use the same one for both paths
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        
        def reset_path(path):
            #this function resets the start and end points of the path to the knight's coordinates, which has the effect that it disappears from screen after the knight has made its move
            path.reset_points()
            path.set_points_as_corners([dot.get_center(), dot.get_center()])
        
        #diagonal is the line that follows the knight once it's finished each move, so it draws a diagonal line from the start point to the end point. It follows dot2 around the board. there are two of them so that I could do a light border around the path
        diagonal.set_points_as_corners([dot2.get_center(), dot2.get_center()])
        def update_diagonal(diagonal):
            previous_diagonal = diagonal.copy()
            previous_diagonal.add_points_as_corners([dot2.get_center()])
            diagonal.become(previous_diagonal)
        diagonal.add_updater(update_diagonal)
        diagonal2.set_points_as_corners([dot2.get_center(), dot2.get_center()])
        def update_diagonal2(diagonal):
            #I don't know if I actually need two of these updaters, or if I can just use the same one for both diagonals
            previous_diagonal = diagonal.copy()
            previous_diagonal.add_points_as_corners([dot2.get_center()])
            diagonal.become(previous_diagonal)
        diagonal2.add_updater(update_diagonal2)
        
        #add the objects that need to be visible to the scene
        for x in squares:
            self.add(x)
        if self.showPath:
            self.add(diagonal, diagonal2, path, path2)
        self.add(dot)
        self.wait()
        
        def getIntermediatePosition(fromSquare, toSquare):
            diff = toSquare - fromSquare
            print(fromSquare, toSquare, diff)
            if diff == 10 or diff == 6:
                return toSquare - 8
            if diff == 17 or diff == -15:
                return toSquare - 1
            if diff == 15 or diff == -17:
                return toSquare + 1
            if diff == -6 or diff == -10:
                return toSquare + 8
                
        
        def movePiece(self, move):
            #move the piece in the direction given
                           
            #if len(move) == 4:
                #dot.move_to(RIGHT*(-4.5+move[2])+UP*(-4.5+move[3]))
                #dot2.move_to(RIGHT*(-4.5+move[2])+UP*(-4.5+move[3]))
                                
            if self.moveDiagonally:
                self.play(dot.animate.move_to(dots[move]), run_time = 0.2)
            else:
                self.play(dot.animate.move_to(dots[getIntermediatePosition(previousPosition,move)]), run_time = 0.2)
                self.play(dot.animate.move_to(dots[move]), run_time = 0.2)
            #move the hidden knight to the position of the visible knight
            self.play(dot2.animate.move_to(dot), run_time = 0.2)
            #if I want to add a different coloured square, I should probably do it here...
            set_square_colour(squares[move], True, move)
            self.wait(0.1)
            #hide the horizontal/vertical path from this move
            reset_path(path)
            reset_path(path2)
        
        previousPosition = self.startSquare
        for move in self.moves:
            movePiece(self, move)
            previousPosition = move
            
        self.wait()
            
                
class RandomKnightsTour(MoveAroundChessboard):
    def construct(self):
    
        #set a random starting position
        startX = random.randint(1,8)
        startY = random.randint(1,8)
        
        def get_square_index(x, y):
            return int(x-1+(y-1)*8)
            
        super().set_startSquare(get_square_index(startX, startY))
    
        #generate all the moves that can be made (there is probably a better place to do this. shouldn't need to redo it every time)
        possibleMoves = []
        possibleMoves.append((UP*2, RIGHT))
        possibleMoves.append((UP*2, LEFT))
        possibleMoves.append((DOWN*2, RIGHT))
        possibleMoves.append((DOWN*2, LEFT))
        possibleMoves.append((RIGHT*2, UP))
        possibleMoves.append((RIGHT*2, DOWN))
        possibleMoves.append((LEFT*2, UP))
        possibleMoves.append((LEFT*2, DOWN))
                     
        moves = []
        squaresVisited = []
        current_x = startX
        current_y = startY
        squaresVisited.append((current_x, current_y))
        canMove = True
        while canMove == True:
        #for x in range(10):
            possibleMovesNow = possibleMoves.copy()
            while len(possibleMovesNow) > 0:
                #choose a move at random, then remove that move from the list of possible moves
                moveToDo = random.randint(0,len(possibleMovesNow)-1)
                move = possibleMovesNow[moveToDo]
                possibleMovesNow.pop(moveToDo)
                
                #work out if the selected move is allowed
                #first work out what square the knight would be at after this move
                moveTo_x = current_x + move[0][0] + move[1][0]
                moveTo_y = current_y + move[0][1] + move[1][1]
                #print ('x: ', moveTo_x, ', y: ', moveTo_y)
                #check that the new position isn't outside the bounds of the chessboard
                if(moveTo_x >= 1 and moveTo_x <= 8 and moveTo_y >= 1 and moveTo_y <= 8):
                    #check that we haven't already been to the new position
                    if not (moveTo_x, moveTo_y) in squaresVisited:
                        #we're all good. add the move to the list of moves to make and keep note of which square it ended at
                        moves.append(get_square_index(moveTo_x, moveTo_y))
                        current_x = moveTo_x
                        current_y = moveTo_y
                        squaresVisited.append((current_x, current_y))
                        break
                    else:
                        #that move is no good. are there any moves left that we haven't tried?
                        if len(possibleMovesNow) == 0:
                            #no moves left. cry
                            canMove = False
                else:
                    #that move is no good. are there any moves left that we haven't tried?
                    if len(possibleMovesNow) == 0:
                        #no moves left. cry
                        #no moves left. cry
                        canMove = False
                 
        #pass up the list of moves and run the code to generate the video
        #if len(moves) > 4 and len(moves) < 8:
        super().set_moves(moves)
        super().construct()
        
        #keep a log of how many moves were made
        f = open("knightTourLog.txt", "a")
        f.write(str(len(moves)) + "\n")
        f.close()
               
        print('The knight made ', len(moves), ' moves')
        
class RandomKnightsTours(RandomKnightsTour):
    def construct(self):
        for x in range(10000):
            super().construct()
            self.clear()
            self.next_section('My name is ' + str(x))

class DefinedTour(MoveAroundChessboard):
    def construct(self):
                        
        moves = []
        
        #read the text file
        f = open("ToursForShorts/16_FourByFourPatch.txt", "r")
        lines = f.read().splitlines()        
        #the first line is the image to use
        #second line specifies if the diagonal lines between moves should be shown (true for knight, false otherwise)
        #third line can specify the colour to use for visited squares (if not specified it will be chosen at random from a palatte)
        #read all that from the file then remove the entries
        image = lines[0]
        if int(lines[1])==1:
            moveDiagonally = True
        else:
            moveDiagonally = False
        visitedColour = str(lines[2])
        firstSquare = int(lines[3])
        for x in range(4):
            lines.pop(0)
        super().set_image(image)
        super().set_moveDiagonally(moveDiagonally)
        super().set_visitedSquareColour(visitedColour)
        super().set_startSquare(firstSquare)
                
        #each subsequent line is a number representing a square on the chessboard. squares are numbered 0 to 63, starting in the bottom left corner and reading left to right on the bottom row, right to left on the next row up, and so on
        #append each move to the list of moves
        for line in lines:
            moves.append(int(line))
        f.close()
    
        #run the knight's tour animation
        super().set_moves(moves)
        super().construct()