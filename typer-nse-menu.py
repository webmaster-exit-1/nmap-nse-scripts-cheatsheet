import subprocess
import re
import typer

app = typer.Typer()

def run_nmap(nse_script: str, target: str, parameters: str):
    command = f"nmap --script={nse_script} {parameters} {target}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")
    else:
        print(output.decode())  # decode bytes to string

def load_nse_scripts(file_path):
    nse_scripts = {}
    with open(file_path, 'r') as f:
        content = f.read()

    # Matches the script name before the code block
    matches = re.findall(r'(.*\.nse)(?=\n\n```bash)', content)

    for match in matches:
        # Strip leading/trailing white spaces and remove .nse extension
        script = match.strip()
        nse_scripts[script] = ""  # As of now, setting parameters as empty string

    return nse_scripts

@app.command()
def main():
    nse_scripts = load_nse_scripts('cheat-sheet.md')

    print("Please choose an NSE script:")
    for i, script in enumerate(nse_scripts.keys(), start=1):
        print(f"{i}. {script}")

    choice = int(typer.prompt("Enter your choice: "))

    chosen_script = list(nse_scripts.keys())[choice-1]
    parameters = nse_scripts[chosen_script]

    # Extract the parameter names
    parameter_names = re.findall(r'<(.*?)>', parameters)

    # Prompt the user for each parameter
    for param_name in parameter_names:
        param_value = typer.prompt(f"Enter the value for {param_name}: ")
        parameters = parameters.replace(f"<{param_name}>", param_value)

    target = typer.prompt("Enter the target: ")

    run_nmap(chosen_script, target, parameters)

if __name__ == "__main__":
    app()