class ASTNode:
  pass


class Program(ASTNode):
  def __init__(self, statements):
      self.statements = statements

  def __repr__(self):
      statements_repr = ', '.join(map(repr, self.statements))
      return f'Program([ {statements_repr} ])'


class VarDeclaration(ASTNode):
  def __init__(self, identifier, datatype, expression):
      self.identifier = identifier
      self.datatype = datatype
      self.expression = expression

  def __repr__(self):
      return f'VarDeclaration({self.identifier}, {self.datatype}, {self.expression})'


class FuncDeclaration(ASTNode):
  def __init__(self, name, parameters, body):
      self.name = name
      self.parameters = parameters
      self.body = body

  def __repr__(self):
      parameters_repr = ', '.join(map(repr, self.parameters))
      body_repr = ', '.join(map(repr, self.body))
      return f'FuncDeclaration({self.name}, [ {parameters_repr} ], [ {body_repr} ])'

class ObjInstantiation(ASTNode):
  def __init__(self, class_name, objname):
    self.type = class_name
    self.objname = objname

  def __repr__(self):
    return f'ObjInstantiation({self.type}, {self.objname})'

class ObjAccess(ASTNode):
  def __init__(self, parent,child):
    self.parent = parent
    self.child = child

  def  __repr__(self):
   return f"ObjAccess({self.parent}'s property: {self.child})"
class FuncCall(ASTNode):
  def __init__(self, name, arguments):
    self.name = name
    self.arguments = arguments
  def __repr__(self):
    return f"FunctionCall({self.name}, {self.arguments})"
    
class StructDeclaration(ASTNode):
  def __init__(self, name, fields):
      self.name = name
      self.fields = fields

  def __repr__(self):
      fields_repr = ', '.join([f'({datatype}, {identifier})' for datatype, identifier in self.fields])
      return f'StructDeclaration({self.name}, [ {fields_repr} ])'


class Assignment(ASTNode):
  def __init__(self, identifier, expression):
      self.identifier = identifier
      self.expression = expression

  def __repr__(self):
      return f'Assignment({self.identifier}, {self.expression})'


class IntLiteral(ASTNode):
  def __init__(self, value):
      self.value = value

  def __repr__(self):
      return f'IntLiteral({self.value})'


class StringLiteral(ASTNode):
  def __init__(self, value):
      self.value = value

  def __repr__(self):
      return f'StringLiteral({self.value})'


class ListLiteral(ASTNode):
  def __init__(self, elements):
      self.elements = elements
      self.value = elements

  def __repr__(self):
      elements_repr = ', '.join(map(repr, self.elements))
      return f'ListLiteral([ {elements_repr} ])'


class Identifier(ASTNode):
  def __init__(self, name):
      self.name = name
      self.value = "magic_value_string_depr_do_not"

  def __repr__(self):
      return f'Identifier({self.name})'


class BinOp(ASTNode):
  def __init__(self, left, op, right):
      self.left = left
      self.op = op
      self.right = right
      self.value = "magic_value_string_depr_do_not"

  def __repr__(self):
      return f'BinOp({self.left}, {self.op}, {self.right})'


class UnaryOp(ASTNode):
  def __init__(self, op, operand):
      self.op = op
      self.operand = operand
      self.value = "magic_value_string_depr_do_not"

  def __repr__(self):
      return f'UnaryOp({self.op}, {self.operand})'


