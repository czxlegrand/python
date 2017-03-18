# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 23:29:28 2017

@author: Administrator
"""
class Moneytree(object):
    piece = [0]*3
    def __init__(self,m,s,p):
        self.root = Node(m,p)
        self.piece[0] = s[0]
        self.piece[1] = s[1]
        self.piece[2] = s[2]
                
    def grow(self, r):
        n = r
        if n.val >= self.piece[0]:
            n.child[0] = Node(n.val - self.piece[0], n)
            if n.child[0].val > min(self.piece):
                self.grow(n.child[0])                
                
        if n.val >= self.piece[1]:
            n.child[1] = Node(n.val - self.piece[1], n)
            if n.child[1].val > min(self.piece):
                self.grow(n.child[1])
                
        if n.val >= self.piece[2]:
            n.child[2] = Node(n.val - self.piece[2], n)
            if n.child[2].val > min(self.piece):
                self.grow(n.child[2])

    def size(self,r):
        if r == None:
            return 0
        else:
            return 1 + self.size(r.child[0]) + self.size(r.child[1]) + self.size(r.child[2])
        
    def front_recursion(self, roo):
        if roo == None:
            return
        else:
            print(roo.val)
            self.front_recursion(roo.child[0])
            self.front_recursion(roo.child[1])
            self.front_recursion(roo.child[2])
            

        
class Node(object):
    child = [0]*3
    def __init__(self,val,p,c0=None,c1=None,c2=None):
        self.val = val
        self.child[0] = c0
        self.child[1] = c1
        self.child[2] = c2
        self.parent = p
                  
if __name__=="__main__":
    moneytree = Moneytree(5, [3,2,1], None)
    moneytree.grow(moneytree.root)
    print(moneytree.root.child[2].val)
    print(moneytree.size(moneytree.root))
    #moneytree.front_recursion(moneytree.root)
    
    
    
        
        
    