import os, datetime
def scan(t): 
    with open(f"./Logs/Gap_Reports/Gap.md",'w') as f: f.write(f"Scanned {t}")
if __name__ == "__main__": scan(".")
