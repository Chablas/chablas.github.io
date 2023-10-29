from django.contrib import messages

def emit_message_error(request, errors ='Error de servidor'):
    if(errors == 'Error de servidor' or errors == 'Token inválido' or errors == 'Internal server error'):
        del request.session['token']
        del request.session['usuario']
        
    if (isinstance(errors, str)):
        messages.error(request, errors)
    else:    
        for error in errors: 
            messages.error(request, f"{error['loc'][1]}: {error['msg']}")

    
def emit_message_success(request, msg): messages.success(request, msg)
