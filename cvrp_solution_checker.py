

def check_file():
    with open('A-n32-k5.vrp', 'r') as f:
        data = f.read()
        l = data.split("\n")
        print(l)

if __name__ == "__main__":
    check_file()