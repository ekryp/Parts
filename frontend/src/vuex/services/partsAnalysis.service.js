const id_token = localStorage.getItem('id_token');

export default {

    get_spare_part_analysis() {
        console.log('calling get_spare_part_analysis service')
        return fetch('http://10.138.1.2:5000/api/v1/get_spare_part_analysis', {
            method: 'GET',
        }).then(response => {
            return this.handleresponse(response)
        }).catch(handleError => {
            console.log(' Error Response ------->', handleError)
        })
    },

    post_spare_part_analysis(data) {
        console.log('calling create_spare_part_analysis service', data)
        let formData = new FormData();
        formData.append('analysis_name', data.analyisisName)
        formData.append('analysis_type', data.analysisType)
        formData.append('replenish_time', data.replensihTime)
        formData.append('customer_dna_file', data.file)
        formData.append('user_email_id', 'khali.saran@ekryp.com')
        formData.append('customer_name', data.customerNames)
        console.log('formdata ----->', formData.get('analysis_name'))
        return fetch('http://10.138.1.2:5000/api/v1/post_spare_part_analysis', {
            method: 'POST',
            body: formData
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

