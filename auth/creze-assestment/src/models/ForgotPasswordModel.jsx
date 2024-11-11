export const ForgotPasswordRequest = {
    username:''
}

export const ForgotPasswordResponse = {
    code: null,
    message: '',
    description: ''
}

export const ForgotPasswordResponseError = {
    detail: {
        code: null,
        message: '',
        description: ''
      }
}

export const ForgotPasswordConfirmationRequest = {
    username: '',
    confirmation_code: '',
    new_password: ''
}

export const ForgotPasswordConfirmationResponse = {
    code: null,
    message: '',
    description: ''
}

export const ForgotPasswordConfirmationResponseError = {
    detail: {
        code: null,
        message: '',
        description: ''
      }
}

