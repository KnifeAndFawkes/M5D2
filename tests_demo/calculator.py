class Calculator: 
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.nirosh = 3.4

    def Multiply(self):
        return self.x * self.y
    
    def Add(self):
        return self.x + self.y
    
    def subtract(self):
        return self.x - self.y
    
    def divide(self, xFirst):
        if (xFirst):
            return self.x / self.y
        else:
            return self.y / self.x
    
    def Multiply_Nirosh(self):
        return (self.x * self.y) * self.nirosh
    
    def Add_Nirosh(self):
        ans = (self.x + self.y) * self.nirosh
        return ans
    
if __name__ == "__main__":
    calc = Calculator(10,5)
    print("X:",calc.x,"Y:",calc.y)
    print("Multiply:",calc.Multiply())
    print("Add:",calc.Add())
    print("subtract:",calc.subtract())
    print("divide X:",calc.divide(True))
    print("divide Y:",calc.divide(False))
    print("Nirosh")
    print("Multiply:",calc.Multiply_Nirosh())
    print("Add:",calc.Add_Nirosh())