from parser import ObjAccess, BinOp, UnaryOp

def append_unique_tuple(existing_tuples, new_tuple):
  existing_second_elements = [t[1] for t in existing_tuples]

  if new_tuple[1] not in existing_second_elements:
      existing_tuples.append(new_tuple)
      return existing_tuples
  else:
      index_to_remove = existing_second_elements.index(new_tuple[1])
      existing_tuples.pop(index_to_remove)
      existing_tuples.append(new_tuple)
      return existing_tuples


class Interpreter:
  def __init__(self):
      self.global_scope = {"print":{"type":"function", "builtin":True}}
      self.current_scope = self.global_scope
      self.symbol_table = {}

  def visit(self, node):
      method_name = f'visit_{type(node).__name__}'
      visitor = getattr(self, method_name, self.generic_visit)
      return visitor(node)

  def generic_visit(self, node):
      
      raise Exception(f'No visit_{type(node).__name__} method defined')

  def visit_Program(self, node):
      for statement in node.statements:
          self.visit(statement)

  def visit_VarDeclaration(self, node):
      if node.expression:
          value = self.visit(node.expression)
      else:
          value = None

      self.current_scope[node.identifier] = value

  def visit_FuncDeclaration(self, node):
      self.current_scope[node.name] = {"type":"function","params": node.parameters, "body": node.body, "builtin": False}

  def visit_StructDeclaration(self, node):
    self.current_scope[node.name] = {"type":"struct","fields": node.fields, "builtin": False}
     

  def visit_FuncCall(self, node):
      func_name = node.name
      args = node.arguments
      
      
      if func_name in self.current_scope and self.current_scope[func_name]["type"] == "function":
        if self.current_scope[func_name]["builtin"]:
          if func_name == "print":
            
            for arg in args:
              
              if arg.value != "magic_value_string_depr_do_not":
                print(arg.value)
              elif type(arg) in [BinOp, UnaryOp]:
                print(self.visit(arg))
              elif type(arg.name) == ObjAccess:
                
                
                obj = next((tup for tup in self.current_scope[arg.name.parent]["fields"] if tup[1] == arg.name.child), [None, None])[0]


                print(obj)
              
                

              
              
              else:
                print(self.current_scope[arg.name])
        else:
          argnames = self.current_scope[func_name]["params"]
          orig = self.current_scope
          i = 0
          for arg in args:
            
            self.current_scope[argnames[i]] = arg
            i += 1
            
          for statement in self.current_scope[func_name]["body"]:
            self.visit(statement)
          self.current_scope = orig
          
    
      
      

  
  def visit_ObjInstantiation(self, node):

    obj_type = node.type
    name = node.objname
    if obj_type in self.current_scope and self.current_scope[obj_type]["type"] == "struct":
      self.current_scope[name] = {"type":obj_type, "fields":self.current_scope[obj_type]["fields"]}
     
      
  def visit_Assignment(self, node):
      value = self.visit(node.expression)
      if type(node.identifier) == ObjAccess:
        self.current_scope[node.identifier.parent]["fields"] = append_unique_tuple(self.current_scope[node.identifier.parent]["fields"], (value, node.identifier.child))
        
      else:
        self.current_scope[node.identifier] = value

  def visit_IntLiteral(self, node):
      return node.value

  def visit_StringLiteral(self, node):
      return node.value

  def visit_ListLiteral(self, node):
      return [self.visit(element) for element in node.elements]

  def visit_Identifier(self, node):
      if node.name in self.current_scope:
          return self.current_scope[node.name]
      elif (type(node.name) == ObjAccess) and (node.name.parent in self.current_scope):
          
          return next((tup for tup in self.current_scope[node.name.parent]["fields"] if tup[1] == node.name.child), [None, None])[0]
      else:
          raise NameError(f'Name {node.name} is not defined')

  def visit_BinOp(self, node):
      left = self.visit(node.left)
      right = self.visit(node.right)

      if node.op == 'PLUS':
          return left + right
      elif node.op == 'MINUS':
          return left - right
      elif node.op == 'MULT':
          return left * right
      elif node.op == 'DIV':
          return left / right
      else:
          raise ValueError(f'Unsupported binary operation: {node.op}')

  def visit_UnaryOp(self, node):
      operand = self.visit(node.operand)

      if node.op == 'MINUS':
          return -operand
      else:
          raise ValueError(f'Unsupported unary operation: {node.op}')

  def interpret(self, ast):
      self.visit(ast)
  