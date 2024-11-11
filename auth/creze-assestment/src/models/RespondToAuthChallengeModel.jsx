export const RespondToAuthChallengeRequest = {
    session: '',
    user_code: '',
    username: '' 
}

export const RespondToAuthChallengeRespond = {
    code: null,
    message: '',
    description: '',
    access_token: '',
    id_token: '',
    refresh_token: '',
    token_type: ''
}

export const RespondToAuthChallengeRespondError = {
    detail: {
        code: null,
        message: '',
        description: ''
      }
}