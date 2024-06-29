import os
import logging
from dotenv import load_dotenv
import anthropic
from crewai import Agent, Task, Crew
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
import subprocess
import tempfile

# Set up logging
logging.basicConfig(filename='main.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Set up Anthropic client
try:
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
except Exception as e:
    logging.error(f"Failed to initialize Anthropic client: {e}")
    raise

class ClaudeLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "claude"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            response = client.completion(
                model="claude-2",
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
                max_tokens_to_sample=300,
                stop_sequences=stop if stop else None
            )
            return response.completion
        except Exception as e:
            logging.error(f"Error in Claude API call: {e}")
            raise

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": "claude-2"}

class CodeGenerator:
    @staticmethod
    def generate_code(prompt):
        try:
            claude = ClaudeLLM()
            return claude._call(f"Generate Python code for the following prompt: {prompt}")
        except Exception as e:
            logging.error(f"Error in code generation: {e}")
            raise

class CodeExecutor:
    @staticmethod
    def execute_code(code):
        print("Generated code:")
        print(code)
        confirmation = input("Do you want to execute this code? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Code execution aborted.")
            return "Code execution aborted by user."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(['python', temp_file_path], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return f"Execution Error: {result.stderr}"
            return result.stdout
        except subprocess.TimeoutExpired:
            return "Execution Error: Code execution timed out"
        except Exception as e:
            return f"Execution Error: {str(e)}"
        finally:
            os.unlink(temp_file_path)

def log_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + '\n')

# Create agents
developer = Agent(
    name="Velibor",
    role="Junior Developer",
    goal="Generate code based on prompts",
    backstory="A junior developer eager to learn and implement new ideas.",
    verbose=True,
    llm=ClaudeLLM()
)

senior_developer = Agent(
    name="Chief Technical Officer",
    role="Senior Developer and CTO",
    goal="Oversee code generation and verify its correctness",
    backstory="An experienced CTO with a keen eye for code quality and best practices.",
    verbose=True,
    llm=ClaudeLLM()
)

# Define tasks
task1 = Task(
    description="Generate code based on the CTO's prompt",
    agent=developer,
    expected_output="Python code that fulfills the CTO's requirements"
)

task2 = Task(
    description="Verify the generated code and provide feedback",
    agent=senior_developer,
    expected_output="A detailed review of the code, including suggestions for improvements if necessary"
)

# Create the crew
crew = Crew(
    agents=[developer, senior_developer],
    tasks=[task1, task2],
    verbose=2
)

def main():
    logging.info("Starting the Code Generation and Verification System")
    print("Welcome to the Code Generation and Verification System")
    print("Please enter the requirements for the Senior Developer (CTO):")
    cto_prompt = input("> ")

    log_to_file("promptsanderrors.txt", f"CTO Prompt: {cto_prompt}")

    try:
        # Generate code
        generated_code = CodeGenerator.generate_code(cto_prompt)
        log_to_file("promptsanderrors.txt", f"Generated Code:\n{generated_code}")

        # Save generated code
        with open("main.py", "w") as f:
            f.write(generated_code)

        print("\nCode generated and saved to main.py")
        logging.info("Code generated and saved to main.py")

        # Execute and verify code
        logging.info("Starting crew tasks")
        result = crew.kickoff()
        logging.info("Crew tasks completed")

        log_to_file("promptsanderrors.txt", f"Crew Task Results:\n{result}")

        # Check for errors
        execution_result = CodeExecutor.execute_code(generated_code)
        log_to_file("promptsanderrors.txt", f"Code Execution Result:\n{execution_result}")

        if "Execution Error" in execution_result:
            print(f"\nErrors detected: {execution_result}")
            logging.warning(f"Errors detected in code execution: {execution_result}")
            print("Generating new prompt based on errors...")
            new_prompt = senior_developer.run(f"Generate a new prompt to fix these errors: {execution_result}")
            log_to_file("promptsanderrors.txt", f"New Prompt: {new_prompt}")
            print(f"New prompt generated: {new_prompt}")
        else:
            print("\nCode executed successfully.")
            logging.info("Code executed successfully")

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        log_to_file("promptsanderrors.txt", error_msg)

if __name__ == "__main__":
    main()