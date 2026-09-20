
def line_number(in_file: str, out_file: str) -> None:
    """
    The line_numer function opens the input file then goes line by line when it then will iterate each line and record 
    it to the output file while also keeping track of the number of the line. 

    in_file represents the input file 
    out_file represents the output file
    the function returns the output file that has the lines from the input file numbered. 
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

def main():
    line_number(__file__, "h2_p1_Lance_Van.txt")

if __name__ == "__main__":
    main()

           


            
        

        