class Parser:
  def __init__(self, lexer):
      self.lexer = lexer
      self.current_token = self.lexer.get_next_token()

  def error(self, message):
      raise Exception(f'Parser Error: {message}')

  def eat(self, token_type):
      if token_type == "ANYTYPE":
        if self.current_token.token_type in ["STRING_TYPE", "INT_TYPE", "LIST_TYPE"]:
          self.current_token = self.lexer.get_next_token()
        else:
          self.error(f'Expected any type, got {self.current_token.token_type}')
      else:
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected {token_type}, got {self.current_token.token_type}')

  def factor(self):
      token = self.current_token

      if token.token_type == 'INT':
          self.eat('INT')
          return IntLiteral(token.value)
      elif token.token_type == 'STRING':
          self.eat('STRING')
          return StringLiteral(token.value)
      elif token.token_type == 'LBRACKET':
        elements = []
        self.eat('LBRACKET')
  
        while self.current_token.token_type != 'RBRACKET':
            elements.append(self.expr())
            if self.current_token.token_type == 'COMMA':
                self.eat('COMMA')
  
        self.eat('RBRACKET')
        return ListLiteral(elements)
      elif token.token_type == 'IDENTIFIER':
          return self.handle_ident()
      elif token.token_type == 'LPAREN':
          self.eat('LPAREN')
          node = self.expr()
          self.eat('RPAREN')
          return node
      else:
          self.error(f'Unexpected token: {token.token_type}')

  def term(self):
      node = self.factor()

      while self.current_token.token_type in ('MULT', 'DIV'):
          token = self.current_token
          if token.token_type == 'MULT':
              self.eat('MULT')
          elif token.token_type == 'DIV':
              self.eat('DIV')

          node = BinOp(left=node, op=token.token_type, right=self.factor())

      return node

  def expr(self):
      node = self.term()

      while self.current_token.token_type in ('PLUS', 'MINUS'):
          token = self.current_token
          if token.token_type == 'PLUS':
              self.eat('PLUS')
          elif token.token_type == 'MINUS':
              self.eat('MINUS')

          node = BinOp(left=node, op=token.token_type, right=self.term())

      return node





  def parse_statement(self):
      token = self.current_token

      if token.token_type == 'INT_TYPE':
          self.eat('INT_TYPE')
          identifier = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('EQUALS')
          expression = self.expr()
          self.eat('SEMICOLON')
          return VarDeclaration(identifier, 'int', expression)
      elif token.token_type == 'STRING_TYPE':
          self.eat('STRING_TYPE')
          identifier = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('EQUALS')
          expression = self.expr()
          self.eat('SEMICOLON')
          return VarDeclaration(identifier, 'string', expression)
      elif token.token_type == 'LIST_TYPE':
          self.eat('LIST_TYPE')
          identifier = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('EQUALS')
          expression = self.expr()
          self.eat('SEMICOLON')
  
          return VarDeclaration(identifier, 'list', expression)

      elif token.token_type == 'POINTER_TYPE':
          self.eat('POINTER_TYPE')
          identifier = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('SEMICOLON')
          return VarDeclaration(identifier, 'pointer', None)
      elif token.token_type == 'FUNC':
          self.eat('FUNC')
          name = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('LPAREN')
          args = []
          while self.current_token.token_type != 'RPAREN':
            args.append(self.expr())
            if self.current_token.token_type == 'COMMA':
                self.eat('COMMA')
            
          self.eat('RPAREN')
          self.eat('LBRACE')
          body = self.parse_statements()
          self.eat('RBRACE')
          return FuncDeclaration(name, args, body)
      elif token.token_type == 'STRUCT':
          self.eat('STRUCT')
          name = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('LBRACE')
          fields = self.parse_struct_fields()
          self.eat('RBRACE')
          return StructDeclaration(name, fields)
      elif token.token_type == 'IDENTIFIER':
          return self.handle_ident()
      else:
          self.error(f'Unexpected token: {token.token_type}')
  def handle_ident(self, customs=None):
    
    if customs == None:
      identifier = self.current_token.value
      self.eat('IDENTIFIER')
    else: 
      
      identifier = ObjAccess(customs, self.current_token.value)
      self.eat('IDENTIFIER')
      
    if self.current_token.token_type == 'IDENTIFIER':
        name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('SEMICOLON')
        return ObjInstantiation(identifier,name)
    elif self.current_token.token_type == 'LPAREN':

        self.eat('LPAREN')
        args = []
        while self.current_token.token_type != 'RPAREN':
            args.append(self.expr())
            if self.current_token.token_type == 'COMMA':
                self.eat('COMMA')
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return FuncCall(identifier, args)
    elif self.current_token.token_type == "DOT":
      
        self.eat("DOT")
        return self.handle_ident(identifier)
        
        


    elif self.current_token.token_type == "EQUALS":
      
      
      self.eat('EQUALS')
      expression = self.expr()
      self.eat('SEMICOLON')
      return Assignment(identifier, expression)
    else:
      return Identifier(identifier)
  def parse_struct_fields(self):
      fields = []
      while self.current_token.token_type != 'RBRACE':
          datatype = self.current_token.value
          self.eat("ANYTYPE")
          identifier = self.current_token.value
          self.eat('IDENTIFIER')
          self.eat('SEMICOLON')
          fields.append((datatype, identifier))
      return fields

  def parse_statements(self):
      statements = []
      while self.current_token.token_type != 'RBRACE':
          statements.append(self.parse_statement())
      return statements

  def parse_program(self):
    statements = []
    while self.current_token.token_type != 'EOF':
        statements.append(self.parse_statement())
    return statements
    

  def parse(self):
      statements = self.parse_program()
      return Program(statements)



