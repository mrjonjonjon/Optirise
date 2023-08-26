# Dynamic code generation
variable_name = "x"
variable_value = 42
dynamic_code = f"{variable_name} = {variable_value}\n"

# Add more lines to the dynamic code
dynamic_code += "y = 23\n"
dynamic_code += "result = x + y\n"
dynamic_code += "print('Result:', result)"

# Executing the dynamically generated code
exec(dynamic_code)

print(y)