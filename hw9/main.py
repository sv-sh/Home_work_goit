import re
def main():
    global users  # all function can see this variable, not needed to pass it into function additionaly
    users = {}    # store all records
    command_dict = {     # for passing function as variable, a loop.
        'hello':handler_hello, 
        'add':handler_add, 
        'change':handler_change, 
        'phone': handler_phone, 
        'show all':handler_show_all,
        'good bye':handler_exit,
        'close':handler_exit,
        'exit':handler_exit}

    while True:
        cli_in = input("input your command\n" ).lower() # not sensitive to register
        cli_in = cli_in.strip()                         # eliminate first, end spases
        cli_in = re.sub(r"\s+", ' ', cli_in)            # eliminate aditional spaces between words 
        if cli_in == "show all" or cli_in == "good bye":# take into a count key words with spase between
            command_key = cli_in
            command_handler = command_dict[command_key] # get function for execution
            result = command_handler()                  # evoke function
            print(result)            

        elif cli_in.split()[0] in command_dict:         # check if keyword is correct
            command_key = cli_in.split()[0]             # get keyword from input
            if command_key in ("add", "change", "phone"): # function_handlers thees keywords demanded "user" or "user" and "phone" parameters
                args = cli_in.split()[1:]               # get parameters for passing into function_handlers 
                command_handler = command_dict[command_key] 
                result = command_handler( *args)          # evoke function with parameters
                print(result)
            else:
                command_handler = command_dict[command_key] # another key in command dict (hello, close exit)
                result = command_handler()
                print(result)
        
        else:                                              # any input that is not command word
            print(f"wrong command {cli_in}")             
        
        if result == 'good bye':                          # exit from loop
            break


def input_error(func):    # error handler
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return 'No user with this name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
        except TypeError:
            return f'wrong parameters{args} for {func.__name__}'
    return inner

@input_error
def handler_hello(*args):# pass parameters, nou use them, for avoiding errors in decorator input_error(result = func(*args, **kwargs))
    return "How can I help you?"

@input_error
def handler_exit(*args): 
    return 'good bye'

@input_error
def handler_show_all():
    if not users:
        return "No contacts in dictionary"
    return "\n".join([f"{user}:{phone}" for user, phone in users.items()])

@input_error
def handler_phone(user):
    phone = users.get(user)
    return f"The {user}'s phone is {phone}"

@input_error
def handler_change(user, phone):  
    if user in users:      # check if user exist in dictionary, prevent to writing new pair in dict 
        if phone.isdigit(): # check if phone consist from numbers 
            users[user] = phone # modify phone record
            return f"The  {user} phone has been updated to {phone} "
        else:
            return f"wrong parameter {phone} as new phone"
    else:
        raise KeyError

@input_error
def handler_add(user, phone):
    if user.isalpha() and phone.isdigit(): # check if corect values in variables
        users.update({user:phone}) # add new reccord in dict
        return f"The new reccord {user}:{phone} has been added"
    else:
        raise ValueError

if __name__=='__main__':
    main()