import sys
from auction import auction

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("cli 입력 에러, 파라미터 확인하세요")
        sys.exit(1)

    # print(sys.argv[0]) //main.py
    commerce_code = sys.argv[1]
    url = sys.argv[2]
    output_dir = sys.argv[3]

    if commerce_code == 'auction':
        auction(url, output_dir)
    else:
        print("없는 커머스 코드")
