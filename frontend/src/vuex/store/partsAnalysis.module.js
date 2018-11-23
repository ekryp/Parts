import partsAnalysisService from '../services/partsAnalysis.service'

const state = {
    status: {
        success: '',
        failure: '',
    },
    spare_part_analysis: ''
};

const actions = {

    async get_spare_part_analysis({ commit }) {
        console.log('module sucess')
        // partsAnalysisService.get_spare_part_analysis()
        partsAnalysisService.get_spare_part_analysis().then(data => {
            console.log('data ---module-->', new Date(), data)
            commit('spare_part_analysis', data)
        }).catch(error => console.log('error ------>', error))
    }

}

const mutations = {
    spare_part_analysis(state, payload) {
        console.log('mutation ----->', payload)
        state.status.success = true
        state.spare_part_analysis = payload
    }
}

export const partsAnalysis = {
    namespaced: true,
    state,
    actions,
    mutations
};