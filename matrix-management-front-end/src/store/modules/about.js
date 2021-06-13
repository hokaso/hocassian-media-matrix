const state = {
  info: {
    aboutIcon: "nil.png",
    aboutQrcode: null
  }
};

const mutations = {
  TOGGLE_INFO: (state, info) => {
    state.info = info;
  }
};

const actions = {
  toggleInfo({ commit }, info) {
    commit("TOGGLE_INFO", info);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
