# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 18:01:34 2018

@author: Mateusz Rechnio

MIT License

Copyright (c) 2018 Mateusz Rechnio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#Tree module allowing segmentation of image
#Image have to be presented as matrix of pixels

import math

class Coords(object):
    """
    Class containing coordinates of sub-matrix
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_end = x + width
        self.y_end = y + height
    
    def __str__(self):
        return "\nx: " + str(self.x) + " - " + str(self.x_end) + "\n" + "y: " + str(self.y) + " - " + str(self.y_end)

#------------------------------------------------------------------------------

class Node(object):
    """
    Class representing single node of a tree
    idt - id of node
    parent - parent node
    coords - coordinates of sub-matrix represented by node
    children - children of a node
    """
    def __init__(self, idt, level, parent, coords):
        self.idt = idt
        self.level = level
        self.parent = parent
        self.coords = coords
        self.children = []
        
    def __str__(self):
        children_id = ()
        for child in self.children:
            children_id += (child.idt,)
        
        string = "Node: " + str(self.idt) + "\n" + "Level:" + str(self.level) + "\n" + "Coordinates: " + str(self.coords) + "\n"
        
        if (self.parent != None):
            return string + "Parent: " + str(self.parent.idt) + "\n" + "Children id: " + str(children_id) + "\n"
        else:
            return string + "Parent: None" + "\n" + "Children id: " + str(children_id) + "\n"
    
    def AddChild(self, node):
        self.children.append(node)

#------------------------------------------------------------------------------
        
class Tree(object):
    """
    Tree containing all of sub-matrices
    root - first node
    image - image in form of matrix
    alpha - factor of tolerable aberrancy 
        from average color of sub-matrix
    strTree - string representing text form of tree
    globalIndex - index of nodes
    minWidth - minimum width of sub-matrix
    minHeight - minimum height of sub-matrix
    minLevel - factor representing how many nodes 
        won't be checked for coherence
    """
    def __init__(self, root, image):
        self.root = root
        self.image = image
        self.__alpha__ = 0
        self.__strTree__ = ""
        self.__globalIndex__ = root.idt
        self.__minWidth__ = 1
        self.__minHeight__ = 1
        self.__minLevel__ = 0
        
    def __recursivelyToString__(self, node):
        """
        Fills strTree
        """
        if(len(node.children) != 0):
            for child in node.children:
                self.__strTree__ += str(child) + "\n"
                self.__recursivelyToString__(child)
    
    def __str__(self):
        self.__recursivelyToString__(self.root)
        string = self.__strTree__
        self.__strTree__=""
        return str(self.root) + "\n" + string
    
    def setMinWidthAndHeight(self, min_width, min_height):
        """
        Sets minimum width and height of sub-matrix
        """
        self.__minWidth__ = min_width
        self.__minHeight__ = min_height
        
    def setAlpha(self, alpha):
        """
        Set factor of tolerable aberrancy 
        from average color of sub-matrix
        """
        self.__alpha__ = alpha
        
    def setMinLevel(self, level):
        """
        Sets how many nodes won't be checked for coherence
        """
        self.__minLevel__  = level
    
    def recursivelyFillTree(self, width, height, parent):
        """
        Fills tree recursively and modifies image
        """
        w_ceil = math.ceil(width / 2)
        w_floor = math.floor(width / 2)
        h_ceil = math.ceil(height / 2)
        h_floor = math.floor(height / 2)
        
        average = self.__averagePixelColor__(width, height, parent)
        
        if(parent.level >= self.__minLevel__):
            if(self.__checkNodeCoherence__(width, height, parent, average) and (width >= self.__minWidth__ or height >= self.__minHeight__)):
                self.__createNextLevel__(parent, w_floor, w_ceil, h_floor, h_ceil)
            else:
                for row in range(parent.coords.y, parent.coords.y + height):
                    for col in range(parent.coords.x, parent.coords.x + width):
                        self.image[row][col] = average
        else:
            self.__createNextLevel__(parent, w_floor, w_ceil, h_floor, h_ceil)
    
    def __createNextLevel__(self, parent, w_floor, w_ceil, h_floor, h_ceil):
        """
        Fills next level of tree, adding new children
        """
        if(w_floor != 0 and h_floor != 0):
            self.__extendTree4__(parent, 
                                 [parent.coords.x, parent.coords.y, w_ceil, h_ceil], 
                                 [parent.coords.x + w_ceil, parent.coords.y, w_floor, h_ceil], 
                                 [parent.coords.x, parent.coords.y + h_ceil, w_ceil, h_floor], 
                                 [parent.coords.x + w_ceil, parent.coords.y + h_ceil, w_floor, h_floor])
        elif(w_ceil == 1 and h_floor != 0):
            self.__extendTree2__(parent,
                                 [parent.coords.x, parent.coords.y, 1, h_ceil],
                                 [parent.coords.x, parent.coords.y + h_ceil, 1, h_floor])
        elif(h_ceil == 1 and w_floor != 0):
            self.__extendTree2__(parent,
                                 [parent.coords.x, parent.coords.y, w_ceil, 1],
                                 [parent.coords.x + w_ceil, parent.coords.y, w_floor, 1])
    
    def __extendTree4__(self, parent, child1, child2, child3, child4):
        """
        Adds 4 children to the node
        """
        
        level = parent.level + 1
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child1[0], child1[1], child1[2], child1[3])))
        self.recursivelyFillTree(child1[2], child1[3], parent.children[0])
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child2[0], child2[1], child2[2], child2[3])))
        self.recursivelyFillTree(child2[2], child2[3], parent.children[1])
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child3[0], child3[1], child3[2], child3[3])))
        self.recursivelyFillTree(child3[2], child3[3], parent.children[2])
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child4[0], child4[1], child4[2], child4[3])))
        self.recursivelyFillTree(child4[2], child4[3], parent.children[3])
    
    def __extendTree2__(self, parent, child1, child2):
        """
        Adds 2 children to the node
        """
        
        level = parent.level + 1
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child1[0], child1[1], child1[2], child1[3])))
        self.recursivelyFillTree(child1[2], child1[3], parent.children[0])
        
        self.__globalIndex__ += 1
        parent.AddChild(Node(self.__globalIndex__, level, parent, Coords(child2[0], child2[1], child2[2], child2[3])))
        self.recursivelyFillTree(child2[2], child2[3], parent.children[1])
    
    def __averagePixelColor__(self, width, height, parent):
        """
        Calculates average color of sub-matrix
        """
        pixels_sum = [0, 0, 0]
        counter = 0
        for row in range(parent.coords.y, parent.coords.y + height):
            for col in range(parent.coords.x, parent.coords.x + width):
                pixel = self.image[row][col]
                pixels_sum[0] += pixel[0]
                pixels_sum[1] += pixel[1]
                pixels_sum[2] += pixel[2]
                counter += 0
                
        pixels_sum[0] = int(pixels_sum[0] / (width * height))
        pixels_sum[1] = int(pixels_sum[1] / (width * height))
        pixels_sum[2] = int(pixels_sum[2] / (width * height))
            
        pixels_sum = (pixels_sum[0], pixels_sum[1], pixels_sum[2])
        return pixels_sum
    
    def __checkPixelCoherence__(self, pixel, average):
        """
        Checks if single pixel is coherent
        """
        avg = 255 * (self.__alpha__ / 100)
        counter = 0
        
        for i in range(len(average)):
            if(average[i] + avg > pixel[i] and average[i] - avg < pixel[i]):
                counter += 1
        
        if(counter == 3):
            return True
        else:
            return False
    
    def __checkNodeCoherence__(self, width, height, parent, average):
        """
        Checks if current sub-matrix is coherent
        """
        for row in range(parent.coords.y, parent.coords.y + height):
            for col in range(parent.coords.x, parent.coords.x + width):
                pixel = self.image[row][col]
                
                if(self.__checkPixelCoherence__(pixel, average)):
                    return False
                else:
                    return True