from clueMatrix import generate

def main(**kwargs):
    renderer,extraParts = generate(**kwargs)
    with open("matrix.in","w") as file:
        file.write(renderer.export())

if __name__ == "__main__":
    import sys
    puzzleFile = "PCgbWI.txt"
    if len(sys.argv)>1:
        puzzleFile = sys.argv[1]
    main( puzzleFile = puzzleFile )