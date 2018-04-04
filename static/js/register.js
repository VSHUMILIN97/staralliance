    $('#modal_reg').submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/accounts/register/',
            type: 'POST',
            dataType: "json",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            },
            data: $('#registration').serialize(),
            success: function() {
                console.log('success');
            },
            error: function(errorThrown){
                console.log(errorThrown);
            }
        });
    });





// def ajax_registration(request):
//     login_form, registration_form = False, False
//     if request.method == "POST":
//         if "email" in request.POST: //some condition to distinguish between login and registration form
//             login_form = AuthenticationForm(request.POST)
//             if login_form.is_valid():
//                 //log in
//         else:
//             registration_form = RegistrationForm(request.POST)
//             if registration_form.is_valid():
//                 //register
//
//     obj = {
//         'login_form': login_form if login_form else AuthenticationForm(),
//         'registration_form': registration_form if registration_form else RegistrationForm(),
//     }
//     return render(request, 'registration/registration_form.html', obj)
