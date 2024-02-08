Author: Matthew Mifsud

How to run program: 1. Make sure you are in the directory containing Makefile and source files
                    2. Enter "make run" in terminal
                    3. Automatically "python3 main.py" will be executed which will run the program
                    4. To change expression, edit input.txt file.

Implementation Details: The core program is made up of 4 files in python code:

                1. Scanner.py - This file contains the code for scanning the file input.txt character
                                by character. The scanner was implemented by using a DFA
                        
                2. Parser.py - This file contains the code for parsing the list of tokens after it 
                                has been obtained. The chosen method was a recursive descent approach.

                3. SemanticCodeGen.py - This file contains the code for Semantic actions which were added
                                        to Parser.py as well as code for converting the read functions into
                                        an expression. The approach taken was one were a stack was simulated
                                        by the semantic actions placed in the parser. By continuously popping
                                        from the stack an expression is built.

                4. main.py - This file is the runner file. It combines the scanner, parser and code generation.

                (Program was implemented using standard python without any libraries)
                
Bugs: Some edge cases for bracketing not fully handled.
