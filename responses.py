from template import match_response

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    response = match_response(user_input)

    return response

