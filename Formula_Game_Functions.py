"""
# Copyright Nick Cheng 2016, 2018
# Copyright Tony Attalla 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.
# GLOBALS
# operators is a list that contains all the binary operators,
# referred to in the functions
operators = '*+'
# priority is a dictionary that maps operators to their respective priorities
# this works the same way as it does in regular mathematics but the brackets have the lowest
# priority because they only indicate the beginning of a subexpression
symbol_to_priority = {}
symbol_to_priority['*'] = 3
symbol_to_priority['+'] = 2
symbol_to_priority['-'] = 4
symbol_to_priority['('] = 1
letters = 'abcdefghijklmnopqrstuvwxyz'
def find_root(infix):
    '''(str) -> int
    REQ: infix is an equation in infix notation
    Takes an equation in infix notation represented by infix and returns 
    the root of that formula. find_root is a helper function that's gonna
    be called by validate. It operates by using a theorem that the root
    of any infix equation is the operator that is found when the difference
    between the number of open brackets and closed brackets is 1. To see
    a rigorous proof send me an email (don't).
    >>> find_root('(a+b)')
    2
    >>> find_root('((a+b)*(x*y))')
    6
    >>> find_root('a+b')
    -1
    '''
    # initailzing a boolean that's gonna tell us when
    # we found the root so I know to stop checking 
    # the conditions of the for loop
    rootFound = False
    # initializng two variables that are gonna keep track of how 
    # many open and closed brackets we've encountered so far
    (right_brackets,left_brackets) = (0,0)
    #initiallzing a variable that's gonna tell us where the root
    # is relative to the string. Set to -1 initially because we don't want
    # to asume that the equation contains a operator anyways
    rootIndex = -1
    # this loop runs through the equation to try to locate the root
    for i in range(0,len(infix)):
        # we only want to run the conditions of the loop
        # while we haven't found an operator (it would make
        # no sense if we've already found the root )
        if rootFound == False:
            # if we encounter open or closed brackets, we need
            # to increment the variables to keep track of how many
            # we have
            if infix[i] == '(':
                left_brackets +=1
            elif infix[i] == ')':
                right_brackets +=1
            # moment of truth. If we've found a operator
            # (+ or *)
            elif infix[i] in operators:
                # if the difference between the left and right
                # brackets is 1 when we've found an operator
                # we know we're at the index of the operator
                if left_brackets-right_brackets == 1:
                    # so, we know that we've found the root
                    # and the index of the root is the index
                    # that we're currently looking at 
                    rootFound = True
                    rootIndex = i
    # return the index of the root. Note that if we haven't found 
    # a root the function will return -1 by default
    return rootIndex


    
def validate(infix):
    '''(str) -> bool
    The validate function works in tandem with find_root to  recursively validate whether
    an infix expression meets the requirements as defined by the handout to be
    a valid formula. Specifically, we can't have extraneous brackets, capital letters,
    symbols that are not boolean operators, missing brackets, and incorrect placement
    of children relative to their parent nodes.
    >>> validate('(a+b)')
    True
    >>> validate('(x*y*z)')
    False
    >>> validate('-(a+-b)'')
    True
    '''
    # the following if statement checks to make sure that the amount of open brackets
    # in the infix expression is the same as the amount of closed brackets and that 
    # the expression is not empty. (I needed a special case for this because if the string
    # is empty the function is gonna try to read the first character, causing an error)
    result = False
    if infix.count('(') == infix.count(')') and infix != '':
        # initialize a variable called result. result's gonna store 
        # whether or not the expression (or recursively, the part of the 
        # expression) we're looking at is valid or not
        # BASE CASE:
        # the base case is when the expression we're looking at is only
        # 1 character long. Fundamentally, when we break down any valid
        # formula we should get a letter (this is due to the way I handle
        # the not operator and the fact that when we go down a valid
        # tree, we should always arrive at a leaf). To see a 
        # rigourous proof paypal me 20 bucks and send me an email
        
        if len(infix) == 1:
            # if the one character is a symbol (or, easier to understand, if
            # its a leaf), we know that the expression (or at least, the current
            # subexpression) is valid
            if infix[0] in letters:
                # set our result variable to true
                result =  True
            else:
                # if the one character is an internal node where a leaf is supposed to go
                #, we know this subexpression is invalid
                result =  False
        # we need a unique way of handling nots, since they're pretty easy to take care of
        #. Essentailly, we know that if we encounter a not, the next character better be an
        # open bracket, indicating the start of another equation, or it better be a symbol
        # we're negating or another not, leading to another negation
        elif infix[0] == '-':
            if infix[1] in '(-' or infix[1] in letters:
                # if we've met the above condition, let's ignore the 
                # not and just look at the rest of the string as if
                # its not there
                infix = infix[1:]
                # recursively call the function again because
                # we've verified the positioning of the not is valid
                result = validate(infix)
            # if the not isn't negating what it should be negating,
            # we know the positioning of the not is incorrect, making
            # the whole formula invalid
            else:
                result = False
        # if we've found an open bracket, we know that there is some sub-expression contained
        # in our formula that we need to recursively evaluate because an open bracket indicates 
        # the beginning of a new formula
        elif infix[0] == '(':
            # so let's call the find_root helper to give us the position of the root we're looking
            # for
            rootIndex = find_root(infix)
            if rootIndex == -1:
                # if no root exists within the sub formula, we know that this sub formula is invalid
                # so set the result to false
                result = False
            else:
                # we need to make sure that both everything to the left of the root is valid
                # and everything to the right of the root is valid, so let's split the equation
                # into left and right, and recursively call the function on those parts.
                # use the min function to make sure that even if one side is valid and the other isn't.
                # we still know the whole formula is invalid. both sides must be valid for the whole
                # formula to be valid
                result = min(validate(infix[1:rootIndex]),validate(infix[rootIndex+1:-1]) )

    # return whether or not the formula is valid. Note that if the first condition above
    # is not met, the function won't be considered valid because result is false
    # by default
    return result


def to_postfix(infix):
    '''(str) -> str
    The to_postfix function takes an equation in infix notation
    and converts it to postfix notation. This makes constructing the tree
    a lot easier and a lot more efficient because we don't have to use
    recursion. In postfix, the operators come after the operands. The reason
    I do this will become more clear in the build_tree function
    >>> to_postfix('a+b')
    ab+
    >>> to_postfix('---a')
    a---
    >>> to_postfix('((a+b)+(a*b))')
    ab+ab*+
    '''
    # first, create an empty stack that we're gonna use to store
    # brackets and operators
    # this stack has some special properties though, when we look through 
    # a string to convert it to postfix, we want to make sure that every time we add
    # an operator to the stack, we want to remove all other operators with higher or equal priority
    # we know which operators have higher priority by the dictionary named priority, defined as a global
    # variable. It's the same as regular math, nots -> ands -> ors -> brackets
    stack = []
    # the postfix variable stores the postfix expression
    postfix = ''
    # loop through every character in the infix expression
    for character in infix:
        # if the character is an operand, just append it to the final expression
        # (because we want operands to come before operators anyways)
        if character in letters:
            # append
            postfix += character
        # assuming the character isn't an operand(so it's a bracket or operator)
        else:
            
            if character == '(' or character == '-':
                # if we're looking at an open bracket, add it to the stack. This is important
                # because later we pop from the stack until we find an open bracket. Cause
                # open brackets signify the beginning of an equation. We treat nots the same way we treat
                # an open bracket. Similar to the way open brackets indicate the beginning of an equation,
                # nots indicate that everything after the not until a close bracket will be negated
                stack.append(character)
            elif character == ')':
                # if we're looking at a right bracket, we know that we've found the end of an
                # equation, so assuming its a valid formula we will have found some operator before 
                # it.  
                operator = stack.pop()
                # keep popping from the stack and adding it to the equation until we get to
                # an open bracket, which indicates the beginning of a sub-expression
                while operator is not '(':
                    postfix += operator
                    operator = stack.pop()
            
            # if we're looking at an and or or, we need to pop operators from the stack until its empty, but we also
            # need to satisfy a second condition. We need to make sure that the operator we're looking at has less or equal
            # priority than the operator's we're removing from the stack. This is to make sure that we satisfy the order of 
            # operations for boolean logic. 
            else:
                while (not len(stack) == 0) and symbol_to_priority[character] <= symbol_to_priority[stack[-1]]:
                    postfix += stack.pop()
                # once we've made sure everything in the stack with higher priority has been added to our expression 
                # already, we can now add the current operator to the stack
                stack.append(character)
    # finally, once we've already constructed most of the expresion, take the leftover operators and add them to 
    # our final expression
    while (len(stack) != 0):
        postfix += stack.pop()
    # return the new expression in postfix notation
    return postfix

def build_tree(formula):
    '''(str) -> FormulaTree
    Takes the infix expression represented by formula 
    and outputs the corresponding formula tree. build_tree works 
    with to_postfix in order to convert an equation into postfix notation
    and then create the tree. (probably the cleanest function I've ever written)
    build_tree also uses validate to make sure that a formula is valid before 
    attempting to construct the tree.
    >>> build_tree('((a+b)*(x*m))'))
    AndTree(OrTree(Leaf('a'), Leaf('b')), AndTree(Leaf('x'), Leaf('m')))
    >>> build_tree('-a')
    NotTree(Leaf('a'))
    >>> build_tree('(a+X)')
    None
    '''
    # first, we need to validate the formula using our helper
    # validate function. If the function is valid, we can proceed 
    # constructing the tree
    if validate(formula) == True:
        # first, let's convert our equation into postfix notation
        # using our to_postfix helper function
        fixedFormula = to_postfix(formula)
       # create an empty stack that we're gonna use to store
       # sub-expressions and connect them later
        stack = []
        # looping through every character in the postfix expression
        for character in fixedFormula:
            # if we encounter an operand, make a new subtree
            #we'll make the parent-child links as we go 
            if character in letters:
                newTree = Leaf(character)
            # if we encounter an and operator, we know that 
            # we have to have a left and right child, because and 
            # is binary, so pop two characters from the stack
            # and set them to the left and right children of the 
            # AndTree we're constructing. We're guaranteed to have 
            # two or more characters in the stack because of the way 
            # postfix expression works.
            elif character == '*':
                right = stack.pop()
                left = stack.pop()
                newTree = AndTree(left,right)
            # because not is a unary operator, all we need to do 
            # is set its one child to the subexpression that's 
            # highest up in the stack
            elif character == '-':
                newTree = NotTree(stack.pop())
            # an or tree behaves the same way as an and tree, it just needs
            # its own statement because we'll be using a different type of 
            # tree 
            elif character == '+':
                right = stack.pop()
                left = stack.pop()
                newTree = OrTree(left,right)
            # no matter what kind of sub-tree we've created, we need to re-add it back onto the stack
            # so that we can later create the parent-child relationships of that tree
            stack.append(newTree)
    # in the case where the formula is invalid, we know that we can set the newTree to None and simply
    # return that valud
    else:
        newTree = None
    # return the tree represnted by the given equation
    return newTree
def evaluate(root,variables,values):
    ''' (FormulaTree, str, str) -> int
    evaluates the tree with root root with the variables of the 
    tree given by variables and the values of those variables given by
    values. evaluate works recursively to first evaluate every subtree in
    the tree and then works up the tree to evaluate the whole thing
    REQ: Variables must correspond to all leaves in the subtree
    REQ: len(values) == len(variables)
    REQ: values contains only 1's and 0's
    >>> ft = build_tree('(a+b)')
    >>> evaluate(ft, 'ab','11')
    1
    >>> ft = build_tree('(x*y)')
    >>> evaluate(ft,'xy','10')
    0
    '''
    # initialize an empty string for our value of result (doesn't really matter what data type we use here)
    result = ''
    # a dictionary to map the variables of the leaves of the formula tree to the values the user is assigning them so that we can refer
    # to them later
    variablesToValues = {}
    # loop through all the variables (we could also loop through the values but it doesnt make a difference since a REQ is that len(variables == len(values)))
    # and map the current variable to its corresponding value
    for i in range(0,len(variables)):
        variablesToValues[variables[i]] = values[i]
    #Base Case: if we get to a leaf, return the value in the dictionary that maps to that variable
    if type(root) == Leaf:
        return variablesToValues[root.get_symbol()]
    #Recursive Cases:
    # if we encounter an internal node that corresponds to an and tree we need to evaluate the minimum of the left and right subtrees. So in order for the sub-expression to evaluate
    # to true, we need both the left and right to be 1.

    elif type(root) == AndTree:
        result = min(int(evaluate(root.get_children()[0],variables,values)) , int(evaluate(root.get_children()[1],variables,values)))
    # if we encounter an internal node that corresponds to an or tree we need to evaluate the maximum of the left and right subtrees. So in order for the sub-expression to evaluate
    # to false, we need both the left and right to evaluate to 0
    elif type(root) == OrTree:
        result = max(int(evaluate(root.get_children()[0],variables,values)) ,  int(evaluate(root.get_children()[1],variables,values)))
    # if we encounter an internal node that corresponnds to a not tree, we need to subtract 1 from the value of everything below it and evaluate that
    elif type(root) == NotTree:
        result =  1 -  int(evaluate(root.get_children()[0],variables,values))

    return result
        
def draw_formula_tree_helper(root, depth,result):
    '''(FormulaTree, int, str) -> str
    A recursive helper function to draw an easier to understand, string
    representation of a formula tree. Takes two additional parameters of depth and result 
    so that the function knows how far down the tree it is and what it's drawn already. The helper
    function, however doesn't strip the output of its newline character at the end due to its recursive
    nature, so we'll do that in the body of the main function
    REQ: root is the root of a valid tree
    >>> draw_formula_tree_helper(AndTree(Leaf('a'),Leaf('b')))
    'b\\n a \\n'
    >>> draw_formula_tree_helper(NotTree(Leaf('a')))
    '- a \\n'
    '''
    #Base Case
    # assuming we've already looked at a layer of the formula tree
    # and began a new line, we need to set the appropriate depth
    # to represent how far we are into the tree
    if len(result) >= 1:
        if result[-1] == '\n':
            
            result += (' ') * 2 * depth
    
    # for every node we visit, we want to add it to the output
    result += root.get_symbol()
    # assuming we're not at a leaf, add an empty character so that we 
    # can continue going down the branch (we don't wanna add an empty character
    #if we're at a leaf because leaves indicate we're at the bottom of the tree )  
    if type(root) != Leaf:
        result += ' '
    # if we're at a not tree, proceed to draw the not symbol above and recursively draw the 
    # subtree contained within it. we also need to increment depth by 1 to indicate we've gone down
    # the tree
    if type(root) == NotTree:
            result = draw_formula_tree_helper(root.get_children()[0],depth + 1,result) 
    # if we're at an and or or tree, proceed to draw their respective symbols and do a 
    # root-right-left traversal
    if type(root) == AndTree or type(root) == OrTree:

            result = draw_formula_tree_helper(root.get_children()[1],depth+1,result) 
            result = draw_formula_tree_helper(root.get_children()[0],depth+1,result) 
    # in the case where we have a leaf, make a newline character because this indicates we've gone all the way down a branch
    if type(root) == Leaf:
        result += '\n'
    
   
    return result

def draw_formula_tree(root):
    '''(FormulaTree) -> str
    A function to draw an easier to understand, string
    representation of a formula tree. Most of the work is done by the draw_formula_tree helper function 
    but stripping newline characters is done here. The root isn't indented, children of the root are indented
    two spaces, children of those children are indented 4, etc...
    REQ: root is the root of a valid tree
    >>> draw_formula_tree_helper(AndTree(Leaf('a'),Leaf('b')))
    'b\\n a'
    >>> draw_formula_tree_helper(NotTree(Leaf('a')))
    '- a'
    '''
    # call the helper function starting with an empty string and depth 0 (because we haven't gone down the tree yet)
    result = draw_formula_tree_helper(root,0,'')
    # strip the final result of its newline character drawn at the end.
    result = result.rstrip('\n')
    return result


def play2win(root, turns, variables, values):
    '''(FormulaTree, str, str,str) -> int
    Takes the FormulaTree rooted at root, the turns to play given by turns, the variables
    players will choose given by variables, and the values chosen already given by values
    and returns the best move for the player who's turn is next. Note that the best move must 
    be a guaranteed win, and not just a good strategy. If there's no guaranteed winning strategy, return 1 for E
    and 0 for A
    REQ: There must be at least 1 move left to play
    REQ: root is the root of a valid formula tree
    REQ: Turns contains only E's and A's
    >>> t1 = build_tree('((x+y)*((y+z)*(-y+-z)))')
    >>> play2win(t1,'EEA','xyz','011')
    1
    '''
    # set the result as 1 by default (doesn't really matter if we choose 1 or 0)
    guaranteedWin = 1
    # a variable to make sure we know how many turns are left to be played
    numTurns = len(variables) - len(values)
    # for every turn left to be played, we need to make sure that there is an optimal move in every sub-expression
    # this makes it easier to figure out if there is an optimal play for the whole tree
    for i in range(0,numTurns):
        # if we have an and tree, we need to make sure there's an optimal move for both the left and right subtrees. This is because 
        # due to the structure of a basic and tree, if the opponent can choose even 1 value for themselves, the game is lost 
        if type(root) == AndTree:
            # base case, if one of  the children are leaves, return the value we've calculated for guaranteedWin
            if type(root.get_children()[0]) == Leaf or type(root.get_children()[1]) == Leaf:
                return guaranteedWin
            # recursive case, try to calculate an optimal move for the left and right subtrees
            else:
                guaranteedWin = play2win(root.get_children()[0],turns,variables,values) and  play2win(root.get_children()[1],turns,variables,values)
        # if we have an or tree, we need to make sure there's an optimal move for one of the left and right subtrees. This is because 
        # due to the structure of a basic or tree, if the opponent can choose even both values for themselves, the game is lost     
        if type(root) == OrTree:
            if type(root.get_children()[0]) == Leaf or type(root.get_children()[1]) == Leaf:
                # base case, if one of  the children are leaves, return the value we've calculated for guaranteedWin
                return guaranteedWin
            # recursive case, try to calculate an optimal move for the left and right subtrees
            else:
                guaranteedWin = play2win(root.get_children()[0],turns,variables,values) or  play2win(root.get_children()[1],turns,variables,values)

    return guaranteedWin
