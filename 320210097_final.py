import re
#creating variavle dictionary
def define_propositional_variables(sentence):
  var_map = {}
  props = re.split(r'\s*(and|\bor\b|then|,|but|\.|therefore|^if|if)\s*',sentence.lower())
  print(props)
  for prop in props:
    if prop not in {'and', 'or', 'then', 'if', ',', 'but', '.', '', 'therefore', ' '}:
      if "not" in prop:
        ind=prop.index("not")
        temp=prop[:ind] + prop[ind+4:]
        prop=temp
      if prop not in var_map:
        var_map[prop] = f'P{len(var_map)+1}'
  return var_map

#replace sentence with propositional variable
def replacement( s ,variables):
  s=s.lower()
  for j in variables.keys():
    s=s.replace( j , variables[j])
  s=s.split(".")
  for i in range(len(s)):
    for j in variables.keys():
        s[i]=s[i].replace(" not "," ")
        s[i]=s[i].replace( j , f"~{variables[j]}")
    if ("if" in s[i]):
      s[i]=s[i].replace("," , "->")
      s[i]=s[i].replace("then" , "->")
    s[i]=s[i].replace("therefore " , "")        
    s[i]=s[i].replace("or" , "∨")
    s[i]=s[i].replace("and" , "∧")
    s[i]=s[i].replace("if " , "")
  conclusion=s[-1]
  s=s[:-1]
  return (s , conclusion)
#rules of inference 
def modus_ponens(a, b):
    if len(a)>=2 and a[1] == "->" and len(b)==1 and a[0] == b[0]:
        return [a[2]]
    return None

def modus_tollens(a, b):
    if len(a) >=2 and a[1] == "->" and len(b) ==1 and (b[0] == "~" + a[2] or  "~" + b[0] == a[2] ):
        return ["~" + a[0]]
    return None

def simplification(a):
    if len(a)>=2 and a[1] == "∧":
        return [a[0], a[2]]
    return None

def conjunction(a , b):
    if len(a)==1 and len(b)==1 and b!=0 and a!=0:
        return [a , "∧" , b]

def hypothetical_syllogism(a, b):
    if len(a)==2 and len(b)==2 and a[1] == "->" and b[1] == "->" and a[2] == b[0]:
        return [ a[0] , "->" ,  b[2]]
    return None

def disjunctive_syllogism(a, b):
  if len(a) >= 2 and a[1] == "∨" and len(b) == 1 and (b[0] == "~" + a[0]
                                                      or "~" + b[0] == a[0]):
    return [a[2]]
  elif len(a[0]) >= 3:
    a = a[0]
    if a[2] == "∨" and len(b) == 1 and (b[0] == "~" + a[0:2] or "~" + b[0] == a[0:2]):
      return [a[3:]]
  return None

def resolution(a , b):
    if len(a)>=2 and a[1]=="∨"  and b[1] =="∨"  and ( b[0] == "~" + a[0] or "~" + b[0] == a[0]):
        return [ a[2] , "∨" , b[2] ]
    
#applying the rules 
def apply_rules(premises, conclusion, inferred):
    for p in premises:
        for q in inferred:
          if p!=q:
            result = modus_ponens(p, q)
            if result is not None and result not in inferred:
                print(f"modes ponens used with {p} and {q} , the result is {result}")
                inferred.append(result)
                inferred.remove(q)
                inferred.remove(p) if p in inferred else None
                apply_rules(premises, conclusion, inferred)
            result = modus_tollens(p, q)
            if result is not None and result not in inferred:
                print(f"modes tollens used with {p} and {q} , the result is {result}")
                inferred.append(result)
                inferred.remove(q)
                inferred.remove(p) if p in inferred else None
                apply_rules(premises, conclusion, inferred)
            result = simplification(p)
            if result is not None and [result[0]] not in inferred and [result[1]] not in inferred:
                print(f"simplification used with {p} and {q} , the result is {result}")
                inferred.append([result[0]])
                inferred.append([result[1]])
                inferred.remove(p)
                apply_rules(premises, conclusion, inferred)
            result = hypothetical_syllogism(p, q)
            if result is not None and result not in inferred:
                print(f"hypothetical_syllogism used with {p} and {q} , the result is {result}")
                inferred.append(result)
                inferred.remove(q)
                inferred.remove(p) if p in inferred else None
                apply_rules(premises, conclusion, inferred)
            result = disjunctive_syllogism(p, q)
            if result is not None and result not in inferred:
                print(f"disjunctive_syllogism used with {p} and {q} , the result is {result}")
                inferred.append(result)
                inferred.remove(q)
                inferred.remove(p) if p in inferred else None
                apply_rules(premises, conclusion, inferred)
            result = resolution(p, q)
            if result is not None and result not in inferred:
                print(f"resolution used with {p} and {q} , the result is {result}")
                inferred.append(result)
                inferred.remove(q)
                inferred.remove(p) if p in inferred else None
                apply_rules(premises, conclusion, inferred)
    if len(inferred) != 1:
        apply_rules(inferred, conclusion, inferred)
    return f" the argument is valid and the conclusion is {inferred}"


sentence="If today is Tuesday, I have a test in English or I have a test in Science.If my English Professor is absent then I have not a test in English.Today is Tuesday and my English Professor is absent.Therefore I have a test in Science"
#sentence="if he love pizza then he love orange.he love pizza.therefore he love orange"
variable=define_propositional_variables(sentence)
print(variable)
premises=replacement(sentence, variable)[0]
conclusion=replacement(sentence, variable)[1]
print(premises)
premises=list(map(lambda x : x.replace(" " , ""), premises ))
premises=list(map(lambda x :re.split(r'\s*(∧| ∨|->)\s*',x), premises ))
print(apply_rules(premises, conclusion, premises))

