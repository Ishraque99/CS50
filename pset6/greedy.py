print("O hai! ", end="")
while True:
    x = float(input("How much change is owed?"))
    if x > 0.0:
        break

monies = round(x*100)
count = 0

while(monies >= 25):
    monies = monies - 25
    count += 1
        
while(monies >= 10):
    monies = monies - 10
    count += 1

while(monies >= 5):
    monies = monies - 5
    count += 1
        
while(monies >= 1):
    monies = monies - 1
    count += 1
    
print(count)