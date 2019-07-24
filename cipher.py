class Cipher:



    """
        Author's info: 
            Name:       Aderinlokun Oluwaseun
            Email:      aderinlokunoluwaseun@gmail.com
            Twitter:    
            Date:       24-07-2019

            THANK YOU IN ANTICIPATION!!!

            Copyright © 2019
    """




    """
    Instructions on how to use this cipher program are listed below:
    1.  create an object - instance of the Cipher class
    2.  To encrypt, call the object function .encrypt() and pass two arguments: text to be encrypted, and the key
    3.  To decrypt, call the object function .decrypt() and pass two arguments: text to be encrypted, and the key

    """

    """
    To run this, do one of the two below:

        1.  Copy and run the below 4 lines of code

            from cipher import Cipher

            cipher = Cipher()
            cipher.encrypt()
            cipher.decrypt()

        2.  Run the sample.py

    """




    #   The initial properties of the cipher object are initialized here...
    def __init__(self):
        self.random_key = 0
        self.transform_key = []
        self.map = {}
        self.inverse_map = {}
        self.visit = []
        self.cipher = ''
        self.random = 0
        self.q = 0

        #   This loop will be be used during the initialization of map and inverse map
        for i in range (0,127):
            if i in range(0,32):
                self.visit.append('unvisited')
            elif i in range(32,127):
                self.visit.append('visited')

        return


    #   This function will turn texts into a matrix m x n
    def Columnize(self,text,row,col,option):
        matrix = []

        #   Matrix for Encryption
        j = 0
        if(option == 'encrypt'):
            for i in range(0,col):
                j = i
                temp = []

                while j < len(text):
                    temp.append(text[j])
                    j += col

                matrix.append(temp)

        #   Matrix for Decryption
        elif(option == 'decrypt'):
            i = 0
            while i < len(text):
                j = i
                temp = []

                for k in range(0,row):
                    temp.append(text[j])
                    j += 1
                
                matrix.append(temp)
                i += row

        return matrix


    #   The columnal trans formation will take place here for encryption
    def columnTransform(self,cipher_list):

        #   The below block ensures that the element in the cipher_list is m x n
        col = len(self.transform_key)
        if ((len(cipher_list)%col) != 0):
            row = (len(cipher_list)//col) + 1
        else:
            row = len(cipher_list)//col
        
        while (len(cipher_list)%col != 0):
            cipher_list += ' '
        
        #   The cipher_list is transformed to a matix
        matrix = self.Columnize(cipher_list,row,col,'encrypt')

        #   process of switching indexes starts here
        transformed_matrix = []
        for i in range(0,len(matrix)):
            transformed_matrix.append(' ')

        #   getting the index of the matrix according to the transform_key digit
        index = []
        for i in range(0,len(self.transform_key)):
            index.append(self.transform_key[i] - 1)

        #   Indexes are switched
        for i in range (0,col):
            transformed_matrix[i] = matrix[index[i]]

        #   Turning the matrix to a linear list
        cipher_text_transform_list = []
        for i in range(0,col):
            for j in range(0,len(transformed_matrix[i])):
                cipher_text_transform_list.append(transformed_matrix[i][j])
        
        return cipher_text_transform_list


    #   The columnal transformation will take place here for decryption
    def reverseColumnTransform(self,cipher_list):

        #   The below block ensures that the element in the cipher_list is m x n
        col = len(self.transform_key)
        if ((len(cipher_list)%col) != 0):
            row = (len(cipher_list)//col) + 1
        else:
            row = len(cipher_list)//col
        
        while (len(cipher_list)%col != 0):
            cipher_list += ' '

        #   The cipher_list is transformed to a matix
        matrix = self.Columnize(cipher_list,row,col,'decrypt')

        #   process of switching indexes starts here
        reverse_transformed_matrix = []
        for i in range(0,len(matrix)):
            reverse_transformed_matrix.append(' ')

        #   getting the index of the matrix according to the transform_key digit
        index = []
        for i in range(0,len(self.transform_key)):
            index.append(self.transform_key[i] - 1)

        #   Indexes are switched
        for i in range (0,col):
            reverse_transformed_matrix[index[i]] = matrix[i]

        cipher_text_reverse_transform_list = []

        #   Turning the matrix to a linear list
        for i in range(0,row):
            for j in range(0,col):
                cipher_text_reverse_transform_list.append(reverse_transformed_matrix[j][i])

        return cipher_text_reverse_transform_list


    #   This function generates plain_text for the decrytion
    def generatePlainText(self,cipher_list,cipher):
        plain_text = ''

        for i in range(0,len(cipher)):
            if (cipher_list[i] != ' '):
                plain_text += chr(self.inverse_map[cipher_list[i]])
        return plain_text
        

    #   This function decrypts encrypted text
    def decrypt(self):
        cipher_texts = str(input("Enter the text to be decrypted: "))
        enc_key = str(input("Enter the Encrypttion key: "))

        enc_key = str(enc_key)
        self.generateKey(enc_key)
        self.initializeMap()
        cipher_list = []

        cipher_list = self.reverseColumnTransform(cipher_texts)
        plain_text_list = self.generatePlainText(cipher_list,cipher_texts)

        #   Sets the object attributes to the intial values
        self.random_key = 0
        self.transform_key = []
        self.map = {}
        self.inverse_map = {}
        self.cipher = ''
        self.random = 0
        self.q = 0
        
        print(plain_text_list)
        return plain_text_list


    #   This function encrypts plain text
    def encrypt(self):
        plain_text = str(input("Enter the text to be encrypted: "))
        enc_key = str(input("Enter the Encrypttion key: "))

        self.generateKey(enc_key)
        self.initializeMap()
        cipher = self.generateCipher(plain_text)
        cipher_text = ""

        for i in range(0,len(cipher)):
            cipher_text += str(cipher[i])

        #   Sets the object attributes to the intial values
        self.random_key = 0
        self.transform_key = []
        self.map = {}
        self.inverse_map = {}
        self.cipher = ''
        self.random = 0
        self.q = 0

        print(cipher_text)
        return cipher_text
        

    #   This function generates cipher texts for plain texts
    def generateCipher(self,plain_text):
        cipher_list = []
        plain_text_ascii = []
        
        
        for i in range(0,len(plain_text)):
            plain_text_ascii.append(ord(plain_text[i]))
            cipher_list.append(self.map[plain_text_ascii[i]])
        
        self.cipher = self.columnTransform(cipher_list)

        return self.cipher


    #   This function generates the random key and transform key from the inputed key
    def generateKey(self,enc_key):
            key_ascii = []
            seen = []

            for i in range (0,len(enc_key)):
                key_ascii.append(ord(enc_key[i]))
                
            temp_transform_key = []

            for i in range(0,len(key_ascii)):
                self.random_key = self.random_key*10 + key_ascii[i]
                temp_transform_key.append((key_ascii[i] % len(enc_key)) + 1)
        
            replacer = 1         
            for i in range(0,len(temp_transform_key)):
                if temp_transform_key[i] not in seen:
                    seen.append(temp_transform_key[i])
                else:
                    while replacer in seen:
                        replacer += 1

                    temp_transform_key[i] = replacer
                    seen.append(replacer)
                    replacer += 1
            
            self.transform_key = temp_transform_key
            return [self.random_key,self.transform_key]


    #   This function gets random ascii digits
    def getNextRandom(self):

        while (True):
            self.random = self.q % 127
            self.q = self.random + 3*self.random_key
            if(self.visit[self.random] is 'unvisited'):
                if ((self.random in range(0,32)) or (self.random in range(127,256))):
                    continue
                elif (self.random in range(32,127)):
                    self.visit[self.random] = 'visited'
                    break
            else:
                self.random = (self.random + 1) % 127
                break
        return self.random
    

    #   This function populates the map and inverse map
    def initializeMap(self):
        for i in range (0,256):
            if (i in range(0,32)) or (i in range(127,256)):
                self.map[i] = i
            else:
                self.map[i] = chr(self.getNextRandom())

        map = self.map
        
        for key, value in map.items():
            self.inverse_map[value] = key
        
        return [self.map,self.inverse_map]





"""
Author's info: 
    Name:       Aderinlokun Oluwaseun
    Email:      aderinlokunoluwaseun@gmail.com
    Twitter:    
    Date:       24-07-2019


    THANK YOU IN ANTICIPATION!!!

    Copyright © 2019
"""
