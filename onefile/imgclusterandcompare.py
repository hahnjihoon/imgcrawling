import sys
import os

def auction(url, output_dir):
    # auction 크롤링 로직 구현
    print(f"auction: {url}, {output_dir}")

def elevenst(url, output_dir):
    # elevenst 크롤링 로직 구현
    print(f"elevenst: {url}, {output_dir}")

def gmarket(url, output_dir):
    # gmarket 크롤링 로직 구현
    print(f"gmarket: {url}, {output_dir}")

def main():
    if len(sys.argv) != 4:
        print("cli 입력 에러, 파라미터 확인하세요")
        sys.exit(1)

    commerce_code = sys.argv[1]
    url = sys.argv[2]
    output_dir = sys.argv[3]

    commerce_code = commerce_code.lower()
    if commerce_code == 'auction':
        auction(url, output_dir)
    elif commerce_code == 'elevenst':
        elevenst(url, output_dir)
    elif commerce_code == 'gmarket':
        gmarket(url, output_dir)
    else:
        print("없는 커머스 코드")
        sys.exit(1)

if __name__ == '__main__':
    main()
