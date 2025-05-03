with open("sample_text.txt", "r") as file:
    lines = file.readlines()


if lines: 
    print("First line:", lines[0].strip())  
    print("Last line:", lines[-1].strip())