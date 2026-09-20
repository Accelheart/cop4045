import ast

def line_number(in_file: str, out_file: str) -> None:
    """
    The line_numer function opens the input file then goes line by line when it then will iterate each line and record 
    it to the output file while also keeping track of the number of the line. 
    """
    try:
        with open(in_file, "r") as file_in:
            in_collection = file_in.readlines()
            with open(out_file, "w") as file_out:
                for line_num, text_line in enumerate(in_collection, start=1):
                    file_out.write(str(line_num) + ". " + text_line)
    except:
        print("No file was found")
        raise

def parse_functions(file_parse: str) -> tuple:
    """
    the parse_functions function opens the python file then reads its contents then find every function definition using the in built python
    module ast which is used to turn all the code into one line in which I read the line and extract information about each function
    using ast.FunctionDef. The function also includes line number, the function name, and the arguments. It will then remove comments and empty lines and 
    then sort the functions which will return the tuple at the end.

    """
    try:
        with open(file_parse, "r") as file:
            parse_collection = file.read()
            parse_tree = ast.parse(parse_collection)
            functions = []
            for node in ast.walk(parse_tree):
                if isinstance(node, ast.FunctionDef):
                    line_num = node.lineno
                    function_name = node.name
                    arguments = ", ".join(arg.arg for arg in node.args.args)
                    function_code = ast.get_source_segment(parse_collection, node)
                    code_lines = function_code.splitlines()
                    clean_lines = []
                    for line in code_lines:
                        if "#" in line:
                            line = line.split("#")[0]
                        stripped = line.strip()
                        if stripped and not stripped.startswith("#"):
                            clean_lines.append(line)
                    function_code = "\n".join(clean_lines) + "\n"
                    functions.append((line_num, function_name, arguments, function_code))
            functions.sort(key=lambda x: x[1])
            return tuple(functions)
    except:
        print("No file was found")
        raise



def main():
    line_number(__file__, __file__.replace(".py", ".txt"))
    result = parse_functions(__file__)
    print(result)
    # with open(__file__.replace(".py", ".txt"), "r") as file:
      #  print(file.read())


if __name__ == "__main__":
    main()

           


            
        

        
