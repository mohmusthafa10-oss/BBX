from google.genai import types

from config import MODEL
from models import CalculatorArgs

from services.gemini_client import retry_call


def calculate(args):

    if args.operation == "add":

        return args.a + args.b

    elif args.operation == "subtract":

        return args.a - args.b

    elif args.operation == "multiply":

        return args.a * args.b

    elif args.operation == "divide":

        if args.b == 0:

            raise ValueError(
                "Division by zero is not allowed."
            )

        return args.a / args.b


def calculator_demo(client, usage_tracker):

    declaration = types.FunctionDeclaration(

        name="calculator",

        description="Perform a basic arithmetic operation.",

        parameters_json_schema=CalculatorArgs.model_json_schema()
    )

    tool = types.Tool(
        function_declarations=[declaration]
    )

    config = types.GenerateContentConfig(

        system_instruction=(
            "Use the calculator function for arithmetic. "
            "Do not calculate mentally."
        ),

        tools=[tool],

        max_output_tokens=300
    )

    contents = [

        types.Content(

            role="user",

            parts=[
                types.Part(
                    text="Calculate (184.5 divided by 3) plus 27."
                )
            ]
        )
    ]

    for _ in range(4):

        response = retry_call(
            lambda: client.models.generate_content(

                model=MODEL,

                contents=contents,

                config=config
            )
        )

        usage_tracker.report(
            response.usage_metadata
        )

        calls = response.function_calls or []

        if not calls:

            print(
                "\n[tool result]",
                response.text or "No text returned."
            )

            return

        # Preserve Gemini's function-call message.

        contents.append(
            response.candidates[0].content
        )

        for call in calls:

            if call.name != "calculator":

                raise ValueError(
                    "Unknown function requested."
                )

            args = CalculatorArgs.model_validate(
                call.args
            )

            result = calculate(args)

            print(
                f"\n[tool execution] "
                f"{args.operation} "
                f"{args.a}, {args.b} = {result}"
            )

            function_response = types.Part.from_function_response(

                name=call.name,

                response={
                    "result": result
                }
            )

            contents.append(
                types.Content(
                    role="user",
                    parts=[function_response]
                )
            )

    print(
        "[tool] Maximum tool-call iterations reached."
    )