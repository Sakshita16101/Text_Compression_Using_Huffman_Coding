#!/usr/bin/env python
# coding: utf-8

# In[24]:


import os
import heapq
class BinaryTreeNode:
    def __init__(self,key,frequency):
        self.left=None
        self.right=None
        self.key=key
        self.frequency=frequency
    def __lt__(self,other):
        return self.frequency<other.frequency
    def __eq__(self,other):
        return self.frequency==other.frequency
        
class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reverseCodes={}
        
    def __make_frequency_dict(self,text):
        freq_dict={}
        for char in text:
            freq_dict[char]=freq_dict.get(char,0)+1
        return freq_dict
    
    def __buildHeap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binary_tree_node=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binary_tree_node)
    def __buildTree(self):
        while(len(self.__heap)>1):
            binary_tree_node_1=heapq.heappop(self.__heap)
            binary_tree_node_2=heapq.heappop(self.__heap)
            freq_sum=binary_tree_node_1.frequency+binary_tree_node_2.frequency
            newNode=BinaryTreeNode(None,freq_sum)
            newNode.left=binary_tree_node_1
            newNode.right=binary_tree_node_2
            heapq.heappush(self.__heap,newNode)
        return
            
    

    def __buildCodesHelper(self,root,curr_bits):
        if root is None:
            return
        if root.key is not None:
            self.__codes[root.key]=curr_bits
            self.__reverseCodes[curr_bits]=root.key
            return
        self.__buildCodesHelper(root.left,curr_bits+"0")
        self.__buildCodesHelper(root.right,curr_bits+"1")
        
    def __buildCodes(self):
        root=heapq.heappop(self.__heap)
        self.__buildCodesHelper(root,"")
        
    def __getEncodedText(self,text):
        encoded_text=""
        for char in text:
            encoded_text +=self.__codes[char]
        return encoded_text
    def __getPaddedText(self,encoded_text):
        padded_amount=8-(len(encoded_text)%8)
        
        for i in range(padded_amount):
            encoded_text +="0"
        padded_info="{0:08b}".format(padded_amount)
        padded_encoded_text=padded_info+encoded_text
        return padded_encoded_text
    def __getBytesArray(self,padded_encoded_text):
        array=[]
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            array.append(int(byte,2))
        return array
            
        
            
        
    
            
        
        
    
    def compress(self):
        file_name,file_extention=os.path.splitext(self.path)
        output_path=file_name+".bin"
        with open(self.path,'r+') as file ,open(output_path,'wb') as output:
            #make frequency dictionary using the text
            text=file.read()
            text=text.rstrip()
            
            freq_dict=self.__make_frequency_dict(text)
            #construct the heap from the frequency_dict
            self.__buildHeap(freq_dict)
            #construct the binary tree from the heap
            self.__buildTree()
            self.__buildCodes()
            #creating the encoded text using the codes
            encoded_text=self.__getEncodedText(text)
            #put this encoded text into the binary file
            padded_encoded_text=self.__getPaddedText(encoded_text)
            bytes_array=self. __getBytesArray(padded_encoded_text)
            #return the binary file as output
            final_bytes=bytes(bytes_array)
            output.write(final_bytes)
        print("Compressed")
        return output_path
    def __removePadding(self,text):
        padded_info=text[:8]
        extra_padding=int(padded_info,2)
        text=text[8:]
        text_after_padding_removed=text[:-1*extra_padding]
        return text_after_padding_removed
    def __decodedText(self,text):
        decoded_text=""
        curr_bits=""
        for bit in text:
            curr_bits +=bit
            if curr_bits in self.__reverseCodes:
                character=self.__reverseCodes[curr_bits]
                decoded_text +=character
                curr_bits=""
        return decoded_text
    def decompress(self,input_path):
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename+"_decompressed"+".txt"
        with open(input_path,'rb') as file, open(output_path,'w')as output:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string +=bits
                byte=file.read(1)
            actual_text=self.__removePadding(bit_string)
            decompressed_text=self.__decodedText(actual_text)
            output.write(decompressed_text)
        print("Decompressed")
        return output_path
def printTextInFile(path):
    if path[-3:]=="bin":
        with open(path,'rb+') as file:
            text=file.read()
            print(path," : " ,text)
            return
    with open(path,'r+') as file:
        text=file.read()
        print(path," : " ,text)
        return

path='C:/Users/sjayaswa/OneDrive - American Express/Desktop/Coding Ninjas Notes/test1.txt'
printTextInFile(path)
h=HuffmanCoding(path)
output_path=h.compress()
printTextInFile(output_path)
output_path= h.decompress(output_path)      
printTextInFile(output_path)


        
        


# In[ ]:




