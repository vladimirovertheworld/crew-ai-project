#!/bin/bash

# File name for the README
README_FILE="README.md"

# Content of the README
cat << EOF > $README_FILE
# Code Generation and Verification System

## Description
This project implements an AI-powered Code Generation and Verification System using the Anthropic API and the CrewAI framework. It automates the process of generating code based on user prompts, verifying the code, and executing it in a controlled environment.

## Features
- AI-powered code generation using Anthropic's Claude model
- Code verification by a simulated senior developer (CTO)
- Sandboxed code execution with user confirmation
- Detailed logging of all operations
- Error handling and new prompt generation for failed executions

## Requirements
- Python 3.x
- anthropic
- crewai
- langchain
- python-dotenv

## Installation
1. Clone this repository:
   \`\`\`
   git clone https://github.com/yourusername/code-generation-system.git
   cd code-generation-system
   \`\`\`

2. Install the required packages:
   \`\`\`
   pip install anthropic crewai langchain python-dotenv
   \`\`\`

3. Set up your Anthropic API key in a \`.env\` file:
   \`\`\`
   ANTHROPIC_API_KEY=your_api_key_here
   \`\`\`

## Usage
Run the script:
\`\`\`
python main.py
\`\`\`

Follow the prompts to enter your code generation requirements. The system will:
1. Generate code based on your prompt
2. Save the generated code to \`main.py\`
3. Verify the code using a simulated CTO review
4. Ask for your confirmation before executing the code
5. Execute the code in a sandboxed environment
6. Provide feedback and generate new prompts if errors occur

## Project Structure
- \`main.py\`: The main script containing all the logic
- \`main.log\`: Log file for all operations
- \`promptsanderrors.txt\`: File containing all prompts, generated code, and execution results

## Safety Features
- Sandboxed code execution using temporary files
- User confirmation required before code execution
- Timeout for code execution to prevent infinite loops

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the [MIT License](LICENSE).
EOF

echo "README.md has been created in the current directory."