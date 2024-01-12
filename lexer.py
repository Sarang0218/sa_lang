class Token:
  def __init__(self, token_type, value=None):
      self.token_type = token_type
      self.value = value

  def __repr__(self):
      return f'Token({self.token_type}, {self.value})'


class Lexer:
  def __init__(self, source_code):
      self.source_code = source_code
      self.position = 0
      self.current_char = self.source_code[self.position] if self.position < len(self.source_code) else None

  def advance(self):
      self.position += 1
      self.current_char = self.source_code[self.position] if self.position < len(self.source_code) else None

  def skip_whitespace(self):
      while self.current_char and self.current_char.isspace():
          self.advance()

  def get_next_token(self):
      while self.current_char:
          if self.current_char.isspace():
              self.skip_whitespace()
              continue

          if self.current_char.isdigit():
              return self.parse_number()

          if self.current_char.isalpha():
              return self.parse_identifier()

          if self.current_char == '"':
              return self.parse_string()

          if self.current_char == '(':
              self.advance()
              return Token('LPAREN')

          if self.current_char == ')':
              self.advance()
              return Token('RPAREN')

          if self.current_char == ':':
              self.advance()
              return Token('COLON')

          if self.current_char == ';':
              self.advance()
              return Token('SEMICOLON')

          if self.current_char == '{':
              self.advance()
              return Token('LBRACE')

          if self.current_char == '}':
              self.advance()
              return Token('RBRACE')

          if self.current_char == '[':
            self.advance()
            return Token('LBRACKET')

          if self.current_char == ']':
            self.advance()
            return Token('RBRACKET')

          if self.current_char == ',':
              self.advance()
              return Token('COMMA')

          if self.current_char == '=':
              self.advance()
              return Token('EQUALS')
          if self.current_char == '+':
            self.advance()
            return Token('PLUS')
          if self.current_char == '-':
            self.advance()
            return Token('MINUS')
          if self.current_char == '*':
            self.advance()
            return Token('MULT')
          if self.current_char == '/':
            self.advance()
            return Token('DIV')
          if self.current_char == '.':
            self.advance()
            return Token('DOT')
          
          self.advance()

      return Token('EOF')

  def parse_number(self):
      num = ''
      while self.current_char and self.current_char.isdigit():
          num += self.current_char
          self.advance()
      return Token('INT', int(num))

  def parse_identifier(self):
      identifier = ''
      while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
          identifier += self.current_char
          self.advance()

      if identifier == 'int':
          return Token('INT_TYPE')
      elif identifier == 'string':
          return Token('STRING_TYPE')
      elif identifier == 'list':
          return Token('LIST_TYPE')
      elif identifier == 'pointer':
          return Token('POINTER_TYPE')
      elif identifier == 'func':
          return Token('FUNC')
      elif identifier == 'struct':
          return Token('STRUCT')
      elif identifier == 'del':
          return Token('DEL')
      elif identifier == 'for':
          return Token('FOR')
      elif identifier == 'while':
          return Token('WHILE')
      else:
          return Token('IDENTIFIER', identifier)

  def parse_string(self):
      self.advance()  # Skip the opening double-quote
      string_value = ''
      while self.current_char and self.current_char != '"':
          string_value += self.current_char
          self.advance()
      self.advance()  # Skip the closing double-quote
      return Token('STRING', string_value)


