import { createStore } from 'vuex'
import ModuleUser from './user'
import ModulePk from './pk'
import ModuleRecord from './record'
import ModuleUtils from './util'

export default createStore({
    state: {
        backPage: "",
    },
    getters: {
    },
    mutations: {
        updateBackPage(state, backPage) {
            state.backPage = backPage;
        }
    },
    actions: {
    },
    modules: {
        user: ModuleUser,
        pk: ModulePk,
        record: ModuleRecord,
        utils: ModuleUtils,
    }
})
