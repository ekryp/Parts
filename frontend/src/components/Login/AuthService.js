import auth0 from 'auth0-js'
import router from '../../router'
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)
import * as constant from "../constant/constant";



export default {
    auth0: new auth0.WebAuth({
        audience: 'https://prod-services.ekryp.com/api/v1/',
        domain: 'ekryp.auth0.com',
        clientID: 'NJh7jJsES1ymojwuBodeZJCzT867UNiu',
        redirectUri: constant.APPURL + 'callback',
        responseType: 'token id_token',
        scope: 'openid'
    }),
    handleAuthentication() {
        console.log('callback')
        this.auth0.parseHash((err, authResult) => {
            if (authResult && authResult.accessToken && authResult.idToken) {
                this.getUserInfo(authResult)
                // this.setSession(authResult)
                console.log('success')
                // router.push('/dashboard')
            } else if (err) {
                console.log(err)
                var error_message = err.errorDescription.split(':')[0]
                var error_email_id = err.errorDescription.split(':')[1]
                console.log(error_message)
                console.log(error_email_id)
                axios.post('https://ekryp.auth0.com/dbconnections/change_password', {
	                          "email" :error_email_id,
	                          "connection" :"db-users"
                          });
                alert(err.errorDescription)
                router.push('/')
                //console.log(err)

            }
        })
    },
    getUserInfo(authResult) {
        console.log('authResult ----->', authResult.idTokenPayload.sub)
        fetch('https://ekryp.auth0.com/api/v2/users/' + authResult.idTokenPayload.sub, {
            headers: {
                Authorization: "Bearer " + authResult.idToken
            }
        }).then(function (responseData) {
            responseData.text().then(response => {

                console.log('response ----->', JSON.parse(response))
                let expiresAt = JSON.stringify(authResult.expiresIn)
                localStorage.setItem('auth0_access_token', authResult.accessToken)
                localStorage.setItem('auth0_id_token', authResult.idToken)
                localStorage.setItem('auth0_expires_at', expiresAt)
                var profile = JSON.parse(response)

                localStorage.setItem('isSocial',profile.identities[0].isSocial)
                localStorage.setItem('user_id',profile.user_id)
                //var allowed_custmors = profile.user_metadata.allowed_custmors
                localStorage.setItem('authorization',profile.app_metadata.authorization.permissions)
                localStorage.setItem('groups',profile.app_metadata.authorization.groups)
                localStorage.setItem('auth0_user_id', profile.user_id)
                localStorage.setItem('username', profile.username)
               // localStorage.setItem("allowed_custmors", JSON.stringify(allowed_custmors))
                if (profile.user_id.includes('samlp')) {
                    localStorage.setItem('email_id', profile.email_id)
                    localStorage.setItem('first_name', profile.first_name)
                    localStorage.setItem('last_name', profile.last_name)
                  //  localStorage.setItem('cust_id', profile.cust_id)
                    router.push('/dashboard')
                } else if (profile.user_id.includes('google')) {
                    localStorage.setItem('email_id', profile.email)
                    localStorage.setItem('first_name', profile.given_name)
                    localStorage.setItem('last_name', profile.family_name)
                   /// localStorage.setItem('cust_id', profile.user_metadata.cust_id)
                    router.push('/dashboard')
                } else {
                    localStorage.setItem('email_id', profile.email)
                    var first_name=profile.nickname.split('.')[0].split(' ');
                    localStorage.setItem('first_name', first_name[0])
                    //localStorage.setItem('last_name', profile.user_metadata.last_name)
                  //  localStorage.setItem('cust_id', profile.user_metadata.cust_id)
                    router.push('/dashboard')
                }
            })
        })
            .catch(function (err) {

                console.log(err);
            });
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
