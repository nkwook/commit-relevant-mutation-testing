import ast
import os

# fix: 전체 같이 쓰는 뮤테이트 함수 있으면 그거 사용하도록 수정하기
def mutate(node):
    return node

# commit relevant하다고 밝혀진 노드가 활용하는
# 다른 모듈의 함수에 대해 mutation을 진행해준다. 
# ex) import_mutate("test.py", ["func1", "func2"])
def import_mutate(file_name, function_names):
    with open(file_name, 'r') as file:
        source = ''.join(file.readlines())
        root = ast.parse(source)

        for node in ast.walk(root):
            if(isinstance(node, ast.FunctionDef) and node.name in function_names):
                mutate(node)

# 경욱님이 mark해준 ast tree의 root node를 넘겨준다
def find_relevant_import(root: ast.Module):    
    direct_calls = []
    from_imports = []
    path_map = {}

    for node in ast.walk(root):
        # from @@@ import ###
        if(isinstance(node, ast.ImportFrom)):
            for iter in node.names:
                from_imports.append({'path': '/'.join(node.module.split('.')), 'name': iter.name})

        # function call 
        # todo: class method call
        if(isinstance(node, ast.Call)):
            if(isinstance(node.func, ast.Attribute)):
                function_name = node.func.attr
                path = node.func.value.id + '.py'
                if(os.path.exists(path)):
                    if(path not in path_map):
                        path_map[path] = []
                    path_map[path].append(function_name)

            if(isinstance(node.func, ast.Name)):
                direct_calls.append(node.func.id)

    for node in from_imports:
        # 호출된 경우만 살펴보기
        if(node['name'] not in direct_calls): continue

        # path.py를 찾을 수 있으면, name은 import한 함수나 클래스 이름이 됨.
        # 찾을 수 없다면, name까지 붙여서 전체를 찾아야 함.
        # ex1) from lib.lib2 import d
        # ex2) from lib.lib2.d import hello()
        path = node['path'] + '.py'
        if(not os.path.exists(path)):
            path = node['path'] + '/' + node['name'] + '.py'
        if(os.path.exists(path)):
            if(path not in path_map):
                path_map[path] = []
            path_map[path].append(node['name'])
        
    for file in path_map:
        import_mutate.import_mutate(file, path_map[file])