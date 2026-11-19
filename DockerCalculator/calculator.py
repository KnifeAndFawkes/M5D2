from pathlib import Path

class Calculator: 
    
    def __init__(self,x,y):
        self.x = x
        self.y = y

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

# if __name__ == "__main__":
#     calc = Calculator(247,12)
#     ans = calc.divide(True)
#     print("Calculating 147 divided by 12...}\n")
#     print(f"Answer found! 247 / 12 = {str(round(ans,2))}\n")


out = Path("/data/results.txt")
calc = Calculator(247,12)
ans = calc.divide(True)
with out.open("a") as f:
    f.write("Calculating 147 divided by 12...\n")
    f.write(f"Answer found! 247 / 12 = {str(round(ans,2))}\n")