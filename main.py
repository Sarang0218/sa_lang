import lexer
import parser
import interpreter

source_code = """
print(1);
int j = 90;

string greeting = "Hello, World!";
list numbers = [[1], 2, 3];
pointer ptr;
func my_function(j) {
   int i = 9;
   print(j+i);
   print(greeting);
}
struct Person {
    string name;
    int age;
}
int x = 10;
x = x + 10;
print();
my_function(10);
Person person;
person.age = 1;
print(numbers);
person.age = person.age + 1;
print(person.age);
"""

# 구현된 기능:
# 자료형: int, string, list
# 함수, 빌트인 함수 (프린트)
# 스코프
# 구조체 (Struct)

# 구현 X:
# 기능: 포인터, 딕셔너리, 클래스, 상속, for문, while문, return, continue, break
# 빌트인: 입력 함수



lex = lexer.Lexer(source_code)

parse = parser.Parser(lex)
ast = parse.parse()


ip = interpreter.Interpreter()
ip.interpret(ast)


