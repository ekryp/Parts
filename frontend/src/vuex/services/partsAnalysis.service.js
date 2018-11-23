const id_token = localStorage.getItem('id_token');

export default {

    get_spare_part_analysis() {
        console.log('calling service')
        let headers = new Headers;
        headers.append('con', id_token)

        return fetch('http://10.138.1.2:5000/api/v1/get_spare_part_analysis', {
            method: 'GET',
        }).then(response => {
            return this.handleresponse(response)
        }).catch(handleError => {
            console.log(' Error Response ------->', handleError)
        })
    },

    handleresponse(response) {
        console.log('success', response)
        return response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log('data ---->', new Date(), data)
            return data;
        });
    }
}

