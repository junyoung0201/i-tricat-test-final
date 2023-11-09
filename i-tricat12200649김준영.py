import operator
import uuid
import math

# 스택 클래스 정의
class Stack:
    def __init__(self):
        # 스택을 리스트로 초기화
        self.items = []

    # 스택이 비어있는지 확인하는 메서드
    def is_empty(self):
        return not bool(self.items)

    # 스택에 값을 추가하는 메서드
    def push(self, value):
        self.items.append(value)

    # 스택에서 값을 꺼내는 메서드
    def pop(self):
        # 스택이 비어있지 않은 경우에만 값을 꺼내고 반환
        if not self.is_empty():
            return self.items.pop()
        else:
            print("Stack is empty")  # 스택이 비어있는 경우 예외 처리
            return None

    # 스택의 가장 상단 값을 확인하는 메서드
    def peek(self):
        # 스택이 비어있지 않은 경우에만 가장 상단 값을 반환
        if not self.is_empty():
            return self.items[-1]

    # 스택의 크기를 반환하는 메서드
    def size(self):
        return len(self.items)

# 계산기 클래스 정의
class Calculator:
    def __init__(self):
        # 고유한 ID를 생성하고 스택, 연산자 딕셔너리 초기화
        self.id = uuid.uuid4()
        self.stack = Stack()
        self.operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

    # 주어진 수식을 계산하는 메서드
    def calculate(self, expression):
        operand = ''

        # 수식을 한 글자씩 순회하면서 피연산자와 연산자를 스택에 추가
        for char in expression:
            if char.isdigit():
                operand += char
            elif char in self.operators.keys():
                if operand:
                    self.stack.push(int(operand))
                    operand = ''
                self.stack.push(char)
            else:
                print(f"Unknown token: {char}")

        # 마지막으로 남은 피연산자를 스택에 추가
        if operand:
            self.stack.push(int(operand))

        # 스택에서 연산 수행 및 결과 반환
        while len(self.stack.items) > 1:
            operand2 = self.stack.pop()
            operator = self.stack.pop()

            # 피연산자나 연산자가 부족하거나 유효하지 않은 연산자인 경우 예외 처리
            if operand2 is None or operator not in self.operators:
                print("Insufficient operands or invalid operator")
                return None

            operand1 = self.stack.pop()
            result = self.operators[operator](operand1, operand2)
            self.stack.push(result)

        # 최종 결과 반환
        return self.stack.pop()

    # 객체가 삭제될 때 호출되는 소멸자
    def __del__(self):
        print(f"Calculator {self.id} is being deleted")

# 공학용 계산기 클래스 정의 (Calculator 클래스를 상속)
class EngineerCalculator(Calculator):
    def __init__(self):
        # 부모 클래스의 초기화 메서드 호출 및 상수와 추가 수학 함수 초기화
        super().__init__()
        self.constants = {'pi': math.pi, 'e': math.e}
        self.operators.update({'sin': math.sin, 'cos': math.cos, 'tan': math.tan})

    # 팩토리얼을 계산하는 메서드
    def factorial(self, n):
        if n == 0:
            return 1
        else:
            return n * self.factorial(n-1)

    # 수식을 계산하는 메서드 (오버라이딩)
    def calculate(self, expression):
        # 수식을 공백을 기준으로 토큰으로 나누어 처리
        tokens = expression.split()
        for token in tokens:
            # 상수인 경우 스택에 추가
            if token in self.constants.keys():
                self.stack.push(self.constants[token])
            # 추가된 수학 함수인 경우 스택에서 피연산자를 꺼내 연산 후 결과를 다시 스택에 추가
            elif token in self.operators.keys():
                operand2 = self.stack.pop()

                # 피연산자가 부족한 경우 예외 처리
                if operand2 is None:
                    print("Insufficient operands for operation")
                    return None

                operand1 = self.stack.pop()
                result = self.operators[token](operand1, operand2)
                self.stack.push(result)
            # 숫자인 경우 스택에 추가
            elif token.isdigit():
                self.stack.push(int(token))
            else:
                print(f"Unknown token: {token}")

        # 최종 결과 반환
        return self.stack.pop()

    # 객체가 삭제될 때 호출되는 소멸자 (오버라이딩)
    def __del__(self):
        print(f"EngineerCalculator {self.id} is being deleted")

# 메인 코드
if __name__ == "__main__":
    # 기본 계산기와 공학용 계산기 인스턴스 생성
    calc = Calculator()
    eng_calc = EngineerCalculator()

    while True:
        print("1. 기본 계산기 사용")
        print("2. 공학용 계산기 사용")
        print("3. 종료")
        choice = input("선택: ")

        # 사용자의 선택에 따라 계산기 선택 및 계산 수행
        if choice == "1":
            expression = input("수식 입력: ")
            result = calc.calculate(expression)
            if result is not None:
                print("결과: ", result)
        elif choice == "2":
            expression = input("수식 입력: ")
            result = eng_calc.calculate(expression)
            if result is not None:
                print("결과: ", result)
        elif choice == "3":
            # 객체 삭제 및 프로그램 종료
            del calc
            del eng_calc
            break
        else:
            print("잘못된 선택입니다.")

