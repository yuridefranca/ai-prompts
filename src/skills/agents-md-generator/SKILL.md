---
name: agents-md-generator
description: Create new AGENTS.md files, modify and improve existing AGENTS.md to be up to date with the project. Use when users want to create a AGENTS.md file or update or optimize an existing one, run evals to test if the file properly describes and is up to date with the project and update it accordingly so AI can get better results when refering to it. Keywords AGENTS.md, documentation, project structure, project features, technologies, dependencies, build commands, test commands, code style guidelines, testing instructions, security considerations, commit messages, pull request guidelines.
---

# AGENTS.md Generator

A skill for creating and updating AGENTS.md files to ensure they are accurate and up-to-date with the project. This skill is essential for maintaining clear documentation of the agents used in the project, which helps AI models refer to it for better results.

At a high level, the process of creating a AGENTS.md file involves:
- Understanding the current state of the project and the agents being used.
- Gathering information about the project technologies, architecture, and dependencies.
- Look for project documentation, code comments, and any relevant information that can help in creating a comprehensive AGENTS.md file.
- Understanding the project's structure, code patterns, naming conventions, libraries, and frameworks to accurately describe the agents in the AGENTS.md file.
- Understanding the projects's main features, functionalities, and use cases to ensure the AGENTS.md file is relevant and useful for users and AI models.
- Running evals to test if the created AGENTS.md file properly describes the project and is up to date, making adjustments as necessary to improve its accuracy and usefulness for users and AI models.

When updating an existing AGENTS.md file, the process involves:
- Reviewing the current AGENTS.md file to identify any outdated or inaccurate information.
- Gathering new information about the project, including any changes in technologies, architecture, dependencies, or features.
- Updating the AGENTS.md file to reflect the current state of the project, ensuring that it accurately describes the agents being used and their functionalities.
- Running evals to test if the updated AGENTS.md file properly describes the project and is up to date, making further adjustments as necessary to improve its accuracy and usefulness for users and AI models.

By maintaining an accurate and up-to-date AGENTS.md file, users and AI models can better understand the agents used in the project, leading to improved results when referring to it for information about the project.

## Output Format
The output of this skill will be a well-structured AGENTS.md file that includes:
```
# Project Name

## Overview
A brief description of the project, its purpose, and its main features.

## Project Architecture
A detailed description of the project's architecture, first describing what architetucture pattern it follows (like layered architecture, hexagonal architecture, microservices, etc) and then describing the different modules or components of the project, their responsibilities.

## Project Features
A detailed description of the main features and functionalities of the project, including any relevant information about the agents being used. When describing the features, group them by context (like on DDD), example: group all features that are user related together, all features that are related to data processing together, etc. Even if they're part of different modules, if they share a common context, group them together and describe how they interact with each other.

## Technologies and Dependencies
A list of the main technologies, libraries, and frameworks used in the project, along with their purposes and any relevant information about their usage in the project, like version numbers, configuration details, and any specific considerations for their integration.

## Build and test commands
A list of the main commands used to build and test the project, along with any relevant information about their usage, such as required environment variables, configuration files, or specific considerations for running them.

## Code style guidelines
A description of the code style guidelines followed in the project, including any specific conventions for naming, formatting, and structuring code, as well as any tools or linters used to enforce these guidelines.

## Testing instructions
A description of the testing instructions for the project, including any specific steps, tools, or frameworks used for testing, as well as any relevant information about test coverage, test data, or test environments.

## Security considerations
A description of any security considerations for the project, including any specific measures taken to ensure the security of the project, such as authentication, authorization, data encryption, or vulnerability management.

## Commit messages and pull request guidelines
A description of the guidelines for commit messages and pull requests in the project, including any specific conventions for formatting commit messages, structuring pull requests, and any relevant information about the review process or requirements for merging code changes.
```

This format ensures that the AGENTS.md file is comprehensive, well-organized, and provides all the necessary information about the project and its agents for users and AI models to refer to.

## Evals
To ensure the AGENTS.md file is accurate and up-to-date, you can run evals that test the file against the current state of the project. These evals can include:
- Comparing the information in the AGENTS.md file with the actual codebase and project documentation to identify any discrepancies or outdated information.
- Testing the AGENTS.md file with AI models to see if it provides accurate and useful information about the project and its agents, and making adjustments as necessary to improve its accuracy and usefulness for users and AI models.
- Gathering feedback from users and AI models about the AGENTS.md file to identify any areas for improvement or additional information that could be included to make it more comprehensive and useful for users and AI models.

By regularly running evals and updating the AGENTS.md file accordingly, you can ensure that it remains a valuable resource for users and AI models to refer to for information about the project and its agents.

## Criteria
The criteria for a successful AGENTS.md file include:
- Accuracy: The AGENTS.md file should accurately describe the project, its architecture, features, technologies, dependencies, build and test commands, code style guidelines, testing instructions, security considerations, and commit messages and pull request guidelines.
- Completeness: The AGENTS.md file should provide comprehensive information about the project and its agents, covering all relevant aspects that users and AI models need to know to understand the project and its agents.
- Clarity: The AGENTS.md file should be well-organized and easy to read, with clear headings, sections, and descriptions that make it easy for users and AI models to find the information they need about the project and its agents.
- Up-to-date: The AGENTS.md file should be regularly updated to reflect any changes in the project, ensuring that it remains accurate and relevant for users and AI models to refer to for information about the project and its agents.

## Extra
To further enhance the AGENTS.md file, you can consider including additional sections such as:
- When finding a Agents.md file, do not delete it, instead, rename it to AGENTS.md.old and create a new AGENTS.md file with the updated information, this way you can keep track of the changes made to the file and refer back to the old version if needed.
