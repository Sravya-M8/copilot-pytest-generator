## Prompt 1: Generate Full Test Suite from User Story
"Generate a complete [Pytest/Jest/JUnit] test suite from this user story.
Cover positive, negative, edge, and boundary cases. Use mocks only.
User Story: [PASTE HERE]"

## Prompt 2: Expand Edge Cases
"Given these acceptance criteria, what edge cases am I missing?
Then generate Pytest tests for each missing case.
Criteria: [PASTE HERE]"

## Prompt 3: Generate Test Data
"Generate a parametrize dataset for testing [feature name]
based on these rules: [PASTE RULES]
Include: valid, invalid, boundary, and null inputs."

## Prompt 4: Convert Manual Test Cases to Automated
"Convert these manual test cases into Pytest code using mocks.
Do not assume any implementation.
Manual Cases: [PASTE HERE]"

## Prompt 5: Generate Negative Tests Only
"From this requirement, generate ONLY negative and error-handling
test cases in Pytest. Focus on: invalid inputs, missing fields,
unauthorized access, and system error responses.
Requirement: [PASTE HERE]"

## Prompt 5: Convert this pytest into manual test cases
"Convert these pytest test cases into manual test cases in table format with:
Test Case ID, Title, Preconditions, Steps, Expected Result"