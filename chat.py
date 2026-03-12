from context import add_to_pinned, create_context, add_to_history, build_prompt, get_active_character, get_technique_summary, save_session, load_session, unpin
from engine import ask, validate

def chat(context):
    while True:
        user_input = input("User: ")
        print("Taken!")
        if user_input.startswith("/"):
            result = handle_command(user_input, context)
            if isinstance(result, dict):
                context = result
            elif result == True:
                break
            continue
        prompt = build_prompt(context, user_input)


        response = ask(prompt, context["system"])
        result = validate(response, context["world_rules"], context["scene"], get_technique_summary(context))

        if result.lower() == "no":
            print(response)
            add_to_history(context, user_input)
            add_to_history(context, response)
        else:
            print("Violates world rules!")
            result = ask(prompt)
            print(result)
            add_to_history(context, user_input)
            add_to_history(context, response)

        

def handle_command(user_input, context):
    parts = user_input.split(" ")
    command = parts[0]
    arg1 = parts[1] if len(parts) > 1 else None
    arg2 = parts[2] if len(parts) > 2 else None
    description = " ".join(parts[3:])

    if command == "/unlock":
        character = get_active_character(context, arg2)
        character["state"]["unlocked_techniques"][arg1] = description
    elif command == "/condition":
            character = get_active_character(context, arg2)
            character["state"]["conditions"].append(arg1)
    elif command == "/length":
        context["response_length"] = arg1
        print(f"Response length set to: {arg1}")
    elif command == "/exit":
        print("Bye!")
        return True
    elif command == "/save":
        save_session(context)
    elif command == "/load":
        return load_session()
    elif command == "/pin":
        message = " ".join(parts[1:])
        add_to_pinned(context, message)
    elif command == "/unpin":
        if context["important"]:
            removed = context["important"].pop()
            print(f"Unpinned {removed}")



        
