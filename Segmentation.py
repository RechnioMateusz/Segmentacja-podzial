# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 11:16:16 2018

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

from PIL import Image
import TreeConfiguration as tc
import os

#==============================================================================

def clearConsole():
    """
    Waits for pressing Enter button and clears console
    """
    input("\n\nPress Enter")
    os.system("cls")

def loadImageInfo():
    """
    Checks if path to image is valid and loads image
    """
    while(True):
        try:
            path = input("Path to image:\t\t")
            img = Image.open(path)
        except:
            print("\nInvalid path")
            clearConsole()
        else:
            print("\nDone")
            clearConsole()
            return (img, path)

def checkChoice():
    """
    Checks if choice is valid
    """
    try:
        choice = int(input("Your choice:\t\t"))
    except:
        print("Invalid input")
        clearConsole()
    else:
        return choice

def printActions():
    """
    Prints avalible actions to choose
    """
    print("[1]\t\tStart segmentation")
    print("[2]\t\tSet alpha")
    print("[3]\t\tSet minimum width and height of children")
    print("[4]\t\tSet minimum number of children before segmentation")
    print("[8]\t\tLoad new image")
    print("[9]\t\tReload image")
    print("[0]\t\tExit program")

def printTreeFeatures(tree):
    """
    Prints most important features of tree
    """
    print()
    print("Image width:", len(tree.image[0]))
    print("Image height:", len(tree.image))
    print("Alpha:", tree.__alpha__)
    print("Minimum width of sub-matrix:", tree.__minWidth__)
    print("Minimum height of sub-matrix:", tree.__minHeight__)
    print("Number of children before coherence check", tree.__minLevel__)
    print()

def reloadImage(tree, path):
    """
    Reloads image for further segmentation
    Saves settings
    """
    image = Image.open(path)
    width, height = image.size
    pixels = [[image.getpixel((row, col)) for row in range(width)] for col in range(height)]
    temp_alpha= tree.__alpha__
    temp_minW = tree.__minWidth__
    temp_minH = tree.__minHeight__
    temp_minL = tree.__minLevel__
    tree = tc.Tree(tc.Node(0, 0, None, tc.Coords(0, 0, width, height)), pixels)
    tree.setAlpha(temp_alpha)
    tree.setMinWidthAndHeight(temp_minW, temp_minH)
    tree.setMinLevel(temp_minL)
    return tree

def startSegmentation(tree):
    """
    Starts segmentation and saves modified image
    """
    tree.recursivelyFillTree(len(tree.image[0]), len(tree.image), tree.root)
    new_img = Image.new("RGB", (len(tree.image[0]), len(tree.image)))
    for row in range(len(tree.image)):
        for col in range(len(tree.image[0])):
            new_img.putpixel((col, row), tree.image[row][col])        
    new_img.save("output.jpg")

#==============================================================================

def main():
    os.system("cls")
    load_info = loadImageInfo()
    width, height = load_info[0].size
    pixels = [[load_info[0].getpixel((row, col)) for row in range(width)] for col in range(height)]
    tree = tc.Tree(tc.Node(0, 0, None, tc.Coords(0, 0, width, height)), pixels)
    
    while(True):
        os.system("cls")
        printActions()
        printTreeFeatures(tree)
        choice = checkChoice()
        
        if(choice == 1):
            os.system("cls")
            print("Output will be save in file named:\t\t\"output.jpg\"")
            print("\nWait a moment...")
            startSegmentation(tree)
            print("\nReloading image...")
            tree = reloadImage(tree, load_info[1])
            
        elif(choice == 2):
            os.system("cls")
            print("Alpha is a tolerable aberrancy from average color of sub-matrix (a.k.a. coherence expressed in percentage)")
            new_alpha = checkChoice()
            tree.setAlpha(new_alpha)
            
        elif(choice == 3):
            os.system("cls")
            print("Minimum width of sub-matrix")
            min_width = checkChoice()
            print("Minimum height of sub-matrix")
            min_height = checkChoice()
            tree.setMinWidthAndHeight(min_width, min_height)
            
        elif(choice == 4):
            os.system("cls")
            print("Number of children before cohrence check")
            min_number_children = checkChoice()
            tree.setMinLevel(min_number_children)
            
        elif(choice == 8):
            os.system("cls")
            load_info = loadImageInfo()
            width, height = load_info[0].size
            pixels = [[load_info[0].getpixel((row, col)) for row in range(width)] for col in range(height)]
            tree = tc.Tree(tc.Node(0, 0, None, tc.Coords(0, 0, width, height)), pixels)
            
        elif(choice == 9):
            os.system("cls")
            tree = reloadImage(tree, load_info[1])

        elif(choice == 0):
            os.system("cls")
            break
        
        else:
            print("Invalid input")
main()