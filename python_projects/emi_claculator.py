
i = 0
print("\n_________ enter e to exit _________\n")
data = []
def process_final(data,GST:float):
    total:float = 0.0
    tax:float = 0.0
    process_fee:float =300.0 #you can take processing fee also as a input, here i've hard coded it...
    for ins in data:
        print(f"{ins[0]} | {ins[1]} | {ins[2]}")
        tax += ins[1]*(GST/100)
        total += ins[0]
    total += tax+process_fee+(process_fee*(GST/100))
    print(total) #print final amount you need to pay for EMI...

#take all installment emi and interest
while 1:
    i+= 1
    installment = input(f"enter installment {i} : ")
    if installment == "e":
        tax = float(input(f"enter GST in % : "))
        process_final(data,tax)
    else:
        installment = float(installment)
        interest = float(input(f"enter interest : "))
        data.append([installment, interest,interest+installment])
