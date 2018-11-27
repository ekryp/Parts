import auth0 from 'auth0-js'
import router from '../../router'

export default {
    auth0: new auth0.WebAuth({
        domain: 'ekryp.auth0.com',
        clientID: 'NJh7jJsES1ymojwuBodeZJCzT867UNiu',
        redirectUri: 'http://35.230.112.86:2323/callback',
        responseType: 'token id_token',
        scope: 'openid'
    }),
    handleAuthentication() {
        console.log('callback')
        this.auth0.parseHash((err, authResult) => {
            if (authResult && authResult.accessToken && authResult.idToken) {
                this.setSession(authResult)
                console.log('success')
                router.push('/dashboard')
            } else if (err) {
                router.push('/')
                console.log(err)
            }
        })
    },
    setSession(authResult) {
        console.log('authResult ------>', authResult)
        let expiresAt = JSON.stringify(
            authResult.expiresIn * 1000 + new Date().getTime()
        )
        localStorage.setItem('access_token', authResult.accessToken)
        localStorage.setItem('id_token', authResult.idToken)
        localStorage.setItem('expires_at', expiresAt)
    },

    logout() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('id_token')
        localStorage.removeItem('expires_at')
        this.userProfile = null
        router.replace('/')
    },

    login(context) {
        console.log('login calling')
        localStorage.clear()
        this.auth0.authorize()
    },
    isAuthenticated() {
        let expiresAt = JSON.parse(localStorage.getItem('expires_at'))
        return new Date().getTime() < expiresAt
    }
}
